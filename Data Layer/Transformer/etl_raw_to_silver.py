#!/usr/bin/env python
# coding: utf-8

# # ETL Raw → Silver
# ## Crime Data Pipeline
# 
# Pipeline de transformação de dados brutos para camada Silver.
# 
# **Objetivo**: Transformar dados da camada Raw para Silver com limpeza, validação e feature engineering.
# 
# **Entrada**: `Data Layer/raw/data_raw.csv`  
# **Saída**: PostgreSQL (`schema silver`, tabela `crimes`)

# In[1]:


# Configuração inicial
import os
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
from sqlalchemy import create_engine

def find_project_root(start: Path) -> Path:
    for p in [start, *start.parents]:
        if (p / 'Data Layer').exists():
            return p
    return start

# Configurar raiz do projeto
PROJECT_ROOT = find_project_root(Path.cwd())
RAW_PATH = PROJECT_ROOT / 'Data Layer' / 'raw' / 'data_raw.csv'
DDL_PATH = PROJECT_ROOT / 'Data Layer' / 'silver' / 'ddl.sql'

# Configuração PostgreSQL
POSTGRES_DB = os.getenv("POSTGRES_DB", "crime_data")
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
DB_URL = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

print(f"📁 Projeto: {PROJECT_ROOT}")
print(f"📥 Raw: {RAW_PATH}")
print(f"🧱 DDL: {DDL_PATH}")
print(f"🗄️  DB: {POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}")


# In[ ]:


# Instalar dependências (se necessário)
# get_ipython().run_line_magic('pip', 'install pandas numpy sqlalchemy psycopg2-binary')  # Commented out - packages already installed


# In[ ]:


# Inicializar conexão e aplicar DDL (PostgreSQL)
engine = create_engine(DB_URL)

with engine.begin() as conn:
    ddl_sql = DDL_PATH.read_text(encoding="utf-8")
    for stmt in ddl_sql.split(";"):
        stmt = stmt.strip()
        if stmt:
            conn.exec_driver_sql(stmt)

print("✅ Conexão Postgre pronta e DDL aplicado")


# In[ ]:


# Carregar dados Raw
df = pd.read_csv(RAW_PATH)
print(f"✅ Dados Raw carregados: {len(df):,} registros")
print(f"📋 Colunas: {len(df.columns)}")
df.head(3)


# In[ ]:


## Etapa 1: Limpeza de Dados


# In[ ]:


# Limpeza de dados
print("🧹 Aplicando limpeza...")

df_clean = df.copy()

# 1. Remover duplicados
df_clean = df_clean.drop_duplicates(subset=['DR_NO'])
print(f"   Após remover duplicados: {len(df_clean):,}")

# 2. Remover nulos críticos
df_clean = df_clean.dropna(subset=['DR_NO', 'DATE OCC', 'Crm Cd'])
print(f"   Após remover nulos críticos: {len(df_clean):,}")

# 3. Remover coordenadas inválidas (0,0)
df_clean = df_clean[(df_clean['LAT'] != 0) & (df_clean['LON'] != 0)]
print(f"   Após remover coordenadas inválidas: {len(df_clean):,}")

# 4. Remover idades inválidas
df_clean = df_clean[(df_clean['Vict Age'] >= 0) & (df_clean['Vict Age'] <= 120)]
print(f"   Após remover idades inválidas: {len(df_clean):,}")

# 5. Remover registros sem dados essenciais
df_clean = df_clean.dropna(subset=['Crm Cd Desc', 'AREA NAME', 'Status'])
print(f"   Após remover campos essenciais nulos: {len(df_clean):,}")

# 6. Filtro de vítima identificada
df_clean = df_clean[(df_clean['Vict Age'] > 0) | (df_clean['Vict Sex'].isin(['M', 'F']))]
print(f"   Após filtro de vítima identificada: {len(df_clean):,}")

# 7. Remover localizações inválidas
df_clean = df_clean[~df_clean['LOCATION'].isna()]
df_clean = df_clean[~df_clean['Premis Desc'].isna()]
print(f"   Após filtro de localização: {len(df_clean):,}")

print(f"\n✅ Limpeza concluída: {len(df):,} → {len(df_clean):,} ({100*len(df_clean)/len(df):.1f}%)")


