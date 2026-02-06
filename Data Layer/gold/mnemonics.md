# Mnemônicos - Gold Layer
## Crime Data Analytics - Data Warehouse

---

## Padrão de Nomenclatura

Os mnemônicos seguem o padrão de **3 letras por palavra**, separadas por sublinhado.

---

## Tabelas (Tables)

| Mnemônico | Nome SQL | Descrição |
|-----------|----------|-----------|
| fat_crm | fato_crimes | Tabela Fato de Crimes |
| dim_are | dim_area | Dimensão Área |
| dim_crm_typ | dim_crime_type | Dimensão Tipo de Crime |
| dim_wpn | dim_weapon | Dimensão Arma |
| dim_prm | dim_premise | Dimensão Local |
| dim_dat | dim_date | Dimensão Data |
| dim_tim | dim_time | Dimensão Tempo |
| dim_vct | dim_victim | Dimensão Vítima |

---

## Chaves (Keys)

| Mnemônico | Nome SQL | Descrição |
|-----------|----------|-----------|
| sur_key_are | sk_area | Surrogate Key Área |
| sur_key_crm | sk_crime | Surrogate Key Crime |
| sur_key_typ | sk_crime_type | Surrogate Key Tipo Crime |
| sur_key_dat | sk_date | Surrogate Key Data |
| sur_key_tim | sk_time | Surrogate Key Hora |
| sur_key_vct | sk_victim | Surrogate Key Vítima |
| sur_key_wpn | sk_weapon | Surrogate Key Arma |
| sur_key_prm | sk_premise | Surrogate Key Local |
| nat_key_crm | nk_crime_id | Natural Key Crime |

---

## Atributos Geográficos (Geographic)

| Mnemônico | Nome SQL | Descrição |
|-----------|----------|-----------|
| are_cod | area_code | Código da Área |
| are_nam | area_name | Nome da Área |
| reg_ion | region | Região |
| lat_ude | latitude | Latitude |
| lon_gde | longitude | Longitude |

---

## Atributos de Crime (Crime)

| Mnemônico | Nome SQL | Descrição |
|-----------|----------|-----------|
| crm_cod | crime_code | Código do Crime |
| crm_dsc | crime_description | Descrição do Crime |
| crm_cat | crime_category | Categoria do Crime |
| sev_lvl | severity_level | Nível de Severidade |
| is_vio | is_violent | É Violento |

---

## Atributos Temporais (Temporal)

| Mnemônico | Nome SQL | Descrição |
|-----------|----------|-----------|
| ful_dat | full_date | Data Completa |
| yea_num | year | Ano |
| qtr_num | quarter | Trimestre |
| mon_num | month | Mês |
| mon_nam | month_name | Nome do Mês |
| wek_yea | week_of_year | Semana do Ano |
| day_mon | day_of_month | Dia do Mês |
| day_wek | day_of_week | Dia da Semana |
| day_nam | day_name | Nome do Dia |
| hou_num | hour | Hora |
| per_day | period_of_day | Período do Dia |
| is_wkd | is_weekend | É Fim de Semana |
| is_hol | is_holiday | É Feriado |
| is_rsh | is_rush_hour | É Horário de Pico |

---

## Atributos de Vítima (Victim)

| Mnemônico | Nome SQL | Descrição |
|-----------|----------|-----------|
| age_grp | age_group | Faixa Etária |
| sex_typ | sex | Sexo |
| dsc_eth | descent | Descendência/Etnia |

---

## Atributos de Arma (Weapon)

| Mnemônico | Nome SQL | Descrição |
|-----------|----------|-----------|
| wpn_cod | weapon_code | Código da Arma |
| wpn_dsc | weapon_description | Descrição da Arma |
| wpn_cat | weapon_category | Categoria da Arma |
| lth_lvl | lethality_level | Nível de Letalidade |

---

## Atributos de Local (Premise)

| Mnemônico | Nome SQL | Descrição |
|-----------|----------|-----------|
| prm_cod | premise_code | Código do Local |
| prm_dsc | premise_description | Descrição do Local |
| prm_cat | premise_category | Categoria do Local |
| is_pub | is_public | É Público |

---

## Métricas e Agregações (Metrics)

| Mnemônico | Nome SQL | Descrição |
|-----------|----------|-----------|
| tot_crm | total_crimes | Total de Crimes |
| vio_crm | violent_crimes | Crimes Violentos |
| prp_crm | property_crimes | Crimes Patrimoniais |
| tot_occ | total_occurrences | Total de Ocorrências |
| tot_uso | total_uso | Total de Uso |
| tot_vct | total_vitimas | Total de Vítimas |
| pct_num | percentual | Percentual |
| pct_vio | pct_violent | Percentual Violento |
| pct_dif_avg | pct_diff_from_avg | Diferença Percentual da Média |
| avg_mon_crm | avg_monthly_crimes | Média Mensal de Crimes |
| crm_cnt | crime_count | Contagem de Crimes |

