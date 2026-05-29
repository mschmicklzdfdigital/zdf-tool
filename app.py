import streamlit as st

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="ZDFheute WhatsApp Checker",
    layout="wide"
)

# =========================================================
# MODERN DARK NEWSROOM STYLE
# =========================================================
st.markdown("""
<style>

/* Background */
.stApp {
    background-color: #0f172a;
    color: white;
    font-family: Inter, Arial, sans-serif;
}

/* Header */
.header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 18px 30px;
    border-bottom: 1px solid #243244;
}

/* Title */
.title {
    font-size: 22px;
    font-weight: 700;
    color: white;
}

/* KPI Cards */
.kpi-container {
    display: flex;
    gap: 15px;
    margin: 20px 0;
}

.kpi {
    flex: 1;
    background: #1e293b;
    padding: 15px;
    border-radius: 12px;
    text-align: center;
}

/* Category Buttons */
.cat {
    display: inline-block;
    padding: 6px 12px;
    margin: 5px;
    border-radius: 20px;
    background: #1e293b;
    font-size: 13px;
}

/* Article Card */
.card {
    background: #1e293b;
    padding: 14px;
    border-radius: 12px;
    margin-bottom: 10px;
    border-left: 3px solid #ff4d00;
}

/* URL */
.url {
    font-size: 12px;
    color: #94a3b8;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# HEADER (LOGO AREA)
# =========================================================
col1, col2, col3 = st.columns([1, 2, 1])

with col1:
    st.image("https://upload.wikimedia.org/wikipedia/commons/0/0c/ZDF_logo.svg", width=80)

with col2:
    st.markdown("<div class='title'>ZDFheute WhatsApp Artikel-Checker</div>", unsafe_allow_html=True)

with col3:
    st.image("https://upload.wikimedia.org/wikipedia/commons/6/6f/ZDFheute_Logo_2020.svg", width=100)


st.caption("by ZDF Digital News-Redaktion")

st.markdown("---")


# =========================================================
# KPI DASHBOARD (PLACEHOLDER LOGIC)
# =========================================================
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("<div class='kpi'><h3>0</h3><p>Fehlende Artikel</p></div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='kpi'><h3>0</h3><p>Kategorien</p></div>", unsafe_allow_html=True)

with col3:
    st.markdown("<div class='kpi'><h3>0</h3><p>Gefiltert</p></div>", unsafe_allow_html=True)


st.markdown("---")


# =========================================================
# CATEGORY TAGS (UI ONLY)
# =========================================================
st.markdown("""
<div>
<span class="cat">Macht und Folgen</span>
<span class="cat">Service & Alltag</span>
<span class="cat">Trends & Unterhaltung</span>
<span class="cat">Zwischen Tat & Aufklärung</span>
<span class="cat">Sonstiges</span>
</div>
""", unsafe_allow_html=True)
