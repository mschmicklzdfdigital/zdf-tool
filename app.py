import streamlit as st
import pandas as pd
import requests
import xml.etree.ElementTree as ET
from datetime import datetime, date

# =========================================================
# PAGE CONFIGURATION (PIKFEIN & PROFESSIONAL)
# =========================================================
st.set_page_config(
    page_title="ZDFheute | WhatsApp Artikel-Checker",
    page_icon="🧡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================================================
# MODERN ZDF CORAL & SLATE PREMIUM THEME
# =========================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

/* Main App Background Override */
.stApp {
    background: radial-gradient(circle at top left, #121c2e, #070b12);
    color: #f1f3f5;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, Arial, sans-serif;
}

/* Custom Header Container */
.zdf-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 20px 0;
    border-bottom: 2px solid rgba(255, 77, 0, 0.15);
    margin-bottom: 30px;
}

.zdf-logo-container {
    display: flex;
    align-items: center;
    gap: 15px;
}

.zdf-title {
    font-size: 26px;
    font-weight: 700;
    letter-spacing: -0.5px;
    background: linear-gradient(90deg, #ffffff 0%, #ff5a00 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.zdf-subtitle {
    font-size: 13px;
    color: #8a99ad;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-top: -4px;
}

/* Premium Info Box & Cards */
.intro-container {
    background: rgba(255, 255, 255, 0.03);
    border-left: 4px solid #ff5a00;
    border-radius: 4px 12px 12px 4px;
    padding: 20px;
    margin-bottom: 35px;
    backdrop-filter: blur(8px);
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
}

.intro-text {
    font-size: 15px;
    line-height: 1.6;
    color: #e2e8f0;
}

.category-header {
    font-size: 18px;
    font-weight: 600;
    color: #ff5a00;
    margin: 30px 0 15px 0;
    padding-bottom: 6px;
    border-bottom: 1px solid rgba(255, 77, 0, 0.2);
    display: flex;
    align-items: center;
    gap: 10px;
}

/* Glassmorphic Article Cards */
.article-card {
    background: rgba(20, 30, 48, 0.4);
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 12px;
    padding: 18px;
    margin-bottom: 12px;
    backdrop-filter: blur(12px);
    transition: all 0.25s ease-in-out;
}

.article-card:hover {
    border: 1px solid rgba(255, 77, 0, 0.3);
    background: rgba(255, 77, 0, 0.02);
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(255, 77, 0, 0.05);
}

.article-headline {
    font-size: 16px;
    font-weight: 600;
    color: #ffffff;
    margin-bottom: 6px;
    line-height: 1.4;
}

.article-link {
    font-size: 13px;
    color: #ff5a00;
    text-decoration: none;
    word-break: break-all;
    font-weight: 500;
}

.article-link:hover {
    text-decoration: underline;
    color: #ff7c33;
}

/* Stat KPI Blocks */
.kpi-container {
    background: rgba(255, 77, 0, 0.04);
    border: 1px solid rgba(255, 77, 0, 0.15);
    border-radius: 14px;
    padding: 20px;
    text-align: center;
    box-shadow: inset 0 0 15px rgba(255, 77, 0, 0.02);
}

.kpi-value {
    font-size: 36px;
    font-weight: 700;
    color: #ffffff;
    line-height: 1;
    margin-bottom: 4px;
}

.kpi-label {
    font-size: 13px;
    color: #a0aec0;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

/* Hide default streamlit clutter */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# =========================================================
# BRAND HEADER WITH PIXEL-PERFECT VECTORS
# =========================================================
st.markdown("""
<div class="zdf-header">
    <div class="zdf-logo-container">
        <svg width="65" height="40" viewBox="0 0 100 62" fill="none" xmlns="http://www.w3.org/2000/svg">
            <rect width="100" height="62" rx="6" fill="#FF5A00"/>
            <path d="M22 18H42L29 44H18L22 18Z" fill="white"/>
            <path d="M41 18H55C64 18 69 22 67 29C65 37 58 44 48 44H34L41 18ZM49 24L45 38H49C54 38 57 35 58 31C59 27 56 24 51 24Z" fill="white"/>
            <path d="M64 18H84L81 24H73L71 31H78L76 37H69L66 44H56L64 18Z" fill="white"/>
        </svg>
        <div>
            <div class="zdf-title">WhatsApp Artikel-Checker</div>
            <div class="zdf-subtitle">ZDF Digital News-Redaktion</div>
        </div>
    </div>
    <div style="text-align: right; color: #8a99ad; font-size: 12px; font-weight: 500;">
        Plattform-Standard v2026.1<br>
        <span style="color: #ff5a00;">●</span> Live-Abgleich aktiv
    </div>
</div>
""", unsafe_allow_html=True)

# =========================================================
# REQUIRED TEXT COMPONENT (EXACT TEXT WORDING)
# =========================================================
st.markdown("""
<div class="intro-container">
    <div class="intro-text">
        Dieses Tool analysiert ZDFheute-Artikel im gewählten Zeitraum, vergleicht sie mit einer 
        Excel-Liste der Artikel, die auf dem WhatsApp-Kanal der ZDFheute liefen (anhand der piano-Excel-Datei) 
        und zeigt dir nur die Inhalte, die noch nicht im WhatsApp-Kanal veröffentlicht wurden.
    </div>
</div>
""", unsafe_allow_html=True)

# =========================================================
# CONTROL PANEL (INTEGRATED & CLEAN UI SLEEK GRID)
# =========================================================
st.markdown("<p style='font-weight: 600; font-size: 16px; margin-bottom: 5px; color: #ffffff;'>⚙️ Konfiguration & Datenquelle</p>", unsafe_allow_html=True)

col_file, col_d1, col_
