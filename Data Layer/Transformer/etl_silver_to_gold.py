# Configuração inicial
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
import os
from sqlalchemy import create_engine, text

def find_project_root(start: Path) -> Path:
    for p in [start, *start.parents]:
        if (p / 'Data Layer').exists():
            return p
    return start

# Configurar caminhos
PROJECT_ROOT = find_project_root(Path.cwd())
GOLD_PATH = PROJECT_ROOT / 'Data Layer' / 'gold'
DDL_PATH = GOLD_PATH / 'ddl.sql'

# Configuração PostgreSQL
POSTGRES_DB = os.getenv("POSTGRES_DB", "crime_data")
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
DB_URL = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

# Opções de configuração
SAVE_CSV_BACKUP = True  # Salvar CSV como backup
TRUNCATE_BEFORE_LOAD = True  # Truncar tabelas antes de carregar

# Criar diretório gold se não existir
os.makedirs(GOLD_PATH, exist_ok=True)

print(f"📁 Projeto: {PROJECT_ROOT}")
print(f"📥 Silver: PostgreSQL ({POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB})")
print(f"📤 Gold: PostgreSQL ({POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}) + CSV backups")
print(f"🧱 DDL: {DDL_PATH}")

# Carregar dados Silver do PostgreSQL
engine = create_engine(DB_URL)

# Aplicar DDL da camada Gold
print("🏗️  Aplicando DDL da camada Gold...")
with engine.begin() as conn:
    ddl_sql = DDL_PATH.read_text(encoding="utf-8")
    for stmt in ddl_sql.split(";"):
        stmt = stmt.strip()
        if stmt:
            conn.exec_driver_sql(stmt)
print("✅ Schema Gold criado/atualizado")

# Limpar tabelas antes de carregar (se configurado)
if TRUNCATE_BEFORE_LOAD:
    print("🧹 Limpando tabelas Gold...")
    with engine.begin() as conn:
        # Drop e recreate é mais simples com pandas - drop todas as tabelas
        conn.exec_driver_sql("DROP TABLE IF EXISTS gold.fato_crimes CASCADE")
        conn.exec_driver_sql("DROP TABLE IF EXISTS gold.dim_date CASCADE")
        conn.exec_driver_sql("DROP TABLE IF EXISTS gold.dim_time CASCADE")
        conn.exec_driver_sql("DROP TABLE IF EXISTS gold.dim_area CASCADE")
        conn.exec_driver_sql("DROP TABLE IF EXISTS gold.dim_crime_type CASCADE")
        conn.exec_driver_sql("DROP TABLE IF EXISTS gold.dim_victim CASCADE")
        conn.exec_driver_sql("DROP TABLE IF EXISTS gold.agg_area_month CASCADE")
        conn.exec_driver_sql("DROP TABLE IF EXISTS gold.agg_crime_year CASCADE")
    print("✅ Tabelas antigas removidas")

# Carregar dados Silver
print("\n📥 Carregando dados da camada Silver...")
df_silver = pd.read_sql("SELECT * FROM silver.crimes", engine)

# Datas já estão no formato correto do PostgreSQL

print(f"✅ Dados Silver carregados: {len(df_silver):,} registros")
print(f"📋 Colunas: {len(df_silver.columns)}")
df_silver.head(3)

# Validações padronizadas de schema e qualidade (Silver)
print("🧪 Validando schema e qualidade...")

required_cols = [
    'crime_id', 'date_occurred', 'date_reported', 'hour',
    'area_code', 'area_name',
    'crime_code', 'crime_description', 'crime_category', 'crime_severity',
    'victim_age_group', 'victim_sex_desc', 'victim_descent_desc',
    'victim_age',
    'latitude', 'longitude',
    'is_violent', 'has_weapon', 'case_closed',
    'year', 'month'
 ]

null_thresholds = {
    'crime_id': 0.00,
    'date_occurred': 0.01,
    'hour': 0.01,
    'area_code': 0.01,
    'crime_code': 0.01
}

