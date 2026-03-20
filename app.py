import streamlit as st
from datetime import datetime

# CONFIGURAZIONE PAGINA
st.set_page_config(page_title="IMAGES NAVIGATOR", layout="wide", initial_sidebar_state="expanded")

# --- AREA PERSONALIZZAZIONE PALETTE ---
# Inserisci qui i tuoi codici esadecimali (es. #123456)
COLOR_PRIMARIO = "#228be6"  # Colore dei Tab attivi e bordi
COLOR_SFONDO_TAB = "#f1f3f5" # Colore dei Tab inattivi
COLOR_TESTO_TAB = "#495057"  # Colore del testo nei Tab
COLOR_ACCENTO = "#1c7ed6"    # Colore per hover e dettagli

# CUSTOM CSS AGGIORNATO
st.markdown(f"""
    <style>
    /* Sfondo generale */
    .main {{
        background-color: #f8f9fa;
    }}
    
    /* STILIZZAZIONE AVANZATA DEI TAB */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 15px; /* Spazio tra i tab */
        background-color: transparent;
        padding: 10px 0px;
    }}

    .stTabs [data-baseweb="tab"] {{
        height: 60px; /* Aumentata altezza */
        min-width: 140px; /* Larghezza minima garantita */
        border-radius: 8px;
        background-color: {COLOR_SFONDO_TAB};
        border: 1px solid #dee2e6;
        padding: 0px 25px; /* Margini interni generosi (destra/sinistra) */
        transition: all 0.3s ease;
    }}

    /* Testo all'interno dei tab */
    .stTabs [data-baseweb="tab"] p {{
        font-size: 14px;
        font-weight: 600;
        text-transform: uppercase;
        color: {COLOR_TESTO_TAB};
    }}

    /* Tab selezionato */
    .stTabs [aria-selected="true"] {{
        background-color: {COLOR_PRIMARIO} !important;
        border-color: {COLOR_PRIMARIO} !important;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    }}
    
    .stTabs [aria-selected="true"] p {{
        color: white !important;
    }}

    /* Card Risultati */
    .result-card {{
        background-color: white;
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        border-left: 6px solid {COLOR_PRIMARIO};
        margin-top: 20px;
    }}

    /* Uniformità etichette */
    h1, h2, h3, label, .stMarkdown p {{
        text-transform: uppercase;
        letter-spacing: 0.8px;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- RESTO DELLA LOGICA (INVARIATA MA CON ETICHETTE PULITE) ---

DOMINI = {
    "GIUSTIZIA E SICUREZZA": {"mult": 2.2, "threshold": 6.0},
    "SANITA E WELFARE": {"mult": 2.0, "threshold": 6.0},
    "PUBBLICA AMMINISTRAZIONE": {"mult": 2.0, "threshold": 7.0},
    "FINANZA E CREDITO": {"mult": 1.9, "threshold": 7.5},
    "ISTRUZIONE E RICERCA": {"mult": 1.8, "threshold": 8.0},
    "RECRUITING E HR": {"mult": 1.7, "threshold": 8.0},
    "MARKETING E MEDIA": {"mult": 1.3, "threshold": 10.0},
    "GAMING E ENTERTAINMENT": {"mult": 1.1, "threshold": 12.0}
}

with st.sidebar:
    st.title("IMPOSTAZIONI")
    dominio_scelto = st.selectbox("DOMINIO APPLICATIVO", list(DOMINI.keys()))
    st.divider()
    st.markdown("🔍 **NOTA METODOLOGICA**")
    st.caption("L'USO DELLO STRUMENTO È DISCREZIONALE. I RISULTATI COSTITUISCONO UNA GUIDA ALL'AUDIT BASATA SUI PESI CONTESTUALI E SULLA LOGICA INTERSEZIONALE.")

punti_sistema = 0.0
cluster_identita = 0
dettagli_audit = []

def audit_item(label, key, weight=1.0, is_identity=False, level_tag=""):
    global punti_sistema, cluster_identita
    col_check, col_note = st.columns([1, 1])
    with col_check:
        checked = st.checkbox(label.upper(), key=key)
    with col_note:
        if checked:
            punti_sistema += weight
            if is_identity: cluster_identita += 1
            note = st.text_input("EVIDENZA", key=f"n_{key}", placeholder="DETTAGLI...")
            if level_tag:
                dettagli_audit.append(f"[{level_tag}] {label.upper()}\n   NOTA: {note if note else 'NON SPECIFICATA'}")
    return checked

st.title("🛡️ IMAGES NAVIGATOR")
st.markdown("### SISTEMA INTEGRATO DI AUDIT PER L'INCLUSIVITÀ ALGORITMICA")

col_input, col_risultati = st.columns([0.6, 0.4], gap="large")

with col_input:
    tabs = st.tabs(["PREPARAZIONE", "PROCEDURA", "DATI", "TEAM", "MODELLO", "UTENTI", "CONTESTO", "OUTPUT"])

    with tabs[0]:
        st.subheader("PREPARAZIONE")
        audit_item("DEFINIZIONE CASO D'USO E TARGET", "s0_1")
        audit_item("SELEZIONE INDICATORI RILEVANTI", "s0_2")
        audit_item("DEFINIZIONE METRICHE", "s0_3")

    with tabs[1]:
        st.subheader("PROCEDURA")
        audit_item("ASSOCIAZIONE EVIDENZE", "s1_1")
        audit_item("IDENTIFICAZIONE CRITICITÀ", "s1_2")
        audit_item("VALIDAZIONE ITERATIVA", "s1_3")

    with tabs[2]:
        st.subheader("DATI")
        w_dati = 3.0 if dominio_scelto in ["SANITA E WELFARE", "GIUSTIZIA E SICUREZZA"] else 1.5
        audit_item("MANCATO CONFRONTO POPOLAZIONE REALE", "s2_1", weight=w_dati, is_identity=True, level_tag="DATI")
        audit_item("ETICHETTE STEREOTIPATE", "s2_2", weight=w_dati, level_tag="DATI")
        audit_item("ASSENZA RIEQUILIBRIO", "s2_3", weight=w_dati, is_identity=True, level_tag="DATI")

    with tabs[3]:
        st.subheader("TEAM")
        w_team = 2.5 if dominio_scelto == "RECRUITING E HR" else 1.5
        audit_item("OMOGENEITÀ DEMOGRAFICA", "s3_1", weight=w_team, level_tag="TEAM")
        audit_item("IDENTIFICAZIONE PROXY PROTETTI", "s3_2", weight=w_team, is_identity=True, level_tag="TEAM")
        audit_item("ASSENZA COMPETENZE DEI", "s3_3", weight=w_team, level_tag="TEAM")

    with tabs[4]:
        st.subheader("MODELLO")
        w_mod = 3.0 if dominio_scelto in ["SANITA E WELFARE", "FINANZA E CREDITO"] else 2.0
        audit_item("MANCATE METRICHE DISAGGREGATE", "s4_1", weight=w_mod, is_identity=True, level_tag="MODELLO")
        audit_item("ASSENZA TEST PROMPT SENSIBILI", "s4_2", weight=w_mod, is_identity=True, level_tag="MODELLO")
        audit_item("MODEL CARD NON AGGIORNATA", "s4_3", weight=w_mod, level_tag="MODELLO")

    with tabs[5]:
        st.subheader("UTENTI")
        w_ut = 3.0 if dominio_scelto == "MARKETING E MEDIA" else 1.5
        audit_item("MANCATA ANALISI ECHO-CHAMBER", "s5_1", weight=w_ut, level_tag="UTENTI")
        audit_item("ASSENZA CANALI SEGNALAZIONE", "s5_2", weight=w_ut, level_tag="UTENTI")
        audit_item("INTERFACCIA NON ACCESSIBILE", "s5_3", weight=w_ut, is_identity=True, level_tag="UTENTI")

    with tabs[6]:
        st.subheader("CONTESTO")
        audit_item("NON CONFORMITÀ NORMATIVA", "s6_1", weight=2.5, level_tag="CONTESTO")
        audit_item("ASSENZA GOVERNANCE PARTECIPATIVA", "s6_2", weight=2.0, level_tag="CONTESTO")

    with tabs[7]:
        st.subheader("CONTROLLO OUTPUT")
        v1 = st.checkbox("PATTERN VISIVI STEREOTIPATI", key="v1")
        t1 = st.checkbox("BIAS TESTUALI RILEVATI", key="t1")
        punti_img = 1 if v1 else 0
        punti_txt = 1 if t1 else 0

# CALCOLO E VISUALIZZAZIONE RISULTATI
moltiplicatore = DOMINI[dominio_scelto]["mult"] if cluster_identita > 1 else 1.0
punteggio_finale = punti_sistema * moltiplicatore
soglia = DOMINI[dominio_scelto]["threshold"]

with col_risultati:
    st.markdown(f"<div class='result-card'>", unsafe_allow_html=True)
    st.subheader("SCORECARD DI RISCHIO")
    
    st.markdown("**RISCHI SISTEMICI**")
    if punteggio_finale >= soglia:
        st.error(f"🔴 ALTO: {punteggio_finale:.1f} / {soglia}")
    elif punteggio_finale >= (soglia / 2):
        st.warning(f"🟡 MEDIO: {punteggio_finale:.1f} / {soglia}")
    else:
        st.success(f"🟢 BASSO: {punteggio_finale:.1f} / {soglia}")
    
    if moltiplicatore > 1.0:
        st.info(f"⚠️ **EFFETTO INTERSEZIONALE**\nMOLTIPLICATORE: x{moltiplicatore}")

    st.divider()
    st.markdown("**STATO OUTPUT**")
    st.write(f"VISIVO: {'🔴 CRITICO' if punti_img > 0 else '🟢 REGOLARE'}")
    st.write(f"TESTUALE: {'🔴 CRITICO' if punti_txt > 0 else '🟢 REGOLARE'}")
    
    st.markdown("</div>", unsafe_allow_html=True)

    report = f"AUDIT IMAGES - {dominio_scelto}\nVERDETTO: {punteggio_finale:.2f}"
    st.download_button("SCARICA REPORT", report, file_name=f"AUDIT_{dominio_scelto}.txt", use_container_width=True)