# In[ ]:


## Etapa 2: Transformações e Feature Engineering


# In[ ]:


# Mapeamentos
descent_map = {
    'A': 'Other Asian', 'B': 'Black', 'C': 'Chinese', 'D': 'Cambodian', 
    'F': 'Filipino', 'G': 'Guamanian', 'H': 'Hispanic/Latino', 'I': 'American Indian', 
    'J': 'Japanese', 'K': 'Korean', 'L': 'Laotian', 'O': 'Other', 
    'P': 'Pacific Islander', 'S': 'Samoan', 'U': 'Hawaiian', 'V': 'Vietnamese', 
    'W': 'White', 'X': 'Unknown', 'Z': 'Asian Indian', '-': 'Unknown'
}

sex_map = {'M': 'Male', 'F': 'Female', 'X': 'Unknown', 'H': 'Unknown', '-': 'Unknown'}

def get_period(hour):
    if 5 <= hour < 12: return 'Morning'
    elif 12 <= hour < 17: return 'Afternoon'
    elif 17 <= hour < 21: return 'Evening'
    else: return 'Night'

def get_crime_category(desc):
    desc = str(desc).upper()
    if any(x in desc for x in ['HOMICIDE', 'RAPE', 'ROBBERY', 'ASSAULT', 'KIDNAP', 'BATTERY']): 
        return 'Violent Crime'
    elif any(x in desc for x in ['THEFT', 'BURGLARY', 'STOLEN', 'VEHICLE', 'SHOPLIFTING']): 
        return 'Property Crime'
    elif any(x in desc for x in ['VANDALISM', 'TRESPASS', 'DISTURBING']): 
        return 'Quality of Life'
    else: 
        return 'Other Crime'

def get_age_group(age):
    try:
        age = int(age)
        if age <= 0: return 'Unknown'
        elif age < 18: return '0-17'
        elif age < 26: return '18-25'
        elif age < 36: return '26-35'
        elif age < 51: return '36-50'
        elif age < 66: return '51-65'
        else: return '65+'
    except: 
        return 'Unknown'

def get_premise_category(desc):
    desc = str(desc).upper()
    if any(x in desc for x in ['DWELLING', 'RESIDENCE', 'HOUSE', 'APARTMENT', 'CONDOMINIUM']): 
        return 'Residential'
    elif any(x in desc for x in ['STREET', 'SIDEWALK', 'PARKING', 'ALLEY', 'PARK', 'BEACH']): 
        return 'Public'
    elif any(x in desc for x in ['STORE', 'SHOP', 'RESTAURANT', 'COMMERCIAL', 'OFFICE', 'BANK', 'MARKET']): 
        return 'Commercial'
    else: 
        return 'Other'

def get_weapon_category(desc):
    desc = str(desc).upper() if pd.notna(desc) else ''
    if 'GUN' in desc or 'FIREARM' in desc or 'RIFLE' in desc or 'REVOLVER' in desc: 
        return 'Firearm'
    elif 'KNIFE' in desc or 'BLADE' in desc or 'CUTTING' in desc: 
        return 'Blade'
    elif 'BLUNT' in desc or 'CLUB' in desc or 'BAT' in desc: 
        return 'Blunt Object'
    elif 'STRONG-ARM' in desc or 'HANDS' in desc or 'FIST' in desc: 
        return 'Physical Force'
    elif desc == '' or desc == 'NAN': 
        return 'No Weapon'
    else: 
        return 'Other Weapon'

print("✅ Funções de transformação definidas")


# In[ ]:


# Aplicar transformações
print("🔄 Aplicando transformações...")

# Converter datas
df_clean['date_temp'] = pd.to_datetime(df_clean['DATE OCC'], format='%m/%d/%Y %I:%M:%S %p', errors='coerce')
df_clean['date_reported_temp'] = pd.to_datetime(df_clean['Date Rptd'], format='%m/%d/%Y %I:%M:%S %p', errors='coerce')

# Remover registros com datas inválidas após parsing
initial_count = len(df_clean)
df_clean = df_clean[(df_clean['date_temp'].notna()) & (df_clean['date_reported_temp'].notna())].copy()
print(f"   Após remover datas inválidas: {len(df_clean):,} (removidos {initial_count - len(df_clean):,})")