def validate_silver_schema(df):
    errors = []
    warnings = []

    if df.empty:
        errors.append("Dataset vazio.")

    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        errors.append(f"Colunas ausentes: {missing}")

    for col in ['date_occurred', 'date_reported']:
        if col in df.columns and not pd.api.types.is_datetime64_any_dtype(df[col]):
            warnings.append(f"{col} não está em datetime64; verifique conversão.")

    for col, max_null in null_thresholds.items():
        if col in df.columns:
            pct = df[col].isna().mean()
            if pct > max_null:
                errors.append(f"{col} com {pct:.1%} nulos (limite {max_null:.1%}).")

    if 'hour' in df.columns:
        invalid = ~df['hour'].between(0, 23)
        if invalid.any():
            errors.append(f"hour fora de 0-23: {invalid.sum():,} registros.")

    if 'latitude' in df.columns and 'longitude' in df.columns:
        coords = df[['latitude', 'longitude']].dropna()
        if not coords.empty:
            la_bounds = coords['latitude'].between(33.7, 34.4) & coords['longitude'].between(-118.7, -118.1)
            outside = (~la_bounds).sum()
            if outside / len(coords) > 0.05:
                warnings.append(f"{outside:,} coordenadas fora do limite LA (>5%).")

    if 'crime_severity' in df.columns:
        allowed = {'Serious', 'Minor'}
        invalid = ~df['crime_severity'].dropna().isin(allowed)
        if invalid.any():
            warnings.append(f"crime_severity fora do domínio esperado: {invalid.sum():,} registros.")

    if 'crime_id' in df.columns:
        dup = df['crime_id'].duplicated().sum()
        if dup > 0:
            warnings.append(f"crime_id duplicado: {dup:,}")

    return errors, warnings

errors, warnings = validate_silver_schema(df_silver)
if warnings:
    print("⚠️ Avisos:")
    for w in warnings:
        print(f"   - {w}")

if errors:
    print("❌ Erros:")
    for e in errors:
        print(f"   - {e}")
    raise ValueError("Falha nas validações de schema/qualidade. Corrija antes de gerar a Gold.")
else:
    print("✅ Validações concluídas com sucesso.")

## Criação das Dimensões

# Dimensão: Data (dim_date)
print("📅 Criando dim_date...")

dim_date = df_silver[['date_occurred']].drop_duplicates().copy()
dim_date = dim_date.dropna()
dim_date['sk_date'] = range(1, len(dim_date) + 1)
dim_date['full_date'] = dim_date['date_occurred']
dim_date['year'] = dim_date['date_occurred'].dt.year
dim_date['quarter'] = dim_date['date_occurred'].dt.quarter
dim_date['month'] = dim_date['date_occurred'].dt.month
dim_date['month_name'] = dim_date['date_occurred'].dt.month_name()
dim_date['week_of_year'] = dim_date['date_occurred'].dt.isocalendar().week
dim_date['day_of_month'] = dim_date['date_occurred'].dt.day
dim_date['day_of_week'] = dim_date['date_occurred'].dt.dayofweek
dim_date['day_name'] = dim_date['date_occurred'].dt.day_name()
dim_date['is_weekend'] = dim_date['day_of_week'].isin([5, 6])
dim_date = dim_date.drop(columns=['date_occurred'])

# Salvar no PostgreSQL (fail se já existir significa que não foi truncado)
dim_date.to_sql('dim_date', engine, schema='gold', if_exists='fail', index=False, method='multi')
if SAVE_CSV_BACKUP:
    dim_date.to_csv(GOLD_PATH / 'dim_date.csv', index=False)
print(f"   ✅ dim_date: {len(dim_date):,} registros (PostgreSQL + CSV)")

# Dimensão: Tempo (dim_time)
print("⏰ Criando dim_time...")

dim_time = pd.DataFrame({'hour': range(24)})
dim_time['sk_time'] = dim_time['hour'] + 1
dim_time['period_of_day'] = dim_time['hour'].apply(
    lambda h: 'Madrugada' if h < 6 else 'Manhã' if h < 12 else 'Tarde' if h < 18 else 'Noite'
)
dim_time['is_rush_hour'] = dim_time['hour'].isin([7, 8, 9, 17, 18, 19])

