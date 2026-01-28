# Modelagem de Dados - Camada GOLD (Data Warehouse)

**Projeto:** Crime Data Analytics - LAPD
**Arquitetura:** Medallion (Raw → Silver → Gold)
**Modelo:** Star Schema (Dimensional)
**Data:** 2026-01-28

---

## Modelo Entidade Relacionamento (ME-R)

### 1) Identificação das Entidades:

- FCR (fato_crimes)
- DDT (dim_date)
- DTM (dim_time)
- DAR (dim_area)
- DCT (dim_crime_type)
- DVC (dim_victim)

### 2) Descrição das Entidades

- FCR(<u>SKC</u>, NKC, SKD, SKH, SKA, SKT, SKV, LAT, LON, ISV, HSW, CSC)
- DDT(<u>SKD</u>, FDT, YEA, QTR, MON, MNM, WOY, DOM, DOW, DNM, ISW)
- DTM(<u>SKH</u>, HOU, PRD, ISR)
- DAR(<u>SKA</u>, ARC, ARN, REG)
- DCT(<u>SKT</u>, CRC, CRD, CAT, SVR, ISV, SVL)
- DVC(<u>SKV</u>, AGG, SEX, DSC)

### 3) Descrição dos Relacionamentos

**FCR - OCORRE_EM - DDT**
- Um FCR OCORRE EM uma DDT. Uma DDT pode estar associada a um ou muitos FCR.
- Cardinalidade: 1:N (lido como 1 DDT para N FCR)

**FCR - ACONTECE_EM - DTM**
- Um FCR ACONTECE EM uma DTM. Uma DTM pode estar associada a um ou muitos FCR.
- Cardinalidade: 1:N (lido como 1 DTM para N FCR)

**FCR - LOCALIZADO_EM - DAR**
- Um FCR está LOCALIZADO EM uma DAR. Uma DAR pode conter um ou muitos FCR.
- Cardinalidade: 1:N (lido como 1 DAR para N FCR)

**FCR - CLASSIFICADO_COMO - DCT**
- Um FCR é CLASSIFICADO COMO uma DCT. Uma DCT pode classificar um ou muitos FCR.
- Cardinalidade: 1:N (lido como 1 DCT para N FCR)

**FCR - TEM_VITIMA - DVC**
- Um FCR TEM VÍTIMA de perfil DVC. Uma DVC pode estar associada a um ou muitos FCR.
- Cardinalidade: 1:N (lido como 1 DVC para N FCR)

---

## Diagrama Entidade Relacionamento (DE-R)

```
                              ┌─────────────────┐
                              │      DDT        │
                              │─────────────────│
                              │ SKD (PK)        │
                              │ FDT, YEA, QTR   │
                              │ MON, MNM, WOY   │
                              │ DOM, DOW, DNM   │
                              │ ISW             │
                              └────────┬────────┘
                                       │
                                       │ (1,1)
                                       │
┌─────────────────┐           ┌────────▼────────┐           ┌─────────────────┐
│      DTM        │           │      FCR        │           │      DCT        │
│─────────────────│   (1,1)   │─────────────────│   (1,1)   │─────────────────│
│ SKH (PK)        │◄──────────│ SKC (PK)        │──────────►│ SKT (PK)        │
│ HOU, PRD        │           │ NKC             │           │ CRC, CRD        │
│ ISR             │  ACONTECE │ SKD, SKH (FK)   │CLASSIFICADO│ CAT, SVR        │
└─────────────────┘    _EM    │ SKA, SKT (FK)   │  _COMO    │ ISV, SVL        │
                      (1,n)   │ SKV (FK)        │   (1,n)   └─────────────────┘
                              │ LAT, LON        │
┌─────────────────┐           │ ISV, HSW, CSC   │           ┌─────────────────┐
│      DAR        │           └────────┬────────┘           │      DVC        │
│─────────────────│   (1,1)            │            (1,1)   │─────────────────│
│ SKA (PK)        │◄───────────────────┤───────────────────►│ SKV (PK)        │
│ ARC, ARN        │  LOCALIZADO        │        TEM_VITIMA  │ AGG, SEX, DSC   │
│ REG             │    _EM             │           (1,n)    └─────────────────┘
└─────────────────┘   (1,n)            │
                                       │
                                    OCORRE_EM
                                      (1,n)
```

---

## Diagrama Lógico de Dados (DLD)

