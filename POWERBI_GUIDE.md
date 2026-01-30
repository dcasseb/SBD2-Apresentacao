# 📊 Guia de Integração Power BI - Crime Data Analytics

## Visão Geral

Este guia demonstra como conectar o Microsoft Power BI ao banco de dados PostgreSQL do projeto e criar dashboards analíticos baseados nas consultas SQL implementadas.

---

## 🔧 Pré-requisitos

### Software Necessário

1. **Power BI Desktop** (Gratuito)
   - Download: https://powerbi.microsoft.com/pt-br/desktop/
   - Versão recomendada: Latest stable release
   - Tamanho: ~600 MB

2. **Driver PostgreSQL para Power BI**
   - O Power BI Desktop já inclui o driver Npgsql
   - Se necessário, baixar: https://github.com/npgsql/npgsql

3. **Banco de dados PostgreSQL em execução**
   - Container Docker: `sbd2_postgres`
   - Porta: 5432
   - Database: `crime_data`

---

## 📡 Configuração da Conexão

### Passo 1: Iniciar o PostgreSQL

```bash
# Verificar se o container está rodando
docker ps --filter "name=sbd2_postgres"

# Se não estiver rodando, iniciar
docker-compose up -d
```

### Passo 2: Conectar Power BI ao PostgreSQL

1. Abrir **Power BI Desktop**
2. Clicar em **Obter Dados** (Get Data)
3. Procurar por **PostgreSQL database**
4. Inserir as credenciais:

```
Servidor (Server): localhost
Porta (Port): 5432
Banco de Dados (Database): crime_data

Modo de Conectividade: Import (recomendado para melhor performance)
   - Alternativa: DirectQuery (para dados em tempo real)

Usuário: postgres
Senha: postgres
```

### Passo 3: Selecionar Tabelas

Após conectar, selecionar as seguintes tabelas do schema **gold**:

**Tabelas Principais:**
- ✅ `gold.fato_crimes` (38,405 registros)
- ✅ `gold.dim_area` (21 registros)
- ✅ `gold.dim_crime_type` (111 registros)
- ✅ `gold.dim_date` (1,825 registros)
- ✅ `gold.dim_time` (24 registros)
- ✅ `gold.dim_weapon`
- ✅ `gold.dim_premise`
- ✅ `gold.dim_victim` (213 registros)

**Tabelas Agregadas (Opcional):**
- `gold.agg_area_month`
- `gold.agg_crime_year`

---

## 📊 Dashboards Sugeridos

### Dashboard 1: Visão Geral de Crimes

**Componentes:**

1. **KPI Cards (Cartões)**
   - Total de Crimes (38,405)
   - Crimes Violentos (%)
   - Taxa de Crescimento Anual
   - Área mais perigosa

2. **Gráfico de Barras Horizontais**
   - Top 10 Áreas com mais crimes
   - Baseado na Query 1

3. **Gráfico de Pizza**
   - Crimes por Categoria (Violent, Property, Quality of Life, Other)
   - Baseado na Query 2

4. **Gráfico de Linha Temporal**
   - Evolução mensal de crimes (2020-2024)
   - Baseado na Query 3

**DAX Medida Exemplo:**
```dax
Total Crimes = COUNT(fato_crimes[sk_crime])

Violent Crime Rate =
DIVIDE(
    COUNTROWS(FILTER(fato_crimes, fato_crimes[is_violent] = TRUE)),
    COUNTROWS(fato_crimes),
    0
) * 100

YoY Growth =
VAR CurrentYear = CALCULATE([Total Crimes], YEAR(dim_date[full_date]) = MAX(YEAR(dim_date[full_date])))
VAR PreviousYear = CALCULATE([Total Crimes], YEAR(dim_date[full_date]) = MAX(YEAR(dim_date[full_date])) - 1)
RETURN DIVIDE(CurrentYear - PreviousYear, PreviousYear, 0) * 100
```

---

### Dashboard 2: Análise Temporal

**Componentes:**

1. **Heat Map - Crimes por Hora do Dia**
   - Eixo X: Hora (0-23)
   - Eixo Y: Dia da Semana
   - Cor: Intensidade de crimes
   - Baseado na Query 4

2. **Gráfico de Área Empilhada**
   - Crimes ao longo do tempo
   - Segmentado por categoria
   - Baseado na Query 10

3. **Comparativo: Final de Semana vs Dias Úteis**
   - Gráfico de Barras Agrupadas
   - Baseado na Query 7

4. **Slicer (Filtro) de Período**
   - Filtro de data interativo
   - Permite selecionar: Ano, Mês, Trimestre

