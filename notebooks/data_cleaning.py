import os
import pandas as pd
import sqlite3
import numpy as np

# Step 0: Set absolute paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  
DATA_DIR = os.path.join(BASE_DIR, '..', 'data')       

CYCLONE_FILE = os.path.join(DATA_DIR, 'Annual_Cyclone_freq.csv')
GROUNDWATER_FILE = os.path.join(DATA_DIR, 'Ground_Water_data.csv')
KCC_FILE = os.path.join(DATA_DIR, 'KCC_telangana.csv')

# Step 1: Load Cyclone dataset
cyclones = pd.read_csv(CYCLONE_FILE, encoding='utf-8')
cyclones.columns = cyclones.columns.str.strip()  # Remove extra spaces

cyclones_clean = cyclones[['Year', 
                           'Cyclonic Disturbances - TOTAL', 
                           'Cyclones - TOTAL', 
                           'Severe Cyclones - TOTAL']].copy()

cyclones_clean.rename(columns={
    'Year': 'year',
    'Cyclonic Disturbances - TOTAL': 'cyclonic_disturbances',
    'Cyclones - TOTAL': 'cyclones',
    'Severe Cyclones - TOTAL': 'severe_cyclones'
}, inplace=True)

cyclones_clean[['cyclonic_disturbances','cyclones','severe_cyclones']] = \
    cyclones_clean[['cyclonic_disturbances','cyclones','severe_cyclones']].fillna(0).astype(int)

# Step 2: Load Groundwater dataset
groundwater = pd.read_csv(GROUNDWATER_FILE, encoding='ISO-8859-1')
groundwater.columns = groundwater.columns.str.strip()

pre_monsoon_cols = [col for col in groundwater.columns if 'Pre-monsoon' in col]

gw_cols = ['State_Name_With_LGD_Code','District_Name_With_LGD_Code'] + pre_monsoon_cols
groundwater_clean = groundwater[gw_cols].copy()

groundwater_clean.rename(columns={
    'State_Name_With_LGD_Code':'state',
    'District_Name_With_LGD_Code':'district'
}, inplace=True)

for col in pre_monsoon_cols:
    groundwater_clean[col] = pd.to_numeric(groundwater_clean[col], errors='coerce')

new_cols = {}
for col in groundwater_clean.columns:
    if 'Pre-monsoon' in col:
        year = ''.join(filter(str.isdigit, col))
        new_cols[col] = f'Pre-monsoon_{year}'
groundwater_clean.rename(columns=new_cols, inplace=True)

pre_monsoon_cols_clean = [col for col in groundwater_clean.columns if 'Pre-monsoon' in col]

groundwater_long = groundwater_clean.melt(
    id_vars=['state','district'],
    value_vars=pre_monsoon_cols_clean,
    var_name='year',
    value_name='groundwater_level'
)

groundwater_long['year'] = groundwater_long['year'].str.extract(r'(\d+)').astype(int)

groundwater_long['groundwater_level'] = groundwater_long.groupby('district')['groundwater_level'] \
                                                        .transform(lambda x: x.fillna(x.mean()))

# Step 3: Load KCC Telangana dataset
kcc = pd.read_csv(KCC_FILE, encoding='utf-8')
kcc.columns = kcc.columns.str.strip()
kcc_clean = kcc[['StateName','DistrictName','QueryText','KccAns','year','month']].copy()

kcc_clean.rename(columns={
    'StateName':'state',
    'DistrictName':'district',
    'QueryText':'query',
    'KccAns':'response'
}, inplace=True)

kcc_clean[['query','response']] = kcc_clean[['query','response']].fillna('')
kcc_clean['year'] = kcc_clean['year'].astype(int)

# Step 4: Merge Cyclones + Groundwater
climate_agri = pd.merge(groundwater_long, cyclones_clean, on='year', how='left')

# Step 5: Save to SQLite
DB_FILE = os.path.join(BASE_DIR, '..', 'samarth.db')
conn = sqlite3.connect(DB_FILE)

climate_agri.to_sql('climate_agri', conn, if_exists='replace', index=False)
kcc_clean.to_sql('kcc_telangana', conn, if_exists='replace', index=False)

conn.close()

print("✅ Database created: samarth.db")