# Salvar no PostgreSQL
dim_time.to_sql('dim_time', engine, schema='gold', if_exists='fail', index=False, method='multi')
if SAVE_CSV_BACKUP:
    dim_time.to_csv(GOLD_PATH / 'dim_time.csv', index=False)
print(f"   ✅ dim_time: {len(dim_time):,} registros (PostgreSQL + CSV)")

# Dimensão: Área (dim_area)
print("📍 Criando dim_area...")

dim_area = df_silver[['area_code', 'area_name']].drop_duplicates().copy()
dim_area['sk_area'] = range(1, len(dim_area) + 1)

# Classificar regiões
def get_region(area_name):
    north = ['DEVONSHIRE', 'FOOTHILL', 'MISSION', 'NORTH HOLLYWOOD', 'VAN NUYS', 'WEST VALLEY']
    south = ['77TH STREET', 'HARBOR', 'SOUTHEAST', 'SOUTHWEST']
    central = ['CENTRAL', 'HOLLENBECK', 'RAMPART']
    west = ['HOLLYWOOD', 'OLYMPIC', 'PACIFIC', 'WEST LA', 'WILSHIRE']
    
    if area_name in north: return 'North'
    elif area_name in south: return 'South'
    elif area_name in central: return 'Central'
    elif area_name in west: return 'West'
    else: return 'Other'

dim_area['region'] = dim_area['area_name'].apply(get_region)

# Salvar no PostgreSQL
dim_area.to_sql('dim_area', engine, schema='gold', if_exists='fail', index=False, method='multi')
if SAVE_CSV_BACKUP:
    dim_area.to_csv(GOLD_PATH / 'dim_area.csv', index=False)
print(f"   ✅ dim_area: {len(dim_area):,} registros (PostgreSQL + CSV)")

# Dimensão: Tipo de Crime (dim_crime_type)
print("🔍 Criando dim_crime_type...")

dim_crime_type = df_silver[['crime_code', 'crime_description', 'crime_category', 'crime_severity']].drop_duplicates().copy()
dim_crime_type['sk_crime_type'] = range(1, len(dim_crime_type) + 1)
dim_crime_type['is_violent'] = dim_crime_type['crime_category'] == 'Violent Crime'
dim_crime_type['severity_level'] = dim_crime_type['crime_severity'].map({'Serious': 3, 'Minor': 1})

# Salvar no PostgreSQL
dim_crime_type.to_sql('dim_crime_type', engine, schema='gold', if_exists='fail', index=False, method='multi')
if SAVE_CSV_BACKUP:
    dim_crime_type.to_csv(GOLD_PATH / 'dim_crime_type.csv', index=False)
print(f"   ✅ dim_crime_type: {len(dim_crime_type):,} registros (PostgreSQL + CSV)")

# Dimensão: Vítima (dim_victim)
print("👤 Criando dim_victim...")

dim_victim = df_silver[['victim_age_group', 'victim_sex_desc', 'victim_descent_desc']].drop_duplicates().copy()
dim_victim['sk_victim'] = range(1, len(dim_victim) + 1)
dim_victim = dim_victim.rename(columns={
    'victim_age_group': 'age_group',
    'victim_sex_desc': 'sex',
    'victim_descent_desc': 'descent'
})

# Salvar no PostgreSQL
dim_victim.to_sql('dim_victim', engine, schema='gold', if_exists='fail', index=False, method='multi')
if SAVE_CSV_BACKUP:
    dim_victim.to_csv(GOLD_PATH / 'dim_victim.csv', index=False)
print(f"   ✅ dim_victim: {len(dim_victim):,} registros (PostgreSQL + CSV)")

## Criação da Tabela Fato

# Tabela Fato: fato_crimes
print("📊 Criando fato_crimes...")

# Criar mapeamentos de surrogate keys
date_map = dim_date.set_index('full_date')['sk_date'].to_dict()
time_map = dim_time.set_index('hour')['sk_time'].to_dict()
area_map = dim_area.set_index('area_code')['sk_area'].to_dict()
crime_type_map = dim_crime_type.set_index('crime_code')['sk_crime_type'].to_dict()

# Criar chave composta para victim
dim_victim['victim_key'] = dim_victim['age_group'] + '|' + dim_victim['sex'] + '|' + dim_victim['descent']
victim_map = dim_victim.set_index('victim_key')['sk_victim'].to_dict()