**DAX Medida Exemplo:**
```dax
Weekend Crimes =
CALCULATE(
    [Total Crimes],
    dim_date[is_weekend] = TRUE
)

Weekday Crimes =
CALCULATE(
    [Total Crimes],
    dim_date[is_weekend] = FALSE
)

Peak Hour =
CALCULATE(
    FIRSTNONBLANK(dim_time[hour], 1),
    TOPN(1, VALUES(dim_time[hour]), [Total Crimes], DESC)
)
```

---

### Dashboard 3: Análise Geográfica

**Componentes:**

1. **Mapa de Calor (Filled Map)**
   - Latitude: `fato_crimes[latitude]`
   - Longitude: `fato_crimes[longitude]`
   - Tamanho da bolha: Quantidade de crimes
   - Cor: Tipo de crime
   - Baseado na Query 9

2. **Gráfico de Barras - Top Áreas**
   - Ranking de áreas por criminalidade
   - Baseado na Query 8

3. **Tabela de Hotspots Críticos**
   - Area, Região, Coordenadas, Total de Crimes
   - Baseado na Query 15 (CTE - Hotspots)

4. **Filtro de Região**
   - Slicer para filtrar por região geográfica

**DAX Medida Exemplo:**
```dax
Crime Density =
DIVIDE(
    [Total Crimes],
    DISTINCTCOUNT(fato_crimes[latitude]),
    0
)

Hotspot Classification =
VAR CrimeCount = [Total Crimes]
VAR Percentile90 = PERCENTILEX.INC(ALL(dim_area), [Total Crimes], 0.9)
RETURN
    SWITCH(
        TRUE(),
        CrimeCount >= Percentile90, "Hotspot Crítico",
        CrimeCount >= Percentile90 * 0.75, "Hotspot Alto",
        CrimeCount >= Percentile90 * 0.5, "Hotspot Médio",
        "Área Normal"
    )
```

---

### Dashboard 4: Perfil de Vítimas e Armas

**Componentes:**

1. **Gráfico de Barras Empilhadas**
   - Crimes por faixa etária da vítima
   - Segmentado por sexo
   - Baseado na Query 6

2. **Treemap - Top 10 Armas**
   - Tamanho proporcional ao número de ocorrências
   - Baseado na Query 5

3. **Matriz de Risco**
   - Heatmap: Idade vs Tipo de Crime
   - Cor: Taxa de criminalidade violenta
   - Baseado na Query 14 (CTE - Perfil de Risco)

4. **Gráfico de Dispersão**
   - X: Idade da vítima
   - Y: Taxa de violência
   - Tamanho: Total de crimes

---

### Dashboard 5: Análise Avançada (CTEs)

**Componentes:**

1. **Gráfico de Linhas com Benchmark**
   - Crimes mensais vs Média histórica
   - Baseado na Query 12 (CTE - Análise Temporal)

2. **Ranking de Crimes por Categoria**
   - Top 5 crimes por categoria
   - Baseado na Query 13 (CTE - Ranking)

3. **Evolução Year-over-Year**
   - Gráfico de cascata mostrando crescimento
   - Por região
   - Baseado na Query 16 (CTE - Evolução Temporal)

4. **Gauge de Performance**
   - % Variação vs ano anterior
   - Indicador visual de tendência

---

## 🔄 Importar Consultas SQL Diretamente

### Método 1: Consulta SQL Personalizada

No Power BI, ao conectar ao PostgreSQL:

1. Clicar em **Advanced Options**
2. Colar a consulta SQL no campo **SQL Statement**

**Exemplo - Query 11 (Áreas acima da média):**

```sql
SELECT
    da.area_name,
    da.region,
    COUNT(*) as total_crimes,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM gold.fato_crimes), 2) as pct_total
FROM gold.fato_crimes fc
JOIN gold.dim_area da ON fc.sk_area = da.sk_area
GROUP BY da.area_name, da.region
HAVING COUNT(*) > (
    SELECT AVG(crime_count)
    FROM (
        SELECT COUNT(*) as crime_count
        FROM gold.fato_crimes
        GROUP BY sk_area
    ) subq
)
ORDER BY total_crimes DESC;
```

### Método 2: Power Query (M Language)

Após importar as tabelas, usar **Transformar Dados** para aplicar as queries:

```m
let
    Source = PostgreSQL.Database("localhost", "crime_data"),
    gold_fato_crimes = Source{[Schema="gold",Item="fato_crimes"]}[Data],
    gold_dim_area = Source{[Schema="gold",Item="dim_area"]}[Data],

    // Merge (JOIN) das tabelas
    MergedQueries = Table.NestedJoin(
        gold_fato_crimes, {"sk_area"},
        gold_dim_area, {"sk_area"},
        "dim_area",
        JoinKind.Inner
    ),

    // Expandir colunas
    ExpandedArea = Table.ExpandTableColumn(
        MergedQueries, "dim_area",
        {"area_name", "region"},
        {"area_name", "region"}
    ),

    // Agrupar e contar
    GroupedRows = Table.Group(
        ExpandedArea,
        {"area_name", "region"},
        {{"total_crimes", each Table.RowCount(_), Int64.Type}}
    )
in
    GroupedRows
```