# Extrair date_reported para uso posterior
date_reported = df_clean['date_reported_temp']

# Normalizar horário
time_occ = pd.to_numeric(df_clean['TIME OCC'], errors='coerce').fillna(0).astype(int)

# Criar DataFrame Silver
silver = pd.DataFrame()

# Identificação
silver['crime_id'] = df_clean['DR_NO'].values

# Datas - use .values to avoid index alignment issues
silver['date_reported'] = date_reported.values
silver['date_occurred'] = df_clean['date_temp'].values
silver['time_occurred'] = time_occ.values

# Temporal
silver['hour'] = (time_occ // 100).astype(int).values
silver['day_of_week'] = df_clean['date_temp'].dt.dayofweek.values
silver['day_name'] = df_clean['date_temp'].dt.day_name().values
silver['period_of_day'] = silver['hour'].apply(get_period)

# Localização
silver['area_code'] = df_clean['AREA'].values
silver['area_name'] = df_clean['AREA NAME'].values
silver['district_code'] = df_clean['Rpt Dist No'].values

# Crime
silver['crime_severity'] = df_clean['Part 1-2'].map({1: 'Serious', 2: 'Minor'}).values
silver['crime_code'] = df_clean['Crm Cd'].values
silver['crime_description'] = df_clean['Crm Cd Desc'].values
silver['crime_category'] = df_clean['Crm Cd Desc'].apply(get_crime_category).values

# Vítima
silver['victim_age'] = df_clean['Vict Age'].values
silver['victim_age_group'] = df_clean['Vict Age'].apply(get_age_group).values
silver['victim_sex'] = df_clean['Vict Sex'].fillna('X').values
silver['victim_sex_desc'] = df_clean['Vict Sex'].map(sex_map).fillna('Unknown').values
silver['victim_descent'] = df_clean['Vict Descent'].fillna('X').values
silver['victim_descent_desc'] = df_clean['Vict Descent'].map(descent_map).fillna('Unknown').values

# Premissa
silver['premise_code'] = df_clean['Premis Cd'].values
silver['premise_description'] = df_clean['Premis Desc'].values
silver['premise_category'] = df_clean['Premis Desc'].apply(get_premise_category).values

# Arma
silver['weapon_code'] = df_clean['Weapon Used Cd'].values
silver['weapon_description'] = df_clean['Weapon Desc'].values
silver['weapon_category'] = df_clean['Weapon Desc'].apply(get_weapon_category).values

# Flags
silver['is_violent'] = (silver['crime_category'] == 'Violent Crime')
silver['has_weapon'] = (silver['weapon_category'] != 'No Weapon')

# Status
silver['status_code'] = df_clean['Status'].values
silver['status_description'] = df_clean['Status Desc'].values
silver['case_closed'] = df_clean['Status'].isin(['AA', 'JA']).values

# Coordenadas
silver['latitude'] = df_clean['LAT'].values
silver['longitude'] = df_clean['LON'].values
silver['location'] = df_clean['LOCATION'].str.strip().values

# Dimensões temporais
silver['year'] = df_clean['date_temp'].dt.year.values
silver['month'] = df_clean['date_temp'].dt.month.values
silver['quarter'] = df_clean['date_temp'].dt.quarter.values

# Metadados
silver['collected_at'] = datetime.now()

print(f"✅ Transformações aplicadas: {len(silver.columns)} colunas criadas")


# In[ ]:


# Salvar na camada Silver (PostgreSQL)
TRUNCATE_BEFORE_LOAD = True

with engine.begin() as conn:
    if TRUNCATE_BEFORE_LOAD:
        conn.exec_driver_sql("TRUNCATE TABLE silver.crimes")

silver.to_sql(
    'crimes',
    engine,
    schema='silver',
    if_exists='append',
    index=False,
    chunksize=5000,
    method='multi'
 )

print("\n" + "="*50)
print("✅ ETL Raw → Silver concluído (PostgreSQL)!")
print("="*50)
print(f"\n📊 Resumo:")
print(f"   Raw: {len(df):,} registros")
print(f"   Silver: {len(silver):,} registros")
print(f"   Redução: {(1 - len(silver)/len(df))*100:.1f}%")
print(f"\n🗄️  Base carregada: {POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}")