# Construir fato
fato = pd.DataFrame()
fato['sk_crime'] = range(1, len(df_silver) + 1)
fato['nk_crime_id'] = df_silver['crime_id'].values
fato['sk_date'] = df_silver['date_occurred'].map(date_map).values
fato['sk_time'] = df_silver['hour'].map(time_map).values
fato['sk_area'] = df_silver['area_code'].map(area_map).values
fato['sk_crime_type'] = df_silver['crime_code'].map(crime_type_map).values

# Mapear vítima
df_silver['victim_key'] = df_silver['victim_age_group'] + '|' + df_silver['victim_sex_desc'] + '|' + df_silver['victim_descent_desc']
fato['sk_victim'] = df_silver['victim_key'].map(victim_map).values

# Métricas
fato['latitude'] = df_silver['latitude'].values
fato['longitude'] = df_silver['longitude'].values
fato['is_violent'] = df_silver['is_violent'].values
fato['has_weapon'] = df_silver['has_weapon'].values
fato['case_closed'] = df_silver['case_closed'].values

# Salvar no PostgreSQL
fato.to_sql('fato_crimes', engine, schema='gold', if_exists='fail', index=False, chunksize=5000, method='multi')
if SAVE_CSV_BACKUP:
    fato.to_csv(GOLD_PATH / 'fato_crimes.csv', index=False)
print(f"   ✅ fato_crimes: {len(fato):,} registros (PostgreSQL + CSV)")

## Criação das Agregações

# Agregação: Crimes por Área e Mês
print("📈 Criando agregações...")

agg_area_month = df_silver.groupby(['area_name', 'year', 'month']).agg(
    total_crimes=('crime_id', 'count'),
    violent_crimes=('is_violent', 'sum'),
    crimes_with_weapon=('has_weapon', 'sum'),
    cases_closed=('case_closed', 'sum')
).reset_index()

# Salvar no PostgreSQL
agg_area_month.to_sql('agg_area_month', engine, schema='gold', if_exists='fail', index=False, method='multi')
if SAVE_CSV_BACKUP:
    agg_area_month.to_csv(GOLD_PATH / 'agg_area_month.csv', index=False)
print(f"   ✅ agg_area_month: {len(agg_area_month):,} registros (PostgreSQL + CSV)")

# Agregação: Crimes por Tipo e Ano
agg_crime_year = df_silver.groupby(['crime_description', 'crime_category', 'year']).agg(
    total_crimes=('crime_id', 'count'),
    avg_victim_age=('victim_age', 'mean')
).reset_index()

# Salvar no PostgreSQL
agg_crime_year.to_sql('agg_crime_year', engine, schema='gold', if_exists='replace', index=False, method='multi')
if SAVE_CSV_BACKUP:
    agg_crime_year.to_csv(GOLD_PATH / 'agg_crime_year.csv', index=False)
print(f"   ✅ agg_crime_year: {len(agg_crime_year):,} registros (PostgreSQL + CSV)")

# Resumo final
print("\n" + "="*50)
print("✅ ETL Silver → Gold concluído!")
print("="*50)

# Verificar dados carregados no PostgreSQL
print("\n📊 Resumo do carregamento (PostgreSQL):")
with engine.connect() as conn:
    tables_to_check = [
        'dim_date', 'dim_time', 'dim_area', 'dim_crime_type', 'dim_victim',
        'fato_crimes', 'agg_area_month', 'agg_crime_year'
    ]
    for table in tables_to_check:
        result = conn.execute(text(f"SELECT COUNT(*) FROM gold.{table}"))
        count = result.scalar()
        print(f"   📊 gold.{table}: {count:,} registros")

if SAVE_CSV_BACKUP:
    print("\n📁 Arquivos CSV de backup:")
    for f in sorted(GOLD_PATH.glob('*.csv')):
        size_kb = f.stat().st_size / 1024
        print(f"   📁 {f.name}: {size_kb:.1f} KB")
    print(f"\n📂 Diretório CSV: {GOLD_PATH}")

print(f"\n🗄️  Base de dados Gold: {POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}")
