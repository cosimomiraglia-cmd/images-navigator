"""
IMAGES NAVIGATOR — Modulo stili
================================
Importa questo modulo nell'app principale con:

    from styles import apply_styles
    apply_styles()

Chiamare apply_styles() subito dopo st.set_page_config().
"""

import streamlit as st

# ── PALETTE ────────────────────────────────────────────────
C_PRIMARY  = "#e3286d"
C_DARK     = "#565656"
C_MEDIUM   = "#a5a5a5"
C_BG       = "#e2ddd9"
C_BG2      = "#d4cfc9"
C_WHITE    = "#ffffff"
C_CARD     = "#ffffff"

def apply_styles():
    st.markdown(f"""
    <style>

    /* ── IMPORT FONT ───────────────────────────────────────── */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:ital,wght@0,300;0,400;0,500;0,600;0,700;1,400&display=swap');

    /* ── BASE ──────────────────────────────────────────────── */
    html, body, [class*="css"] {{
        font-family: 'Poppins', sans-serif !important;
    }}
    .stApp {{
        background-color: {C_BG};
    }}

    /* ── SIDEBAR ───────────────────────────────────────────── */
    [data-testid="stSidebar"] {{
        background-color: #2a2a2a;
        border-right: none;
    }}
    [data-testid="stSidebar"] * {{
        color: rgba(255,255,255,0.85) !important;
    }}
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {{
        color: {C_PRIMARY} !important;
        font-size: 11px !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        letter-spacing: 1.5px !important;
    }}
    [data-testid="stSidebar"] .stSelectbox label,
    [data-testid="stSidebar"] .stMultiSelect label,
    [data-testid="stSidebar"] .stFileUploader label,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] small {{
        color: rgba(255,255,255,0.65) !important;
        font-size: 12px !important;
    }}
    [data-testid="stSidebar"] [data-baseweb="select"] > div,
    [data-testid="stSidebar"] [data-baseweb="select"] {{
        background-color: rgba(255,255,255,0.08) !important;
        border-color: rgba(255,255,255,0.15) !important;
        color: white !important;
    }}
    [data-testid="stSidebar"] [data-baseweb="tag"] {{
        background-color: rgba(227,40,109,0.3) !important;
        border: none !important;
    }}
    [data-testid="stSidebar"] hr {{
        border-color: rgba(255,255,255,0.1) !important;
    }}
    [data-testid="stSidebar"] .stProgress > div > div {{
        background-color: rgba(255,255,255,0.15) !important;
    }}
    [data-testid="stSidebar"] .stProgress > div > div > div {{
        background-color: {C_PRIMARY} !important;
    }}

    /* ── BOTTONI SIDEBAR ───────────────────────────────────── */
    [data-testid="stSidebar"] .stDownloadButton button,
    [data-testid="stSidebar"] .stButton button {{
        background-color: {C_PRIMARY} !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        font-size: 12px !important;
        text-transform: uppercase !important;
        letter-spacing: 0.8px !important;
        padding: 8px 14px !important;
        transition: all 0.2s ease !important;
        width: 100% !important;
    }}
    [data-testid="stSidebar"] .stButton button:hover {{
        background-color: #c5205a !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 12px rgba(227,40,109,0.35) !important;
    }}

    /* ── TAB ────────────────────────────────────────────────── */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 8px;
        background-color: transparent;
        padding: 12px 0;
        border-bottom: none;
    }}
    .stTabs [data-baseweb="tab"] {{
        height: 42px;
        border-radius: 8px;
        background-color: {C_WHITE};
        border: 1.5px solid {C_MEDIUM};
        padding: 0 20px;
        transition: all 0.25s ease;
        box-shadow: 0 1px 3px rgba(0,0,0,0.06);
    }}
    .stTabs [data-baseweb="tab"] p {{
        font-size: 12px !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.8px !important;
        color: {C_DARK} !important;
    }}
    .stTabs [aria-selected="true"] {{
        background-color: {C_PRIMARY} !important;
        border-color: {C_PRIMARY} !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 16px rgba(227,40,109,0.28) !important;
    }}
    .stTabs [aria-selected="true"] p {{
        color: white !important;
    }}
    .stTabs [data-baseweb="tab-highlight"] {{
        display: none !important;
    }}
    .stTabs [data-baseweb="tab-border"] {{
        display: none !important;
    }}

    /* ── EXPANDER ───────────────────────────────────────────── */
    [data-testid="stExpander"] {{
        background-color: {C_WHITE};
        border: 1.5px solid rgba(165,165,165,0.3) !important;
        border-radius: 10px !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05) !important;
        overflow: hidden;
    }}
    [data-testid="stExpander"] summary {{
        font-weight: 700 !important;
        font-size: 13px !important;
        text-transform: uppercase !important;
        letter-spacing: 0.8px !important;
        color: {C_DARK} !important;
        padding: 14px 18px !important;
        background-color: {C_WHITE} !important;
    }}
    [data-testid="stExpander"] summary:hover {{
        background-color: #fafaf9 !important;
    }}
    [data-testid="stExpander"] [data-testid="stExpanderDetails"] {{
        padding: 4px 18px 18px !important;
    }}

    /* ── RADIO BUTTON (item audit) ──────────────────────────── */
    [data-testid="stRadio"] > label {{
        font-size: 14px !important;
        font-weight: 500 !important;
        color: {C_DARK} !important;
        line-height: 1.55 !important;
        margin-bottom: 6px !important;
    }}
    [data-testid="stRadio"] [role="radiogroup"] {{
        gap: 6px !important;
        flex-wrap: wrap;
    }}
    [data-testid="stRadio"] [role="radiogroup"] label {{
        border: 1.5px solid rgba(165,165,165,0.45) !important;
        border-radius: 6px !important;
        padding: 5px 13px !important;
        background: {C_WHITE} !important;
        font-size: 12.5px !important;
        font-weight: 500 !important;
        color: {C_DARK} !important;
        cursor: pointer !important;
        transition: all 0.15s !important;
        white-space: nowrap;
    }}
    [data-testid="stRadio"] [role="radiogroup"] label:hover {{
        border-color: {C_PRIMARY} !important;
        background: #fdf0f5 !important;
    }}

    /* ── CHECKBOX ───────────────────────────────────────────── */
    [data-testid="stCheckbox"] [data-testid="stCheckboxUserIcon"] {{
        background-color: {C_PRIMARY} !important;
        border-radius: 4px !important;
    }}
    [data-testid="stCheckbox"] label {{
        font-size: 13.5px !important;
        color: {C_DARK} !important;
    }}

    /* ── TEXT INPUT ─────────────────────────────────────────── */
    .stTextInput input {{
        border-radius: 7px !important;
        border: 1.5px solid rgba(165,165,165,0.4) !important;
        background-color: {C_WHITE} !important;
        font-size: 13px !important;
        padding: 8px 12px !important;
        transition: border-color 0.2s !important;
    }}
    .stTextInput input:focus {{
        border-color: {C_PRIMARY} !important;
        box-shadow: 0 0 0 2px rgba(227,40,109,0.12) !important;
    }}
    .stTextInput input:disabled {{
        opacity: 0.32 !important;
        background-color: #f5f3f0 !important;
    }}

    /* ── SELECTBOX / MULTISELECT ────────────────────────────── */
    [data-baseweb="select"] > div {{
        border-radius: 7px !important;
        border: 1.5px solid rgba(165,165,165,0.4) !important;
        background-color: {C_WHITE} !important;
    }}
    [data-baseweb="select"] > div:focus-within {{
        border-color: {C_PRIMARY} !important;
        box-shadow: 0 0 0 2px rgba(227,40,109,0.12) !important;
    }}
    [data-baseweb="tag"] {{
        background-color: rgba(227,40,109,0.12) !important;
        border-radius: 4px !important;
    }}
    [data-baseweb="tag"] span {{
        color: {C_PRIMARY} !important;
        font-weight: 600 !important;
    }}

    /* ── BOTTONI PRINCIPALI ─────────────────────────────────── */
    .stButton > button,
    .stDownloadButton > button {{
        border-radius: 8px !important;
        font-weight: 600 !important;
        font-size: 13px !important;
        text-transform: uppercase !important;
        letter-spacing: 0.8px !important;
        transition: all 0.2s ease !important;
        padding: 9px 20px !important;
    }}
    .stButton > button[kind="primary"],
    .stDownloadButton > button {{
        background-color: {C_PRIMARY} !important;
        color: white !important;
        border: none !important;
        box-shadow: 0 2px 8px rgba(227,40,109,0.2) !important;
    }}
    .stButton > button[kind="primary"]:hover,
    .stDownloadButton > button:hover {{
        background-color: #c5205a !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 5px 14px rgba(227,40,109,0.32) !important;
    }}
    .stButton > button[kind="secondary"] {{
        background-color: transparent !important;
        color: {C_DARK} !important;
        border: 1.5px solid {C_MEDIUM} !important;
    }}
    .stButton > button[kind="secondary"]:hover {{
        border-color: {C_PRIMARY} !important;
        color: {C_PRIMARY} !important;
        background-color: #fdf0f5 !important;
    }}

    /* ── ALERT / NOTICE ─────────────────────────────────────── */
    [data-testid="stAlert"] {{
        border-radius: 8px !important;
        border-left-width: 4px !important;
    }}

    /* ── DIVIDER ────────────────────────────────────────────── */
    hr {{
        border-color: rgba(165,165,165,0.25) !important;
        margin: 16px 0 !important;
    }}

    /* ── TITOLI PRINCIPALI ──────────────────────────────────── */
    h1 {{
        font-size: 28px !important;
        font-weight: 800 !important;
        letter-spacing: -0.5px !important;
        color: {C_DARK} !important;
        text-transform: uppercase !important;
    }}
    h2 {{
        font-size: 18px !important;
        font-weight: 700 !important;
        color: {C_DARK} !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
    }}
    h3 {{
        font-size: 15px !important;
        font-weight: 700 !important;
        color: {C_DARK} !important;
    }}

    /* ── CARD CLASSI CUSTOM ─────────────────────────────────── */
    .result-card {{
        background-color: {C_WHITE};
        padding: 22px 24px;
        border-radius: 14px;
        box-shadow: 0 4px 16px rgba(0,0,0,0.07);
        margin-bottom: 10px;
        border: 1px solid rgba(165,165,165,0.15);
    }}
    .measure-label {{
        font-size: 9.5px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1.8px;
        color: {C_MEDIUM};
        margin-bottom: 8px;
    }}
    .measure-value {{
        font-size: 14px;
        font-weight: 700;
        padding: 11px 14px;
        border-radius: 8px;
    }}
    .item-divider {{
        border: none;
        border-top: 1px solid rgba(165,165,165,0.2);
        margin: 8px 0;
    }}

    /* ── TESTO DI AIUTO SOTTO GLI ITEM ──────────────────────── */
    .item-help {{
        font-size: 12px;
        color: {C_MEDIUM};
        font-style: italic;
        margin: 2px 0 4px;
        line-height: 1.5;
    }}
    .item-help-checkbox {{
        font-size: 12px;
        color: {C_MEDIUM};
        font-style: italic;
        margin: -8px 0 8px 24px;
        line-height: 1.4;
    }}

    /* ── ONBOARDING: CONTAINER ESTERNO ──────────────────────── */
    .ob-container {{
        max-width: 800px;
        margin: 0 auto;
        padding-top: 20px;
    }}

    /* ── ONBOARDING: HERO (banner con gradient) ─────────────── */
    .ob-hero {{
        background: linear-gradient(140deg, #1B2D45 0%, #2A4060 100%);
        border-radius: 16px;
        padding: 40px 44px 36px;
        color: white;
        margin-bottom: 28px;
    }}
    .ob-hero-tag {{
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 2px;
        color: rgba(255,255,255,0.5);
        text-transform: uppercase;
        margin-bottom: 10px;
    }}
    .ob-hero-title {{
        font-size: 36px;
        font-weight: 800;
        margin-bottom: 10px;
        color: white;
        letter-spacing: -0.5px;
    }}
    .ob-hero-sub {{
        font-size: 16px;
        opacity: 0.85;
        line-height: 1.6;
        max-width: 580px;
    }}

    /* ── ONBOARDING: CARD ESPLICATIVE ───────────────────────── */
    .ob-card {{
        background: white;
        border-radius: 12px;
        padding: 24px 26px;
        margin-bottom: 16px;
        border-left: 5px solid {C_MEDIUM};
    }}
    .ob-card.primary {{
        border-left-color: {C_PRIMARY};
    }}
    .ob-card-label {{
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 1.5px;
        color: {C_MEDIUM};
        text-transform: uppercase;
        margin-bottom: 10px;
    }}
    .ob-card-body {{
        color: {C_DARK};
        font-size: 14px;
        line-height: 1.65;
        margin: 0;
    }}

    /* ── ONBOARDING: CHIP DELLE OPZIONI Sì/No/N.A. ──────────── */
    .ob-chip-row {{
        display: flex;
        align-items: flex-start;
        gap: 10px;
        margin-bottom: 10px;
    }}
    .ob-chip-row:last-child {{
        margin-bottom: 0;
    }}
    .ob-chip {{
        padding: 3px 12px;
        border-radius: 5px;
        font-size: 12px;
        font-weight: 700;
        flex-shrink: 0;
        white-space: nowrap;
    }}
    .ob-chip-yes {{ background: #d4edda; color: #155724; }}
    .ob-chip-no  {{ background: #f8d7da; color: #721c24; }}
    .ob-chip-na  {{ background: #f3f4f6; color: #6b7280; }}
    .ob-chip-text {{
        color: {C_DARK};
        font-size: 13px;
        line-height: 1.5;
    }}
    .ob-chips-wrapper {{
        margin-top: 14px;
    }}

    /* ── ONBOARDING: DISCLAIMER ─────────────────────────────── */
    .ob-disclaimer {{
        border-radius: 10px;
        padding: 16px 22px;
        margin: 8px 0 12px;
        font-size: 13px;
        line-height: 1.65;
    }}
    .ob-disclaimer:last-of-type {{
        margin-bottom: 24px;
    }}
    .ob-disclaimer.amber {{
        background: #fff8e1;
        border: 1px solid #ffe082;
        color: #5d4037;
    }}
    .ob-disclaimer.blue {{
        background: #f0f4ff;
        border: 1px solid #c7d2fe;
        color: #3730a3;
    }}
    .ob-disclaimer.green {{
        background: #f0fdf4;
        border: 1px solid #86efac;
        color: #166534;
    }}

    /* ── SCORECARD: PLACEHOLDER (audit non avviato) ─────────── */
    .sc-placeholder {{
        background: white;
        border: 1px dashed {C_MEDIUM};
        border-radius: 16px;
        padding: 40px 24px;
        text-align: center;
        margin-top: 15px;
    }}
    .sc-placeholder-icon {{
        font-size: 32px;
        margin-bottom: 12px;
    }}
    .sc-placeholder-text {{
        color: {C_MEDIUM};
        font-size: 14px;
        margin: 0;
        text-transform: uppercase;
        letter-spacing: 1px;
    }}

    /* ── SCORECARD: COPERTURA ───────────────────────────────── */
    .sc-coverage {{
        border-radius: 12px;
        padding: 14px 18px;
        margin-bottom: 12px;
    }}
    .sc-coverage.ok    {{ background: #d4edda; color: #155724; }}
    .sc-coverage.warn  {{ background: #fff3cd; color: #856404; }}
    .sc-coverage.info  {{ background: #f8f9fa; color: #6c757d; }}
    .sc-coverage-label {{
        font-size: 10px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-bottom: 4px;
    }}
    .sc-coverage-value {{
        font-size: 20px;
        font-weight: 700;
    }}
    .sc-coverage-msg {{
        font-size: 12px;
        margin-top: 4px;
        line-height: 1.4;
    }}

    /* ── SCORECARD: BORDI CARD MISURE ───────────────────────── */
    .result-card-primary {{
        border-top: 6px solid {C_PRIMARY};
    }}
    .result-card-secondary {{
        border-top: 6px solid {C_MEDIUM};
    }}

    /* ── SCORECARD: PANNELLO INTERSEZIONALE ─────────────────── */
    .sc-intersect {{
        background: #fdf0f5;
        border: 1px solid {C_PRIMARY};
        border-radius: 8px;
        padding: 10px 14px;
        margin-top: -6px;
        margin-bottom: 10px;
        font-size: 12px;
        color: {C_DARK};
    }}
    .sc-intersect-header {{
        color: {C_PRIMARY};
        font-weight: 700;
    }}

    /* ── SCORECARD: DETTAGLIO PER LIVELLO ───────────────────── */
    .sc-level-row {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 6px 0;
        border-bottom: 1px solid #eee;
        font-size: 13px;
    }}
    .sc-level-name {{
        color: {C_DARK};
        font-weight: 600;
    }}
    .sc-level-count {{
        font-weight: 400;
        color: {C_MEDIUM};
        font-size: 11px;
    }}
    .sc-level-badge {{
        padding: 2px 10px;
        border-radius: 6px;
        font-weight: 700;
        font-size: 12px;
    }}

    /* ── SCORECARD: STATO OUTPUT (Testi e Immagini) ─────────── */
    .sc-output-row {{
        margin: 6px 0;
        color: {C_DARK};
        font-size: 14px;
    }}

    /* ── SIDEBAR: PROGRESSO AUDIT ───────────────────────────── */
    .sb-progress-label {{
        font-size: 12px;
        margin-top: 4px;
    }}
    .sb-progress-label.ok    {{ color: #28a745; }}
    .sb-progress-label.warn  {{ color: #856404; }}
    .sb-progress-label.info  {{ color: {C_MEDIUM}; }}

    /* ── FILE UPLOADER ──────────────────────────────────────── */
    [data-testid="stFileUploader"] {{
        background: rgba(255,255,255,0.06) !important;
        border: 1.5px dashed rgba(255,255,255,0.2) !important;
        border-radius: 8px !important;
        padding: 12px !important;
    }}
    [data-testid="stFileUploader"] * {{
        font-size: 12px !important;
    }}

    /* ── PROGRESS BAR ───────────────────────────────────────── */
    [data-testid="stProgressBar"] > div {{
        background-color: rgba(165,165,165,0.25) !important;
        border-radius: 4px !important;
        height: 6px !important;
    }}
    [data-testid="stProgressBar"] > div > div {{
        background-color: {C_PRIMARY} !important;
        border-radius: 4px !important;
        transition: width 0.4s ease !important;
    }}

    /* ── CAPTION / SMALL ────────────────────────────────────── */
    .stCaption, small {{
        font-size: 12px !important;
        color: {C_MEDIUM} !important;
        line-height: 1.5 !important;
    }}

    /* ── SUBHEADER ──────────────────────────────────────────── */
    [data-testid="stHeading"] h2,
    .stSubheader {{
        font-size: 20px !important;
        font-weight: 800 !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
        color: {C_DARK} !important;
    }}

    </style>
    """, unsafe_allow_html=True)
