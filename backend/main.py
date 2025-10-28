import sqlite3
import pandas as pd
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'samarth.db')

# DB Connection
def get_conn():
    return sqlite3.connect(DB_PATH)

# Utility: Build IN clause safely
def build_in_clause(column, values):
    placeholders = ','.join(['?'] * len(values))
    return f" AND {column} IN ({placeholders})", values

# Get Dropdown Options
def get_states():
    conn = get_conn()
    df1 = pd.read_sql("SELECT DISTINCT state FROM climate_agri WHERE state IS NOT NULL", conn)
    df2 = pd.read_sql("SELECT DISTINCT state FROM kcc_telangana WHERE state IS NOT NULL", conn)
    conn.close()
    return sorted(list(set(df1['state'].tolist() + df2['state'].tolist())))


def get_districts(states=None):
    conn = get_conn()
    if states:
        placeholders = ','.join(['?'] * len(states))
        query = f"""
        SELECT DISTINCT district FROM climate_agri WHERE state IN ({placeholders})
        UNION
        SELECT DISTINCT district FROM kcc_telangana WHERE state IN ({placeholders})
        """
        df = pd.read_sql(query, conn, params=states + states)
    else:
        query = """
        SELECT DISTINCT district FROM climate_agri
        UNION
        SELECT DISTINCT district FROM kcc_telangana
        """
        df = pd.read_sql(query, conn)
    conn.close()
    return sorted(df['district'].dropna().tolist())


def get_years():
    # 1891–2025 inclusive
    return [str(y) for y in range(1891, 2026)]


def get_keywords():
    conn = get_conn()
    df = pd.read_sql("SELECT DISTINCT query FROM kcc_telangana WHERE query IS NOT NULL", conn)
    conn.close()
    # Remove near-duplicates (case-insensitive)
    unique_queries = list({q.strip().lower(): q.strip() for q in df['query']}.values())
    return sorted(unique_queries)

# Query Functions
def avg_groundwater(states=None, years=None):
    query = "SELECT AVG(groundwater_level) AS avg_gw FROM climate_agri WHERE 1=1"
    params = []

    if states:
        clause, vals = build_in_clause("state", states)
        query += clause
        params += vals
    if years:
        clause, vals = build_in_clause("year", years)
        query += clause
        params += vals

    conn = get_conn()
    df = pd.read_sql(query, conn, params=params)
    conn.close()

    return None if df.empty or pd.isna(df['avg_gw'].iloc[0]) else df['avg_gw'].iloc[0]


def cyclone_summary(years=None):
    query = "SELECT * FROM climate_agri WHERE 1=1"
    params = []

    if years:
        clause, vals = build_in_clause("year", years)
        query += clause
        params += vals

    conn = get_conn()
    df = pd.read_sql(query, conn, params=params)
    conn.close()
    return df


def district_groundwater_trend(districts):
    placeholders = ','.join(['?'] * len(districts))
    query = f"""
    SELECT district, year, groundwater_level
    FROM climate_agri
    WHERE district IN ({placeholders})
    ORDER BY district, year
    """
    conn = get_conn()
    df = pd.read_sql(query, conn, params=districts)
    conn.close()
    return df


def kcc_queries(states=None, districts=None, keywords=None):
    query = "SELECT state, district, query, response, year, month FROM kcc_telangana WHERE 1=1"
    params = []

    if states:
        clause, vals = build_in_clause("state", states)
        query += clause
        params += vals
    if districts:
        clause, vals = build_in_clause("district", districts)
        query += clause
        params += vals
    if keywords:
        clause, vals = build_in_clause("query", keywords)
        query += clause
        params += vals

    conn = get_conn()
    df = pd.read_sql(query, conn, params=params)
    conn.close()
    return df