```
┌─────────────────────────────┐                              ┌─────────────────────────────┐
│          DIM_DATE           │                              │       DIM_CRIME_TYPE        │
├─────────────────────────────┤                              ├─────────────────────────────┤
│ ↑ SKD: SERIAL               │                              │ ↑ SKT: SERIAL               │
│ ○ FDT: DATE                 │                              │ ○ CRC: INTEGER              │
│ ○ YEA: INTEGER              │                              │ ○ CRD: VARCHAR(255)         │
│ ○ QTR: INTEGER              │         (1,1)                │ ○ CAT: VARCHAR(50)          │
│ ○ MON: INTEGER              │◄────────────────────┐        │ ○ SVR: VARCHAR(20)          │
│ ○ MNM: VARCHAR(20)          │                     │        │ ○ ISV: BOOLEAN              │
│ ○ WOY: INTEGER              │                     │        │ ○ SVL: INTEGER              │
│ ○ DOM: INTEGER              │                     │ (1,1)  └──────────────┬──────────────┘
│ ○ DOW: INTEGER              │                     │                       │
│ ○ DNM: VARCHAR(20)          │                     │                       │
│ ○ ISW: BOOLEAN              │      ┌──────────────┴───────────────┐       │
└─────────────────────────────┘      │         FATO_CRIMES          │       │
                                     ├──────────────────────────────┤       │
┌─────────────────────────────┐      │ ↑ SKC: SERIAL                │       │
│          DIM_TIME           │      │ ○ NKC: BIGINT                │       │
├─────────────────────────────┤      │ ↓ FK_DDT_SKD: INTEGER        │       │
│ ↑ SKH: SERIAL               │(1,1) │ ↓ FK_DTM_SKH: INTEGER        │(1,1)  │
│ ○ HOU: INTEGER              │◄─────│ ↓ FK_DAR_SKA: INTEGER        │───────┘
│ ○ PRD: VARCHAR(20)          │      │ ↓ FK_DCT_SKT: INTEGER        │
│ ○ ISR: BOOLEAN              │      │ ↓ FK_DVC_SKV: INTEGER        │
└─────────────────────────────┘      │ ○ LAT: DECIMAL(10,6)         │
                                     │ ○ LON: DECIMAL(10,6)         │
┌─────────────────────────────┐      │ ○ ISV: BOOLEAN               │       ┌─────────────────────────────┐
│          DIM_AREA           │      │ ○ HSW: BOOLEAN               │       │        DIM_VICTIM           │
├─────────────────────────────┤      │ ○ CSC: BOOLEAN               │       ├─────────────────────────────┤
│ ↑ SKA: SERIAL               │(1,1) └──────────────┬───────────────┘(1,1)  │ ↑ SKV: SERIAL               │
│ ○ ARC: INTEGER              │◄────────────────────┴───────────────────────│ ○ AGG: VARCHAR(20)          │
│ ○ ARN: VARCHAR(50)          │                                             │ ○ SEX: CHAR(1)              │
│ ○ REG: VARCHAR(50)          │                                             │ ○ DSC: VARCHAR(50)          │
└─────────────────────────────┘                                             └─────────────────────────────┘

Legenda:
  ↑  Chave Primária (PK)
  ↓  Chave Estrangeira (FK)
  ○  Atributo comum
```

---

## Dicionário de Dados

### Entidade: FCR (fato_crimes)

**Descrição:** Define os dados de cada ocorrência criminal registrada pelo LAPD

| Atributo | Tipo de dado | Descrição |
|----------|--------------|-----------|
| <u>SKC</u> | SERIAL | Identificador único do crime (Surrogate Key) |
| NKC | BIGINT | Identificador original do crime (Natural Key) |
| SKD | INTEGER | Identificador único da data (FK → DDT) |
| SKH | INTEGER | Identificador único do horário (FK → DTM) |
| SKA | INTEGER | Identificador único da área (FK → DAR) |
| SKT | INTEGER | Identificador único do tipo de crime (FK → DCT) |
| SKV | INTEGER | Identificador único da vítima (FK → DVC) |
| LAT | DECIMAL(10,6) | Latitude da localização do crime |
| LON | DECIMAL(10,6) | Longitude da localização do crime |
| ISV | BOOLEAN | Indica se é crime violento |
| HSW | BOOLEAN | Indica se houve uso de arma |
| CSC | BOOLEAN | Indica se o caso foi encerrado |

---

### Entidade: DDT (dim_date)

**Descrição:** Define os dados temporais por data para análise de tendências

| Atributo | Tipo de dado | Descrição |
|----------|--------------|-----------|
| <u>SKD</u> | SERIAL | Identificador único da data (Surrogate Key) |
| FDT | DATE | Data completa da ocorrência |
| YEA | INTEGER | Ano (2020-2025) |
| QTR | INTEGER | Trimestre (1-4) |
| MON | INTEGER | Mês (1-12) |
| MNM | VARCHAR(20) | Nome do mês |
| WOY | INTEGER | Semana do ano |
| DOM | INTEGER | Dia do mês |
| DOW | INTEGER | Dia da semana (0=Domingo, 6=Sábado) |
| DNM | VARCHAR(20) | Nome do dia |
| ISW | BOOLEAN | Indica se é fim de semana |

