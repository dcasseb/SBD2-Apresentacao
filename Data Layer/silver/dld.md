# ME-R

DATA_SILVER(crime_id, date_reported, date_occurred, time_occurred, hour, day_of_week,
day_name, period_of_day, area_code, area_name, district_code, crime_severity,
crime_code, crime_description, crime_category, victim_age, victim_age_group,
victim_sex, victim_sex_desc, victim_descent, victim_descent_desc, premise_code,
premise_description, premise_category, weapon_code, weapon_description, weapon_category,
is_violent, has_weapon, status_code, status_description, case_closed, latitude,
longitude, location, year, month, quarter, collected_at)

# DLD

## Visão Geral
A camada **Silver** contém dados limpos, padronizados e enriquecidos para análise. Este DLD descreve o **schema final** da tabela `data_silver.csv`.

- **Origem:** `Data Layer/raw/data_raw.csv`
- **Destino:** `Data Layer/silver/data_silver.csv`
- **Objetivo:** Padronização, validação e criação de atributos derivados para análise exploratória e geração da Gold.

---

## Dicionário de Dados (Schema)

| Coluna | Tipo | Descrição | Regras/Observações |
|---|---|---|---|
| `crime_id` | INTEGER | Identificador único do crime (DR_NO) | Deve ser único e não nulo |
| `date_reported` | DATETIME | Data de reporte | Conversão para datetime |
| `date_occurred` | DATETIME | Data de ocorrência | Conversão para datetime |
| `time_occurred` | INTEGER | Hora da ocorrência em formato HHMM | Ex.: 1345 |
| `hour` | INTEGER | Hora da ocorrência (0–23) | Derivado de `time_occurred` |
| `day_of_week` | INTEGER | Dia da semana (0=Seg … 6=Dom) | Derivado de `date_occurred` |
| `day_name` | STRING | Nome do dia da semana | Derivado de `date_occurred` |
| `period_of_day` | STRING | Período do dia (Madrugada/Manhã/Tarde/Noite) | Derivado de `hour` |
| `area_code` | INTEGER | Código da área LAPD | Domínio conhecido |
| `area_name` | STRING | Nome da área LAPD | Normalizado |
| `district_code` | INTEGER | Código do distrito | Original do dataset |
| `crime_severity` | STRING | Gravidade do crime | Ex.: Serious/Minor |
| `crime_code` | INTEGER | Código do crime | Original do dataset |
| `crime_description` | STRING | Descrição do crime | Normalizada |
| `crime_category` | STRING | Categoria do crime | Derivada/agrupada |
| `victim_age` | INTEGER | Idade da vítima | Valores inválidos removidos/ajustados |
| `victim_age_group` | STRING | Faixa etária da vítima | Derivada |
| `victim_sex` | CHAR | Sexo da vítima (M/F/X) | Domínio conhecido |
| `victim_sex_desc` | STRING | Sexo (descrição) | Derivada |
| `victim_descent` | CHAR | Descendência (código) | Domínio conhecido |
| `victim_descent_desc` | STRING | Descendência (descrição) | Derivada |
| `premise_code` | INTEGER | Código do local do crime | Original do dataset |
| `premise_description` | STRING | Descrição do local | Normalizada |
| `premise_category` | STRING | Categoria do local | Derivada |
| `weapon_code` | INTEGER | Código da arma | Original do dataset |
| `weapon_description` | STRING | Descrição da arma | Normalizada |
| `weapon_category` | STRING | Categoria da arma | Derivada |
| `is_violent` | BOOLEAN | Flag de crime violento | Derivada |
| `has_weapon` | BOOLEAN | Flag de uso de arma | Derivada |
| `status_code` | STRING | Status do caso | Original do dataset |
| `status_description` | STRING | Descrição do status | Normalizada |
| `case_closed` | BOOLEAN | Caso encerrado | Derivada |
| `latitude` | FLOAT | Latitude | Coordenadas válidas |
| `longitude` | FLOAT | Longitude | Coordenadas válidas |
| `location` | STRING | Endereço/Localização textual | Original do dataset |
| `year` | INTEGER | Ano da ocorrência | Derivado de `date_occurred` |
| `month` | INTEGER | Mês da ocorrência | Derivado de `date_occurred` |
| `quarter` | INTEGER | Trimestre da ocorrência | Derivado de `date_occurred` |
| `collected_at` | DATETIME | Timestamp da coleta/ETL | Gerado no pipeline |

---

## Regras de Qualidade (Silver)

- `crime_id` deve ser único e não nulo.
- `date_occurred` e `date_reported` devem estar em formato datetime.
- `hour` deve estar no intervalo **0–23**.
- `victim_age` deve estar em intervalo plausível (ex.: 0–100).
- `latitude` e `longitude` devem estar dentro dos limites aproximados de LA.
- Campos categóricos devem estar normalizados (ex.: `crime_category`, `weapon_category`).

---

## Campos Derivados

- `hour`, `day_of_week`, `day_name`, `period_of_day`
- `victim_age_group`
- `crime_category`, `crime_severity`
- `premise_category`, `weapon_category`
- `is_violent`, `has_weapon`, `case_closed`
- `year`, `month`, `quarter`

---

## Uso Principal

- Base para análises exploratórias (notebooks de Silver).
- Fonte para construção da camada Gold (dimensões e fato).