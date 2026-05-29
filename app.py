import streamlit as st
import pandas as pd
import requests
import xml.etree.ElementTree as ET
from datetime import datetime, date

# =========================================================
# PAGE CONFIGURATION (PIKFEIN & PROFESSIONAL)
# =========================================================
st.set_page_config(
    page_title="ZDFheute | WhatsApp Intelligence Hub",
    page_icon="🧡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================================================
# NEXT-GEN CYBER SLATE & BRAND CORAL THEME (STRICT SYNTAX)
# =========================================================
ui_styles = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

.stApp {
    background: radial-gradient(circle at 50% 0%, #0d1527 0%, #050810 100%) !important;
    color: #f8fafc !important;
    font-family: 'Inter', -apple-system, sans-serif !important;
}
.brand-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 24px 0;
    border-bottom: 1px solid rgba(255, 90, 0, 0.15);
    margin-bottom: 35px;
}
.brand-logos-left {
    display: flex;
    align-items: center;
    gap: 20px;
}
.brand-divider {
    width: 1px;
    height: 35px;
    background: rgba(255, 255, 255, 0.15);
}
.title-block {
    display: flex;
    flex-direction: column;
}
.main-title {
    font-size: 28px;
    font-weight: 700;
    letter-spacing: -0.8px;
    background: linear-gradient(135deg, #ffffff 30%, #ff5a00 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.meta-subtitle {
    font-size: 11px;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 2px;
    font-weight: 600;
    margin-top: 2px;
}
.premium-info-wrapper {
    background: linear-gradient(135deg, rgba(255, 255, 255, 0.03) 0%, rgba(255, 255, 255, 0.01) 100%);
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-left: 4px solid #ff5a00;
    border-radius: 8px;
    padding: 20px;
    margin-bottom: 40px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.25);
    backdrop-filter: blur(12px);
}
.premium-info-text {
    font-size: 15px;
    line-height: 1.6;
    color: #cbd5e1;
    font-weight: 400
