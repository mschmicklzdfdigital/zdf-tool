import streamlit as st
import pandas as pd
import requests
import xml.etree.ElementTree as ET
from datetime import datetime, date

# =========================================================
# PAGE CONFIGURATION
# =========================================================
st.set_page_config(
    page_title="ZDFheute | WhatsApp Hub",
    page_icon="🧡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================================================
# BERLIN MINIMALIST DARK THEME (HIGH-END EDITORIAL 2026)
# =========================================================
ui_styles = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

.stApp {
    background-color: #05070c !important;
    color: #f1f5f9 !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}

::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: #05070c; }
::-webkit-scrollbar-thumb { background: #1e293b; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #ff5a00; }

p, li, span, label, .stMarkdown {
    color: #94a3b8 !important;
    font-size: 15px !important;
}

.brand-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 30px 0 15px 0;
    border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    margin-bottom: 30px;
}

.shimmer-title {
    font-size: 28px !important;
    font-weight: 800 !important;
    letter-spacing: -1.2px;
    background: linear-gradient(120deg, #ffffff 30%, #ff7a22 50%, #ffffff 70%);
    background-size: 200% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: shine 4s linear infinite;
}

@keyframes shine {
    to { background-position: 200% center; }
}

.live-dot-de {
    display: inline-block;
    width: 6px;
    height: 6px;
    background-color: #ff5a00;
    border-radius: 50%;
    margin-right: 8px;
    vertical-align: middle;
}

.editorial-info-box {
    background: #0d111c;
    border-left: 3px solid #ff5a00;
    padding: 16px 20px;
    border-radius: 0 8px 8px 0;
    margin-bottom: 35px;
    font-size: 14.5px;
    color: #cbd5e1 !important;
    line-height: 1.5;
}

[data-testid="stFileUploader"] {
    background: #0d111c !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    border-radius: 8px !important;
    padding: 18px !important;
    transition: border-color 0.2s ease;
}
[data-testid="stFileUploader"]:hover {
    border-color: #ff5a00 !important;
}
[data-testid="stFileUploader"] label p {
    color: #ffffff !important;
    font-weight: 700 !important;
    font-size: 15px !important;
}

.clean-kpi-container {
    padding: 25px 0;
    margin: 25px 0;
    border-top: 1px solid rgba(255, 255, 255, 0.08);
    border-bottom: 1px solid rgba(255, 255, 255, 0.08);
}
.kpi-shimmer-number {
    font-size: 38px !important;
    font-weight: 800;
    letter-spacing: -1px;
    background: linear-gradient(90deg, #ff5a00 0%, #ff9e66 50%, #ff5a00 100