---

### Entidade: DTM (dim_time)

**Descrição:** Define os dados temporais por hora para análise de padrões diários

| Atributo | Tipo de dado | Descrição |
|----------|--------------|-----------|
| <u>SKH</u> | SERIAL | Identificador único do horário (Surrogate Key) |
| HOU | INTEGER | Hora do dia (0-23) |
| PRD | VARCHAR(20) | Período do dia (Madrugada, Manhã, Tarde, Noite) |
| ISR | BOOLEAN | Indica se é horário de pico (rush hour) |

---

### Entidade: DAR (dim_area)

**Descrição:** Define os dados geográficos das 21 áreas policiais do LAPD

| Atributo | Tipo de dado | Descrição |
|----------|--------------|-----------|
| <u>SKA</u> | SERIAL | Identificador único da área (Surrogate Key) |
| ARC | INTEGER | Código da área LAPD |
| ARN | VARCHAR(50) | Nome da área policial |
| REG | VARCHAR(50) | Região (North, South, Central, West) |

---

### Entidade: DCT (dim_crime_type)

**Descrição:** Define os dados de classificação dos 108 tipos de crime

| Atributo | Tipo de dado | Descrição |
|----------|--------------|-----------|
| <u>SKT</u> | SERIAL | Identificador único do tipo (Surrogate Key) |
| CRC | INTEGER | Código do crime |
| CRD | VARCHAR(255) | Descrição do crime |
| CAT | VARCHAR(50) | Categoria (Violent, Property, Other) |
| SVR | VARCHAR(20) | Severidade |
| ISV | BOOLEAN | Indica se é crime violento |
| SVL | INTEGER | Nível de severidade (1-3) |

---

### Entidade: DVC (dim_victim)

**Descrição:** Define os dados demográficos do perfil das vítimas

| Atributo | Tipo de dado | Descrição |
|----------|--------------|-----------|
| <u>SKV</u> | SERIAL | Identificador único do perfil (Surrogate Key) |
| AGG | VARCHAR(20) | Faixa etária (0-17, 18-24, 25-34, etc.) |
| SEX | CHAR(1) | Sexo (M=Masculino, F=Feminino, X=Outro) |
| DSC | VARCHAR(50) | Descendência/Etnia |

---

## Dicionário de Mnemônicos

### Tabelas

| Mnemônico | Nome Completo | Descrição |
|-----------|---------------|-----------|
| FCR | fato_crimes | Tabela fato de crimes |
| DDT | dim_date | Dimensão de data |
| DTM | dim_time | Dimensão de tempo/hora |
| DAR | dim_area | Dimensão de área geográfica |
| DCT | dim_crime_type | Dimensão de tipo de crime |
| DVC | dim_victim | Dimensão de vítima |

### Chaves

| Mnemônico | Nome Completo | Descrição |
|-----------|---------------|-----------|
| SKC | sk_crime | Surrogate Key do crime |
| SKD | sk_date | Surrogate Key da data |
| SKH | sk_time | Surrogate Key do horário |
| SKA | sk_area | Surrogate Key da área |
| SKT | sk_crime_type | Surrogate Key do tipo de crime |
| SKV | sk_victim | Surrogate Key da vítima |
| NKC | nk_crime_id | Natural Key do crime |

### Atributos

| Mnemônico | Nome Completo | Descrição |
|-----------|---------------|-----------|
| ARC | area_code | Código da área |
| ARN | area_name | Nome da área |
| REG | region | Região |
| LAT | latitude | Latitude |
| LON | longitude | Longitude |
| CRC | crime_code | Código do crime |
| CRD | crime_description | Descrição do crime |
| CAT | crime_category | Categoria do crime |
| SVR | severity | Severidade |
| SVL | severity_level | Nível de severidade |
| FDT | full_date | Data completa |
| YEA | year | Ano |
| QTR | quarter | Trimestre |
| MON | month | Mês |
| MNM | month_name | Nome do mês |
| WOY | week_of_year | Semana do ano |
| DOM | day_of_month | Dia do mês |
| DOW | day_of_week | Dia da semana |
| DNM | day_name | Nome do dia |
| HOU | hour | Hora |
| PRD | period_of_day | Período do dia |
| AGG | age_group | Faixa etária |
| SEX | sex | Sexo |
| DSC | descent | Descendência |

### Flags Booleanas

| Mnemônico | Nome Completo | Descrição |
|-----------|---------------|-----------|
| ISV | is_violent | É crime violento? |
| ISW | is_weekend | É fim de semana? |
| ISR | is_rush_hour | É horário de pico? |
| HSW | has_weapon | Houve uso de arma? |
| CSC | case_closed | Caso encerrado? |

---

**Documento gerado em:** 2026-01-28
**Versão:** 3.0
**Referência:** [mnemonics.md](mnemonics.md)
