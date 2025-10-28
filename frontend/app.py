import streamlit as st
import matplotlib.pyplot as plt
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../backend'))

from main import (
    avg_groundwater, cyclone_summary, district_groundwater_trend, kcc_queries,
    get_states, get_districts, get_years, get_keywords
)

# Page Config
st.set_page_config(page_title="Project Samarth: Climate & Agriculture Q&A", layout="wide")
st.title("🛰️ Project Samarth: Climate & Agriculture Q&A System")

# Top Buttons
col1, col2 = st.columns(2)
with col1:
    if st.button("🌊 Average Groundwater Level"):
        st.session_state['avg_gw'] = True
with col2:
    if st.button("🌪️ Cyclone Summary"):
        st.session_state['cyclone'] = True

# Sidebar Filters
st.sidebar.header("🔍 Filters")

# Year
years = get_years()
year_filter = st.sidebar.multiselect("Select Year(s)", years, help="Select one or multiple years (1891–2025)")

# State
states = get_states()
state_filter = st.sidebar.multiselect("Select State(s)", states, help="Select one or more states")

# District (depends on state)
districts = get_districts(state_filter)
district_filter = st.sidebar.multiselect("Select District(s)", districts, help="Select one or more districts")

# Button below district filter
if st.sidebar.button("📈 Show Groundwater Trend") and district_filter:
    df_trend = district_groundwater_trend(district_filter)
    if df_trend.empty:
        st.info("No groundwater data found for the selected districts.")
    else:
        st.subheader("Groundwater Trend by District")
        for d in district_filter:
            ddf = df_trend[df_trend['district'] == d]
            fig, ax = plt.subplots()
            ax.plot(ddf['year'], ddf['groundwater_level'], marker='o', label=d)
            ax.set_xlabel("Year")
            ax.set_ylabel("Groundwater Level (m)")
            ax.set_title(f"Groundwater Trend - {d}")
            ax.grid(True)
            st.pyplot(fig)

# KCC Keywords
keywords = get_keywords()
keyword_filter = st.sidebar.multiselect("Select KCC Keyword(s)", keywords, help="Select one or more KCC query keywords")

# Button below KCC filter
if st.sidebar.button("🧩 Search KCC Queries") and keyword_filter:
    df_kcc = kcc_queries(state_filter, district_filter, keyword_filter)
    if df_kcc.empty:
        st.info("No matching KCC queries found.")
    else:
        st.subheader("KCC Queries & Responses")
        st.dataframe(df_kcc)

# Display Results for Top Buttons
if st.session_state.get('avg_gw'):
    avg_gw = avg_groundwater(state_filter, year_filter)
    if avg_gw:
        st.subheader("🌊 Average Groundwater Level (m)")
        st.success(f"{avg_gw:.2f}")
    else:
        st.warning("No data found for selected filters.")

if st.session_state.get('cyclone'):
    df_cyc = cyclone_summary(year_filter)
    if df_cyc.empty:
        st.warning("No cyclone data available for the selected years.")
    else:
        st.subheader("🌪️ Cyclone Summary")
        st.dataframe(df_cyc)