---

## 🎨 Temas e Formatação Recomendados

### Paleta de Cores Sugerida

**Cores Principais:**
- Crimes Violentos: `#D32F2F` (Vermelho)
- Crimes contra Propriedade: `#F57C00` (Laranja)
- Qualidade de Vida: `#FBC02D` (Amarelo)
- Outros Crimes: `#1976D2` (Azul)

**Gradiente de Intensidade:**
- Baixo: `#81C784` (Verde claro)
- Médio: `#FFB74D` (Laranja claro)
- Alto: `#E57373` (Vermelho claro)
- Crítico: `#D32F2F` (Vermelho escuro)

### Tema JSON (Opcional)

Salvar como `crime_analytics_theme.json`:

```json
{
  "name": "Crime Analytics",
  "dataColors": [
    "#D32F2F",
    "#F57C00",
    "#FBC02D",
    "#1976D2",
    "#7B1FA2",
    "#00796B"
  ],
  "background": "#FFFFFF",
  "foreground": "#212121",
  "tableAccent": "#1976D2"
}
```

Importar em: **Exibição → Temas → Procurar Temas**

---

## 📈 Medidas DAX Essenciais

### Arquivo: `PowerBI_Measures.dax`

```dax
// ============================================
// MEDIDAS BÁSICAS
// ============================================

Total Crimes = COUNTROWS(fato_crimes)

Violent Crimes = CALCULATE([Total Crimes], fato_crimes[is_violent] = TRUE)

Violent Crime Rate = DIVIDE([Violent Crimes], [Total Crimes], 0) * 100

// ============================================
// MEDIDAS TEMPORAIS
// ============================================

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

YoY Change % = DIVIDE([YoY Change], [Crimes Last Year], 0) * 100

MTD Crimes =
CALCULATE(
    [Total Crimes],
    DATESMTD(dim_date[full_date])
)

YTD Crimes =
CALCULATE(
    [Total Crimes],
    DATESYTD(dim_date[full_date])
)

// ============================================
// MEDIDAS GEOGRÁFICAS
// ============================================

Most Dangerous Area =
CALCULATE(
    FIRSTNONBLANK(dim_area[area_name], 1),
    TOPN(1, ALL(dim_area), [Total Crimes], DESC)
)

Safest Area =
CALCULATE(
    FIRSTNONBLANK(dim_area[area_name], 1),
    TOPN(1, ALL(dim_area), [Total Crimes], ASC)
)

Crimes per Square Unit =
DIVIDE(
    [Total Crimes],
    DISTINCTCOUNT(fato_crimes[latitude]) * DISTINCTCOUNT(fato_crimes[longitude]),
    0
)

// ============================================
// MEDIDAS DE RANKING
// ============================================

Area Rank =
RANKX(
    ALL(dim_area[area_name]),
    [Total Crimes],
    ,
    DESC,
    DENSE
)

Crime Type Rank =
RANKX(
    ALL(dim_crime_type[crime_description]),
    [Total Crimes],
    ,
    DESC,
    DENSE
)

// ============================================
// MEDIDAS ANALÍTICAS AVANÇADAS
// ============================================

Moving Average (3 months) =
AVERAGEX(
    DATESINPERIOD(dim_date[full_date], LASTDATE(dim_date[full_date]), -3, MONTH),
    [Total Crimes]
)

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

Risk Score =
VAR ViolentRate = [Violent Crime Rate]
VAR CrimeDensity = [Crimes per Square Unit]
VAR NormalizedViolence = DIVIDE(ViolentRate, 100, 0)
VAR NormalizedDensity = DIVIDE(CrimeDensity, MAXX(ALL(dim_area), [Crimes per Square Unit]), 0)
RETURN (NormalizedViolence * 0.6) + (NormalizedDensity * 0.4)

// ============================================
// FORMATAÇÃO CONDICIONAL
// ============================================

Crime Status Color =
VAR Rate = [Violent Crime Rate]
RETURN
    SWITCH(
        TRUE(),
        Rate >= 50, "#D32F2F",  // Vermelho
        Rate >= 35, "#F57C00",  // Laranja
        Rate >= 20, "#FBC02D",  // Amarelo
        "#4CAF50"               // Verde
    )
```

---

## 🚀 Publicação e Compartilhamento

### Opção 1: Power BI Service (Online)

