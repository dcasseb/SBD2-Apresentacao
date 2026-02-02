"""
Power BI Dashboard Automation Script
Gera queries SQL e estruturas que podem ser importadas no Power BI Desktop
"""

import json
import psycopg2
from datetime import datetime

# ============================================
# CONFIGURAÇÃO DO BANCO DE DADOS
# ============================================

DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'crime_data',
    'user': 'postgres',
    'password': 'postgres'
}

# ============================================
# QUERIES SQL PARA POWER BI
# ============================================

QUERIES = {
    'dashboard_1_overview': """
        -- Dashboard 1: Visão Geral
        SELECT
            da.area_name,
            da.region,
            COUNT(*) as total_crimes,
            SUM(CASE WHEN fc.is_violent THEN 1 ELSE 0 END) as violent_crimes,
            ROUND(SUM(CASE WHEN fc.is_violent THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as violent_rate
        FROM gold.fato_crimes fc
        JOIN gold.dim_area da ON fc.sk_area = da.sk_area
        GROUP BY da.area_name, da.region
        ORDER BY total_crimes DESC;
    """,

    'dashboard_2_temporal': """
        -- Dashboard 2: Análise Temporal
        SELECT
            dd.year,
            dd.month,
            dd.month_name,
            dd.day_of_week,
            dd.is_weekend,
            dt.hour,
            dt.period_of_day,
            COUNT(*) as total_crimes,
            SUM(CASE WHEN fc.is_violent THEN 1 ELSE 0 END) as violent_crimes
        FROM gold.fato_crimes fc
        JOIN gold.dim_date dd ON fc.sk_date = dd.sk_date
        JOIN gold.dim_time dt ON fc.sk_time = dt.sk_time
        GROUP BY dd.year, dd.month, dd.month_name, dd.day_of_week, dd.is_weekend,
                 dt.hour, dt.period_of_day
        ORDER BY dd.year, dd.month, dt.hour;
    """,

    'dashboard_3_geographic': """
        -- Dashboard 3: Análise Geográfica
        SELECT
            da.area_name,
            da.region,
            fc.latitude,
            fc.longitude,
            dct.crime_category,
            dct.crime_description,
            COUNT(*) as crime_count
        FROM gold.fato_crimes fc
        JOIN gold.dim_area da ON fc.sk_area = da.sk_area
        JOIN gold.dim_crime_type dct ON fc.sk_crime_type = dct.sk_crime_type
        WHERE fc.latitude IS NOT NULL AND fc.longitude IS NOT NULL
        GROUP BY da.area_name, da.region, fc.latitude, fc.longitude,
                 dct.crime_category, dct.crime_description;
    """,

    'dashboard_4_victims_weapons': """
        -- Dashboard 4: Perfil de Vítimas e Armas
        SELECT
            dv.age_group,
            dv.sex,
            dv.descent,
            dw.weapon_description,
            dw.weapon_category,
            dct.crime_category,
            COUNT(*) as total_crimes,
            SUM(CASE WHEN fc.is_violent THEN 1 ELSE 0 END) as violent_crimes
        FROM gold.fato_crimes fc
        JOIN gold.dim_victim dv ON fc.sk_victim = dv.sk_victim
        LEFT JOIN gold.dim_weapon dw ON fc.sk_weapon = dw.sk_weapon
        JOIN gold.dim_crime_type dct ON fc.sk_crime_type = dct.sk_crime_type
        GROUP BY dv.age_group, dv.sex, dv.descent,
                 dw.weapon_description, dw.weapon_category, dct.crime_category;
    """,

    'dashboard_5_advanced': """
        -- Dashboard 5: Análise Avançada (CTE)
        WITH monthly_stats AS (
            SELECT
                dd.year,
                dd.month,
                dd.month_name,
                COUNT(*) as total_crimes,
                SUM(CASE WHEN fc.is_violent THEN 1 ELSE 0 END) as violent_crimes
            FROM gold.fato_crimes fc
            JOIN gold.dim_date dd ON fc.sk_date = dd.sk_date
            GROUP BY dd.year, dd.month, dd.month_name
        ),
        monthly_avg AS (
            SELECT
                AVG(total_crimes) as avg_monthly_crimes,
                AVG(violent_crimes) as avg_monthly_violent
            FROM monthly_stats
        )
        SELECT
            ms.year,
            ms.month,
            ms.month_name,
            ms.total_crimes,
            ms.violent_crimes,
            ma.avg_monthly_crimes,
            ma.avg_monthly_violent,
            ROUND((ms.total_crimes - ma.avg_monthly_crimes) / ma.avg_monthly_crimes * 100, 2) as pct_diff_from_avg
        FROM monthly_stats ms
        CROSS JOIN monthly_avg ma
        ORDER BY ms.year, ms.month;
    """
}

