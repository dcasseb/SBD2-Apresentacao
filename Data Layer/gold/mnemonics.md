# Mnemonics - Gold Layer
## Crime Data Analytics - Data Warehouse

---

## Tabelas (Tables)

| Mnemônico | Nome SQL | Descrição |
|-----------|----------|-----------|
| FCR | fato_crimes | Tabela Fato de Crimes |
| DAR | dim_area | Dimensão Área |
| DCT | dim_crime_type | Dimensão Tipo de Crime |
| DWP | dim_weapon | Dimensão Arma |
| DPR | dim_premise | Dimensão Local |
| DDT | dim_date | Dimensão Data |
| DTM | dim_time | Dimensão Tempo |
| DVC | dim_victim | Dimensão Vítima |

---

## Chaves (Keys)

| Mnemônico | Nome SQL | Descrição |
|-----------|----------|-----------|
| SKA | sk_area | Surrogate Key Área |
| SKC | sk_crime | Surrogate Key Crime |
| SKT | sk_crime_type | Surrogate Key Tipo Crime |
| SKD | sk_date | Surrogate Key Data |
| SKH | sk_time | Surrogate Key Hora |
| SKV | sk_victim | Surrogate Key Vítima |
| SKW | sk_weapon | Surrogate Key Arma |
| SKP | sk_premise | Surrogate Key Local |
| NKC | nk_crime_id | Natural Key Crime |

---

## Atributos Geográficos (Geographic)

| Mnemônico | Nome SQL | Descrição |
|-----------|----------|-----------|
| ARC | area_code | Código da Área |
| ARN | area_name | Nome da Área |
| REG | region | Região |
| LAT | latitude | Latitude |
| LON | longitude | Longitude |

---

## Atributos de Crime (Crime)

| Mnemônico | Nome SQL | Descrição |
|-----------|----------|-----------|
| CRC | crime_code | Código do Crime |
| CRD | crime_description | Descrição do Crime |
| CAT | crime_category | Categoria do Crime |
| SVL | severity_level | Nível de Severidade |
| ISV | is_violent | É Violento |

---

## Atributos Temporais (Temporal)

| Mnemônico | Nome SQL | Descrição |
|-----------|----------|-----------|
| FDT | full_date | Data Completa |
| YEA | year | Ano |
| QTR | quarter | Trimestre |
| MON | month | Mês |
| MNM | month_name | Nome do Mês |
| WOY | week_of_year | Semana do Ano |
| DOM | day_of_month | Dia do Mês |
| DOW | day_of_week | Dia da Semana |
| DNM | day_name | Nome do Dia |
| HOU | hour | Hora |
| PRD | period_of_day | Período do Dia |
| ISW | is_weekend | É Fim de Semana |
| ISH | is_holiday | É Feriado |
| ISR | is_rush_hour | É Horário de Pico |

---

## Atributos de Vítima (Victim)

| Mnemônico | Nome SQL | Descrição |
|-----------|----------|-----------|
| AGG | age_group | Faixa Etária |
| SEX | sex | Sexo |
| DSC | descent | Descendência/Etnia |

---

## Atributos de Arma (Weapon)

| Mnemônico | Nome SQL | Descrição |
|-----------|----------|-----------|
| WPC | weapon_code | Código da Arma |
| WPD | weapon_description | Descrição da Arma |
| WCA | weapon_category | Categoria da Arma |
| LTL | lethality_level | Nível de Letalidade |

---

## Atributos de Local (Premise)

| Mnemônico | Nome SQL | Descrição |
|-----------|----------|-----------|
| PMC | premise_code | Código do Local |
| PMD | premise_description | Descrição do Local |
| PCA | premise_category | Categoria do Local |
| ISP | is_public | É Público |

---

## Métricas e Agregações (Metrics)

| Mnemônico | Nome SQL | Descrição |
|-----------|----------|-----------|
| TCR | total_crimes | Total de Crimes |
| VCR | violent_crimes | Crimes Violentos |
| PCR | property_crimes | Crimes Patrimoniais |
| TOC | total_occurrences | Total de Ocorrências |
| TUS | total_uso | Total de Uso |
| TVT | total_vitimas | Total de Vítimas |
| PCT | percentual | Percentual |
| PCV | pct_violent | Percentual Violento |
| PCD | pct_diff_from_avg | Diferença Percentual da Média |
| AVG | avg_monthly_crimes | Média Mensal de Crimes |
| CRC | crime_count | Contagem de Crimes |

