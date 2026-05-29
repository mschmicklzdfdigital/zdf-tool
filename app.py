import streamlit as st

# =========================================================
# PAGE
# =========================================================
st.set_page_config(
    page_title="ZDFheute WhatsApp Checker",
    layout="wide"
)

# =========================================================
# ZDF COLOR SYSTEM
# =========================================================
ZDF_ORANGE = "#ff4d00"
ZDF_BLUE = "#0b1b2b"
CARD = "#162436"
TEXT = "#e5e7eb"
MUTED = "#94a3b8"


# =========================================================
# BACKGROUND FIX (LESS AGGRESSIVE = TEXT VISIBLE)
# =========================================================
st.markdown(f"""
<style>

.stApp {{
    background-color: {ZDF_BLUE};
    color: {TEXT};
    font-family: Arial;
}}

h1, h2, h3, p {{
    color: {TEXT} !important;
}}

/* KPI CARDS */
.kpi {{
    background: {CARD};
    padding: 18px;
    border-radius: 14px;
    text-align: center;
    border-left: 4px solid {ZDF_ORANGE};
}}

.kpi-title {{
    font-size: 14px;
    color: {MUTED};
}}

.kpi-value {{
    font-size: 28px;
    font-weight: bold;
    color: white;
}}

/* HEADER */
.header {{
    display:flex;
    justify-content:space-between;
    align-items:center;
    padding: 15px 25px;
    border-bottom: 1px solid #223247;
}}

.logo {{
    font-size: 20px;
    font-weight: bold;
}}

.logo span {{
    color: {ZDF_ORANGE};
}}

/* TAGS */
.tag {{
    display:inline-block;
    padding:6px 12px;
    margin:4px;
    border-radius:20px;
    background:#1f2f46;
    font-size:13px;
}}

</style>
""", unsafe_allow_html=True)


# =========================================================
# HEADER (NOW CLEAN + UNDERSTANDABLE)
# =========================================================
col1, col2, col3 = st.columns([1, 2, 1])

with col1:
    st.image("https://upload.wikimedia.org/wikipedia/commons/0/0c/ZDF_logo.svg", width=70)

with col2:
    st.markdown("""
    <div class="logo" style="text-align:center;">
        WhatsApp Artikel-Checker <span>ZDFheute</span>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.image("https://upload.wikimedia.org/wikipedia/commons/6/6f/ZDFheute_Logo_2020.svg", width=110)


st.caption("by ZDF Digital News-Redaktion")

st.markdown("---")


# =========================================================
# INTUITIVE EXPLANATION (VERY IMPORTANT FIX)
# =========================================================
st.markdown("""
### 📊 Was zeigt dir dieses Tool?

Du siehst hier **alle ZDFheute-Artikel**, die im gewählten Zeitraum erschienen sind,  
aber **noch NICHT im WhatsApp-Kanal gepostet wurden**.

👉 Sie werden automatisch sortiert nach Themen  
👉 „Video- und Übersichtsseiten“ werden herausgefiltert  
👉 Du erkennst sofort, was noch fehlt
""")

st.markdown("---")


# =========================================================
# KPI DASHBOARD (NOW HUMAN READABLE)
# =========================================================
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="kpi">
        <div class="kpi-value">0</div>
        <div class="kpi-title">🧾 Fehlende Artikel</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="kpi">
        <div class="kpi-value">0</div>
        <div class="kpi-title">📂 Erkannte Kategorien</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="kpi">
        <div class="kpi-value">0</div>
        <div class="kpi-title">🚫 Herausgefiltert</div>
    </div>
    """, unsafe_allow_html=True)


st.markdown("---")


# =========================================================
# CATEGORY HELP (MAKES IT UNDERSTANDABLE)
# =========================================================
st.markdown("### 🧠 Kategorien im Überblick")

st.markdown("""
<span class="tag">Macht & Politik</span>
<span class="tag">Service & Alltag</span>
<span class="tag">Kriminalität</span>
<span class="tag">Trends & Promis</span>
<span class="tag">Gesellschaft</span>
<span class="tag">Sonstiges</span>
""", unsafe_allow_html=True)