# ============================================
# MEDIDAS DAX
# ============================================

DAX_MEASURES = {
    'basic_measures': """
// MEDIDAS BÁSICAS
Total Crimes = COUNTROWS(fato_crimes)

Violent Crimes =
CALCULATE(
    [Total Crimes],
    fato_crimes[is_violent] = TRUE()
)

Violent Crime Rate =
DIVIDE([Violent Crimes], [Total Crimes], 0) * 100

Average Crimes per Area =
AVERAGEX(
    VALUES(dim_area[area_name]),
    [Total Crimes]
)
""",

    'temporal_measures': """
// MEDIDAS TEMPORAIS
Crimes This Year =
CALCULATE(
    [Total Crimes],
    YEAR(dim_date[full_date]) = YEAR(TODAY())
)

Crimes Last Year =
CALCULATE(
    [Total Crimes],
    YEAR(dim_date[full_date]) = YEAR(TODAY()) - 1
)

YoY Change = [Crimes This Year] - [Crimes Last Year]

YoY Change % =
DIVIDE([YoY Change], [Crimes Last Year], 0) * 100

Moving Average 3M =
AVERAGEX(
    DATESINPERIOD(
        dim_date[full_date],
        LASTDATE(dim_date[full_date]),
        -3,
        MONTH
    ),
    [Total Crimes]
)
""",

    'geographic_measures': """
// MEDIDAS GEOGRÁFICAS
Most Dangerous Area =
CALCULATE(
    FIRSTNONBLANK(dim_area[area_name], 1),
    TOPN(1, ALL(dim_area), [Total Crimes], DESC)
)

Area Rank =
RANKX(
    ALL(dim_area[area_name]),
    [Total Crimes],
    ,
    DESC,
    DENSE
)

Crime Density =
DIVIDE(
    [Total Crimes],
    DISTINCTCOUNT(fato_crimes[latitude]) * DISTINCTCOUNT(fato_crimes[longitude]),
    0
)
""",

    'advanced_measures': """
// MEDIDAS AVANÇADAS
Risk Score =
VAR ViolentRate = [Violent Crime Rate]
VAR CrimeDensity = [Crime Density]
VAR NormalizedViolence = DIVIDE(ViolentRate, 100, 0)
VAR NormalizedDensity = DIVIDE(CrimeDensity, MAXX(ALL(dim_area), [Crime Density]), 0)
RETURN (NormalizedViolence * 0.6) + (NormalizedDensity * 0.4)

Crime Trend =
VAR CurrentMonth = [Total Crimes]
VAR PreviousMonth = CALCULATE([Total Crimes], DATEADD(dim_date[full_date], -1, MONTH))
RETURN
    SWITCH(
        TRUE(),
        CurrentMonth > PreviousMonth * 1.1, "📈 Crescendo",
        CurrentMonth < PreviousMonth * 0.9, "📉 Diminuindo",
        "➡️ Estável"
    )

Percentile 90 =
PERCENTILEX.INC(
    ALL(dim_area),
    [Total Crimes],
    0.9
)

Hotspot Classification =
VAR CrimeCount = [Total Crimes]
VAR P90 = [Percentile 90]
RETURN
    SWITCH(
        TRUE(),
        CrimeCount >= P90, "Hotspot Crítico",
        CrimeCount >= P90 * 0.75, "Hotspot Alto",
        CrimeCount >= P90 * 0.5, "Hotspot Médio",
        "Área Normal"
    )
"""
}