1. Salvar o arquivo `.pbix` localmente
2. No Power BI Desktop: **Arquivo → Publicar → Publicar no Power BI**
3. Selecionar workspace
4. Configurar atualização automática:
   - Ir para PowerBI.com
   - Configurações do Dataset
   - Agendar atualização (requer Gateway se localhost)

### Opção 2: Exportar para PDF/PowerPoint

1. No Power BI Desktop: **Arquivo → Exportar**
2. Escolher formato: PDF ou PowerPoint
3. Selecionar páginas a exportar

### Opção 3: Publicar Web (Público)

1. Publicar no Power BI Service
2. **Arquivo → Publicar na Web**
3. Gerar código de incorporação (embed)
4. ⚠️ **ATENÇÃO**: Dados ficam públicos!

---

## 🔐 Segurança e Performance

### Boas Práticas

1. **Modo Import vs DirectQuery**
   - Use **Import** para melhor performance (dados são copiados)
   - Use **DirectQuery** apenas se precisar de dados em tempo real

2. **Filtragem no Power Query**
   - Filtrar dados desnecessários antes de carregar
   - Exemplo: Carregar apenas últimos 2 anos

3. **Agregações**
   - Usar tabelas agregadas para grandes volumes
   - Configurar relacionamentos automaticamente

4. **Credenciais**
   - Não compartilhar credenciais do banco
   - Usar usuário read-only para Power BI

```sql
-- Criar usuário read-only para Power BI
CREATE USER powerbi_reader WITH PASSWORD 'secure_password';
GRANT CONNECT ON DATABASE crime_data TO powerbi_reader;
GRANT USAGE ON SCHEMA gold TO powerbi_reader;
GRANT SELECT ON ALL TABLES IN SCHEMA gold TO powerbi_reader;
```

---

## 📦 Checklist de Implementação

### Fase 1: Configuração Inicial
- [ ] Instalar Power BI Desktop
- [ ] Verificar PostgreSQL em execução
- [ ] Testar conexão ao banco de dados
- [ ] Importar todas as tabelas do schema gold

### Fase 2: Modelagem de Dados
- [ ] Verificar relacionamentos entre tabelas (auto-detect)
- [ ] Criar medidas DAX básicas
- [ ] Configurar formatação de colunas (datas, números)
- [ ] Criar hierarquias (Ano → Mês → Dia)

### Fase 3: Criação de Dashboards
- [ ] Dashboard 1: Visão Geral (KPIs principais)
- [ ] Dashboard 2: Análise Temporal
- [ ] Dashboard 3: Análise Geográfica
- [ ] Dashboard 4: Perfil de Vítimas e Armas
- [ ] Dashboard 5: Análise Avançada (CTEs)

### Fase 4: Testes e Validação
- [ ] Testar todos os filtros (slicers)
- [ ] Validar números contra queries SQL
- [ ] Verificar performance (tempo de carregamento)
- [ ] Testar drill-down e drill-through

### Fase 5: Publicação
- [ ] Salvar arquivo .pbix
- [ ] Documentar dashboards criados
- [ ] Exportar para apresentação (PDF/PPT)
- [ ] (Opcional) Publicar no Power BI Service

---

## 🎓 Recursos Adicionais

### Documentação Oficial
- Power BI Desktop: https://powerbi.microsoft.com/documentation/
- DAX Functions: https://dax.guide/
- Power Query M: https://docs.microsoft.com/power-query/

### Tutoriais Recomendados
- Microsoft Learn - Power BI: https://learn.microsoft.com/training/powerplatform/power-bi
- DAX Patterns: https://www.daxpatterns.com/
- SQLBI (Guy in a Cube): https://www.sqlbi.com/

### Templates Úteis
- Crime Analytics Template: https://appsource.microsoft.com (buscar "crime analytics")
- Geographic Analysis: Modelos de mapas de calor

---

## ✅ Conclusão

O Power BI oferece uma solução completa e profissional para visualização dos dados do seu Data Warehouse. Com as 16 consultas SQL já implementadas e o modelo dimensional em star schema, você tem uma base sólida para criar dashboards analíticos robustos.

**Próximos Passos Recomendados:**
1. Instalar Power BI Desktop
2. Conectar ao PostgreSQL
3. Começar pelo Dashboard 1 (Visão Geral)
4. Expandir gradualmente para análises mais complexas
5. Apresentar dashboards no PC2

**Tempo Estimado de Implementação:**
- Configuração inicial: 30 minutos
- Dashboard básico: 1-2 horas
- 5 dashboards completos: 4-6 horas

---

**Autor:** Claude Sonnet 4.5
**Data:** 2026-01-30
**Projeto:** Crime Data Analytics - SBD2 Apresentação