---

## Campos Calculados (CTEs)

| Mnemônico | Nome SQL | Descrição |
|-----------|----------|-----------|
| rnk_cat | rank_in_category | Ranking na Categoria |
| ovr_rnk | overall_rank | Ranking Geral |
| vio_rat | violent_rate | Taxa de Violência |
| rsk_lvl | risk_level | Nível de Risco |
| hsp_lvl | hotspot_level | Nível de Hotspot |
| hsp_dcl | hotspot_decile | Decil do Hotspot |
| yoy_grt | yoy_growth | Crescimento Ano a Ano |
| yoy_vio_grt | yoy_violent_growth | Crescimento Violento YoY |
| trd_sts | trend | Tendência |
| sta_tus | status | Status |
| prv_yea_crm | prev_year_crimes | Crimes Ano Anterior |
| prv_yea_vio | prev_year_violent | Violentos Ano Anterior |

---

## CTEs em consultas.sql

| Mnemônico | Nome SQL | Consulta |
|-----------|----------|----------|
| mon_sta | monthly_stats | CTE 12 - Estatísticas Mensais |
| mon_avg | monthly_avg | CTE 12 - Média Mensal |
| crm_rnk | crime_ranking | CTE 13 - Ranking de Crimes |
| vct_prf | victim_profile | CTE 14 - Perfil de Vítima |
| crm_loc | crime_locations | CTE 15 - Localizações |
| hsp_cls | hotspot_classification | CTE 15 - Classificação Hotspots |
| yea_crm | yearly_crimes | CTE 16 - Crimes Anuais |
| yea_ovr_yea | year_over_year | CTE 16 - Comparação Anual |
| grt_cal | growth_calculation | CTE 16 - Cálculo Crescimento |

---

## Aliases em consultas.sql

| Mnemônico | Alias SQL | Tabela Original |
|-----------|-----------|-----------------|
| fat_crm | fc | fato_crimes |
| dim_are | da | dim_area |
| dim_crm_typ | dct | dim_crime_type |
| dim_dat | dd | dim_date |
| dim_tim | dt | dim_time |
| dim_vct | dv | dim_victim |
| dim_wpn | dw | dim_weapon |
| dim_prm | dp | dim_premise |
| mon_sta | ms | monthly_stats (CTE) |
| mon_avg | ma | monthly_avg (CTE) |

---

## Tipos de Dados (Data Types)

| Mnemônico | Tipo SQL | Descrição |
|-----------|----------|-----------|
| ser_ial | SERIAL | Auto-incremento |
| int_ger | INTEGER | Inteiro |
| big_int | BIGINT | Inteiro Grande |
| dec_mal | DECIMAL | Decimal |
| num_ric | NUMERIC | Numérico |
| var_chr | VARCHAR | Texto Variável |
| chr_fix | CHAR | Caractere Fixo |
| boo_lan | BOOLEAN | Booleano |
| dat_ful | DATE | Data |
| tim_hor | TIME | Hora |
| tim_stp | TIMESTAMP | Data e Hora |

---

## Funções SQL Usadas

| Mnemônico | Função SQL | Descrição |
|-----------|------------|-----------|
| cnt_all | COUNT(*) | Contagem |
| sum_val | SUM() | Soma |
| avg_val | AVG() | Média |
| rnd_val | ROUND() | Arredondamento |
| cas_whn | CASE WHEN | Condicional |
| lag_val | LAG() | Valor Anterior |
| rnk_ord | RANK() | Ranking |
| row_num | ROW_NUMBER() | Número de Linha |
| ntl_grp | NTILE() | Divisão em Grupos |
| prc_cnt | PERCENTILE_CONT() | Percentil |
| ovr_win | OVER() | Janela |
| prt_by | PARTITION BY | Particionamento |

---

## Exemplos de Uso

### Referência de Tabela
```sql
-- SELECT * FROM gold.fato_crimes fc
-- fc = alias para fat_crm (fato_crimes)
```

### Referência de Coluna
```sql
-- da.area_name → are_nam (Area Name)
-- dd.year → yea_num (Year)
-- fc.is_violent → is_vio (Is Violent)
```

### Referência de Métrica
```sql
-- COUNT(*) as total_crimes → tot_crm
-- SUM(CASE WHEN fc.is_violent...) as violent_crimes → vio_crm
```

---

**Versão:** 3.0
**Data:** 2026-02-06
**Propósito:** Mnemônicos padronizados com 3 letras por palavra
**Schema:** gold