# ============================================
# ESTRUTURA DE DASHBOARDS
# ============================================

DASHBOARD_STRUCTURE = {
    'dashboard_1': {
        'name': 'Visão Geral de Crimes',
        'visuals': [
            {
                'type': 'card',
                'title': 'Total de Crimes',
                'measure': 'Total Crimes',
                'position': {'x': 0, 'y': 0, 'width': 3, 'height': 2}
            },
            {
                'type': 'card',
                'title': 'Taxa de Crimes Violentos',
                'measure': 'Violent Crime Rate',
                'format': '0.00%',
                'position': {'x': 3, 'y': 0, 'width': 3, 'height': 2}
            },
            {
                'type': 'card',
                'title': 'Área Mais Perigosa',
                'measure': 'Most Dangerous Area',
                'position': {'x': 6, 'y': 0, 'width': 3, 'height': 2}
            },
            {
                'type': 'card',
                'title': 'Crescimento Anual',
                'measure': 'YoY Change %',
                'format': '0.00%',
                'position': {'x': 9, 'y': 0, 'width': 3, 'height': 2}
            },
            {
                'type': 'bar_chart',
                'title': 'Top 10 Áreas com Mais Crimes',
                'x_axis': 'dim_area[area_name]',
                'y_axis': 'Total Crimes',
                'sort': 'descending',
                'top_n': 10,
                'position': {'x': 0, 'y': 2, 'width': 6, 'height': 4}
            },
            {
                'type': 'pie_chart',
                'title': 'Crimes por Categoria',
                'legend': 'dim_crime_type[crime_category]',
                'values': 'Total Crimes',
                'position': {'x': 6, 'y': 2, 'width': 6, 'height': 4}
            },
            {
                'type': 'line_chart',
                'title': 'Evolução Temporal',
                'x_axis': 'dim_date[full_date]',
                'y_axis': ['Total Crimes', 'Violent Crimes'],
                'position': {'x': 0, 'y': 6, 'width': 12, 'height': 4}
            }
        ]
    },
    'dashboard_2': {
        'name': 'Análise Temporal',
        'visuals': [
            {
                'type': 'matrix',
                'title': 'Heatmap - Crimes por Hora e Dia',
                'rows': 'dim_date[day_of_week]',
                'columns': 'dim_time[hour]',
                'values': 'Total Crimes',
                'color_scale': 'sequential',
                'position': {'x': 0, 'y': 0, 'width': 8, 'height': 5}
            },
            {
                'type': 'column_chart',
                'title': 'Crimes por Período do Dia',
                'x_axis': 'dim_time[period_of_day]',
                'y_axis': 'Total Crimes',
                'position': {'x': 8, 'y': 0, 'width': 4, 'height': 5}
            },
            {
                'type': 'area_chart',
                'title': 'Tendência Mensal com Média Móvel',
                'x_axis': 'dim_date[month_name]',
                'y_axis': ['Total Crimes', 'Moving Average 3M'],
                'position': {'x': 0, 'y': 5, 'width': 12, 'height': 5}
            }
        ]
    },
    'dashboard_3': {
        'name': 'Análise Geográfica',
        'visuals': [
            {
                'type': 'map',
                'title': 'Mapa de Calor de Crimes',
                'latitude': 'fato_crimes[latitude]',
                'longitude': 'fato_crimes[longitude]',
                'size': 'Total Crimes',
                'color': 'dim_crime_type[crime_category]',
                'position': {'x': 0, 'y': 0, 'width': 8, 'height': 8}
            },
            {
                'type': 'bar_chart',
                'title': 'Top 10 Áreas',
                'x_axis': 'Total Crimes',
                'y_axis': 'dim_area[area_name]',
                'color': 'Hotspot Classification',
                'top_n': 10,
                'position': {'x': 8, 'y': 0, 'width': 4, 'height': 8}
            },
            {
                'type': 'table',
                'title': 'Detalhamento de Hotspots',
                'columns': ['dim_area[area_name]', 'Total Crimes', 'Violent Crime Rate', 'Hotspot Classification'],
                'position': {'x': 0, 'y': 8, 'width': 12, 'height': 2}
            }
        ]
    }
}

