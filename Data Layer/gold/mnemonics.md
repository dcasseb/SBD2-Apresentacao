# Mnemonics - Gold Layer
## Crime Data Analytics - Data Warehouse

---

## Tables (Tabelas)

| Acronym | Description |
|---------|-------------|
| DIM | Dimension |
| FCT | Fact |
| AGG | Aggregation |
| ARA | Area |
| CRM | Crime |
| WPN | Weapon |
| PRM | Premise |
| DAT | Date |
| TIM | Time |
| VCT | Victim |
| HTS | Hotspots |
| PRD | Period |

---

## Keys (Chaves)

| Acronym | Description |
|---------|-------------|
| SKA | Surrogate Key Area |
| SKC | Surrogate Key Crime |
| SKD | Surrogate Key Date |
| SKP | Surrogate Key Premise |
| SKT | Surrogate Key Time |
| SKV | Surrogate Key Victim |
| SKW | Surrogate Key Weapon |
| NKC | Natural Key Crime |
| PFK | Primary Foreign Key |

---

## Attributes - Geographic (Atributos Geográficos)

| Acronym | Description |
|---------|-------------|
| ARC | Area Code |
| ARN | Area Name |
| REG | Region |
| LAT | Latitude |
| LON | Longitude |
| GRD | Grid |
| LOC | Location |
| DST | District |
| GEO | Geographic |

---

## Attributes - Crime (Atributos de Crime)

| Acronym | Description |
|---------|-------------|
| CRC | Crime Code |
| CRD | Crime Description |
| CAT | Category |
| SVR | Severity |
| VIO | Violent |
| LVL | Level |
| STS | Status |
| CLS | Closed |
| TYP | Type |

---

## Attributes - Temporal (Atributos Temporais)

| Acronym | Description |
|---------|-------------|
| YEA | Year |
| QTR | Quarter |
| MON | Month |
| WEK | Week |
| DAY | Day |
| HOU | Hour |
| MIN | Minute |
| PRD | Period |
| WKD | Weekday |
| WKN | Weekend |
| HOL | Holiday |
| RSH | Rush Hour |
| FDT | Full Date |
| FTM | Full Time |
| DOM | Day of Month |
| DOW | Day of Week |
| WOY | Week of Year |
| MNM | Month Name |
| DNM | Day Name |

---

## Attributes - Victim (Atributos de Vítima)

| Acronym | Description |
|---------|-------------|
| AGE | Age |
| AGG | Age Group |
| SEX | Sex |
| DSC | Descent |
| DSD | Descent Description |
| DEM | Demographic |
| AVA | Average Victim Age |

---

## Attributes - Weapon (Atributos de Arma)

| Acronym | Description |
|---------|-------------|
| WPC | Weapon Code |
| WPD | Weapon Description |
| WPC | Weapon Category |
| LTH | Lethality |
| FRM | Firearm |
| BLD | Blade |
| BLN | Blunt |
| PHY | Physical |

---

## Attributes - Premise (Atributos de Local)

| Acronym | Description |
|---------|-------------|
| PMC | Premise Code |
| PMD | Premise Description |
| PMC | Premise Category |
| PUB | Public |
| RSD | Residential |
| COM | Commercial |
| OTH | Other |

---

## Measures (Medidas)

| Acronym | Description |
|---------|-------------|
| TOT | Total |
| CNT | Count |
| SUM | Sum |
| AVG | Average |
| MIN | Minimum |
| MAX | Maximum |
| PCT | Percentage |
| RAT | Rate |

---

## Crime Metrics (Métricas de Crime)

| Acronym | Description |
|---------|-------------|
| TCR | Total Crimes |
| VCR | Violent Crimes |
| PCR | Property Crimes |
| WCR | Weapon Crimes |
| CCR | Closed Cases |
| WDC | Weekday Crimes |
| WNC | Weekend Crimes |
| UTC | Unique Types Count |

---

## Boolean Flags (Flags Booleanas)

| Acronym | Description |
|---------|-------------|
| ISV | Is Violent |
| ISW | Is Weekend |
| ISH | Is Holiday |
| ISR | Is Rush Hour |
| ISP | Is Public |
| ISC | Is Closed |
| HSW | Has Weapon |

---

## Common Terms (Termos Comuns)

| Acronym | Description |
|---------|-------------|
| DWH | Data Warehouse |
| ETL | Extract Transform Load |
| STR | Star Schema |
| SNF | Snowflake Schema |
| OBT | One Big Table |
| SCD | Slowly Changing Dimension |
| RPT | Report |
| DSH | Dashboard |
| KPI | Key Performance Indicator |
| BI  | Business Intelligence |
| DQL | Data Quality Level |

---

## Data Types (Tipos de Dados)

| Acronym | Description |
|---------|-------------|
| INT | Integer |
| DEC | Decimal |
| VAR | Varchar |
| CHR | Char |
| BOL | Boolean |
| DAT | Date |
| TSP | Timestamp |
| TIM | Time |
| SRL | Serial |

---

## Operations (Operações)

| Acronym | Description |
|---------|-------------|
| SEL | Select |
| INS | Insert |
| UPD | Update |
| DEL | Delete |
| JON | Join |
| GRP | Group By |
| ORD | Order By |
| FLT | Filter |
| AGR | Aggregate |
| TRN | Transform |
| LDG | Loading |
| EXT | Extract |

---

## Schema Objects (Objetos de Schema)

| Acronym | Description |
|---------|-------------|
| TBL | Table |
| VEW | View |
| IDX | Index |
| SEQ | Sequence |
| CON | Constraint |
| FKY | Foreign Key |
| PKY | Primary Key |
| UNQ | Unique |
| CHK | Check |
| DFT | Default |

---

## Analysis Areas (Áreas de Análise)

| Acronym | Description |
|---------|-------------|
| TMP | Temporal Analysis |
| GEO | Geographic Analysis |
| DEM | Demographic Analysis |
| TRN | Trend Analysis |
| PTN | Pattern Analysis |
| COR | Correlation Analysis |
| SGM | Segmentation |
| CLF | Classification |
| PRD | Prediction |

---

## Specific Tables Reference

### Dimensions
| Acronym | Full Table Name |
|---------|-----------------|
| DAR | dim_area |
| DCT | dim_crime_type |
| DWP | dim_weapon |
| DPR | dim_premise |
| DDT | dim_date |
| DTM | dim_time |
| DVC | dim_victim |

### Fact Tables
| Acronym | Full Table Name |
|---------|-----------------|
| FCR | fato_crimes |

### Aggregations
| Acronym | Full Table Name |
|---------|-----------------|
| CAP | agg_crimes_area_period |
| CTY | agg_crimes_type_year |
| CHT | agg_crime_hotspots |

---

## Usage Examples

### Table Reference
```sql
-- Instead of: SELECT * FROM gold.dim_area
-- Reference: DAR = dim_area
```

### Column Reference
```sql
-- SKA = Surrogate Key Area (sk_area)
-- ARC = Area Code (area_code)
-- ARN = Area Name (area_name)
```

### Measure Reference
```sql
-- TCR = Total Crimes
-- VCR = Violent Crimes
-- AVA = Average Victim Age
```

---

**Version:** 1.0
**Date:** 2026-01-26
**Purpose:** Standardized 3-letter mnemonics for Gold layer documentation
**Schema:** gold