---

## Campos Calculados (CTEs)

| Mnemônico | Nome SQL | Descrição |
|-----------|----------|-----------|
| RIC | rank_in_category | Ranking na Categoria |
| OVR | overall_rank | Ranking Geral |
| VRT | violent_rate | Taxa de Violência |
| RSK | risk_level | Nível de Risco |
| HSL | hotspot_level | Nível de Hotspot |
| HSD | hotspot_decile | Decil do Hotspot |
| YOY | yoy_growth | Crescimento Ano a Ano |
| YOV | yoy_violent_growth | Crescimento Violento YoY |
| TRD | trend | Tendência |
| STS | status | Status |
| PYC | prev_year_crimes | Crimes Ano Anterior |
| PYV | prev_year_violent | Violentos Ano Anterior |

---

## CTEs em consultas.sql

| Mnemônico | Nome SQL | Consulta |
|-----------|----------|----------|
| MST | monthly_stats | CTE 12 - Estatísticas Mensais |
| MAV | monthly_avg | CTE 12 - Média Mensal |
| CRK | crime_ranking | CTE 13 - Ranking de Crimes |
| VPR | victim_profile | CTE 14 - Perfil de Vítima |
| CLO | crime_locations | CTE 15 - Localizações |
| HCL | hotspot_classification | CTE 15 - Classificação Hotspots |
| YCR | yearly_crimes | CTE 16 - Crimes Anuais |
| YOY | year_over_year | CTE 16 - Comparação Anual |
| GCA | growth_calculation | CTE 16 - Cálculo Crescimento |

---

## Aliases em consultas.sql

| Mnemônico | Alias SQL | Tabela Original |
|-----------|-----------|-----------------|
| fc | fc | fato_crimes |
| da | da | dim_area |
| dct | dct | dim_crime_type |
| dd | dd | dim_date |
| dt | dt | dim_time |
| dv | dv | dim_victim |
| dw | dw | dim_weapon |
| dp | dp | dim_premise |
| ms | ms | monthly_stats (CTE) |
| ma | ma | monthly_avg (CTE) |

---

## Tipos de Dados (Data Types)

| Mnemônico | Tipo SQL | Descrição |
|-----------|----------|-----------|
| SRL | SERIAL | Auto-incremento |
| INT | INTEGER | Inteiro |
| BIG | BIGINT | Inteiro Grande |
| DEC | DECIMAL | Decimal |
| NUM | NUMERIC | Numérico |
| VAR | VARCHAR | Texto Variável |
| CHR | CHAR | Caractere Fixo |
| BOL | BOOLEAN | Booleano |
| DAT | DATE | Data |
| TIM | TIME | Hora |
| TSP | TIMESTAMP | Data e Hora |

---

## Funções SQL Usadas

| Mnemônico | Função SQL | Descrição |
|-----------|------------|-----------|
| CNT | COUNT(*) | Contagem |
| SUM | SUM() | Soma |
| AVG | AVG() | Média |
| RND | ROUND() | Arredondamento |
| CAS | CASE WHEN | Condicional |
| LAG | LAG() | Valor Anterior |
| RNK | RANK() | Ranking |
| ROW | ROW_NUMBER() | Número de Linha |
| NTL | NTILE() | Divisão em Grupos |
| PRC | PERCENTILE_CONT() | Percentil |
| OVR | OVER() | Janela |
| PTN | PARTITION BY | Particionamento |

---

## Exemplos de Uso

### Referência de Tabela
```sql
-- SELECT * FROM gold.fato_crimes fc
-- fc = alias para FCR (fato_crimes)
```

### Referência de Coluna
```sql
-- da.area_name → ARN (Area Name)
-- dd.year → YEA (Year)
-- fc.is_violent → ISV (Is Violent)
```

### Referência de Métrica
```sql
-- COUNT(*) as total_crimes → TCR
-- SUM(CASE WHEN fc.is_violent...) as violent_crimes → VCR
```

---

**Versão:** 2.0
**Data:** 2026-01-28
**Propósito:** Mnemônicos padronizados baseados em consultas.sql
**Schema:** gold