# ============================================
# FUNÇÕES DE EXPORTAÇÃO
# ============================================

def export_queries_to_file(output_dir='./powerbi_exports'):
    """Exporta queries SQL para arquivos individuais"""
    import os
    os.makedirs(output_dir, exist_ok=True)

    for name, query in QUERIES.items():
        filepath = os.path.join(output_dir, f'{name}.sql')
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(query)
        print(f"[OK] Exportado: {filepath}")

def export_dax_measures(output_dir='./powerbi_exports'):
    """Exporta medidas DAX para arquivo"""
    import os
    os.makedirs(output_dir, exist_ok=True)

    filepath = os.path.join(output_dir, 'dax_measures.dax')
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write("// ============================================\n")
        f.write("// MEDIDAS DAX - CRIME DATA ANALYTICS\n")
        f.write(f"// Gerado em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("// ============================================\n\n")

        for category, measures in DAX_MEASURES.items():
            f.write(measures)
            f.write("\n\n")

    print(f"[OK] Exportado: {filepath}")

def export_dashboard_structure(output_dir='./powerbi_exports'):
    """Exporta estrutura de dashboards como JSON"""
    import os
    os.makedirs(output_dir, exist_ok=True)

    filepath = os.path.join(output_dir, 'dashboard_structure.json')
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(DASHBOARD_STRUCTURE, f, indent=2, ensure_ascii=False)

    print(f"[OK] Exportado: {filepath}")

def execute_query_and_export_csv(query_name, query, output_dir='./powerbi_exports'):
    """Executa query e exporta resultado para CSV"""
    import os
    import csv

    os.makedirs(output_dir, exist_ok=True)

    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()

        cursor.execute(query)
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]

        filepath = os.path.join(output_dir, f'{query_name}.csv')
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(columns)
            writer.writerows(rows)

        print(f"[OK] Exportado CSV: {filepath} ({len(rows)} linhas)")

        cursor.close()
        conn.close()

    except Exception as e:
        print(f"[ERRO] Erro ao executar {query_name}: {str(e)}")

def generate_powerbi_connection_string():
    """Gera string de conexão para Power BI"""
    connection_string = f"""
Servidor PostgreSQL: {DB_CONFIG['host']}
Porta: {DB_CONFIG['port']}
Banco de Dados: {DB_CONFIG['database']}
Usuário: {DB_CONFIG['user']}

String de conexão completa:
postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}
"""
    return connection_string

# ============================================
# FUNÇÃO PRINCIPAL
# ============================================

def main():
    """Executa todas as exportações"""
    print("Iniciando exportacao de artefatos para Power BI...")
    print("=" * 60)

    # 1. Exportar queries SQL
    print("\nExportando queries SQL...")
    export_queries_to_file()

    # 2. Exportar medidas DAX
    print("\nExportando medidas DAX...")
    export_dax_measures()

    # 3. Exportar estrutura de dashboards
    print("\nExportando estrutura de dashboards...")
    export_dashboard_structure()

    # 4. Executar queries e exportar CSVs
    print("\nExecutando queries e exportando dados...")
    for name, query in QUERIES.items():
        execute_query_and_export_csv(name, query)

    # 5. Gerar informações de conexão
    print("\nInformacoes de conexao:")
    print(generate_powerbi_connection_string())

    print("\n" + "=" * 60)
    print("Exportacao concluida!")
    print("\nArquivos gerados em: ./powerbi_exports/")
    print("\nProximos passos:")
    print("1. Abrir Power BI Desktop")
    print("2. Conectar ao PostgreSQL usando as credenciais acima")
    print("3. Importar as queries SQL ou CSVs exportados")
    print("4. Copiar e colar as medidas DAX")
    print("5. Criar visualizacoes baseadas na estrutura JSON")

if __name__ == '__main__':
    main()
