import streamlit as st
from datetime import datetime

# CONFIGURAZIONE PAGINA
st.set_page_config(page_title="IMAGES NAVIGATOR", layout="wide", initial_sidebar_state="expanded")

# --- PALETTE UFFICIALE PROGETTO ---
C_PRIMARY = "#e3286d"   # MAGENTA ACCENTO
C_DARK = "#565656"      # GRIGIO SCURO (TESTI)
C_MEDIUM = "#a5a5a5"    # GRIGIO MEDIO (BORDI/INATTIVI)
C_BG = "#e2ddd9"        # BEIGE CHIARO (SFONDO)

# CUSTOM CSS AVANZATO
st.markdown(f"""
    <style>
    /* Sfondo generale dell'app */
    .stApp {{
        background-color: {C_BG};
    }}
    
    /* STILIZZAZIONE TAB: AMPIEZZA E MARGINI */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 20px; 
        background-color: transparent;
        padding: 15px 0px;
    }}

    .stTabs [data-baseweb="tab"] {{
        height: 65px; 
        min-width: 160px; 
        border-radius: 12px;
        background-color: white;
        border: 2px solid {C_MEDIUM};
        padding: 0px 30px; 
        transition: all 0.4s ease;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }}

    /* Testo nei Tab */
    .stTabs [data-baseweb="tab"] p {{
        font-size: 15px;
        font-weight: 700;
        text-transform: uppercase;
        color: {C_DARK};
    }}

    /* Tab attivo */
    .stTabs [aria-selected="true"] {{
        background-color: {C_PRIMARY} !important;
        border-color: {C_PRIMARY} !important;
        transform: translateY(-3px);
        box-shadow: 0 8px 15px rgba(227, 40, 109, 0.2);
    }}
    
    .stTabs [aria-selected="true"] p {{
        color: white !important;
    }}

    /* Card laterale dei risultati */
    .result-card {{
        background-color: white;
        padding: 30px;
        border-radius: 20px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        border-top: 8px solid {C_PRIMARY};
        margin-top: 10px;
    }}

    /* Uniformità etichette: tutto MAIUSCOLO */
    h1, h2, h3, h4, label, .stMarkdown p, .stButton button {{
        text-transform: uppercase;
        letter-spacing: 1px;
        color: {C_DARK};
    }}

    /* Input evidenze */
    .stTextInput input {{
        border-radius: 8px;
        border: 1px solid {C_MEDIUM};
    }}
    </style>
    """, unsafe_allow_html=True)

# LOGICA DOMINI E PESI
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

# SIDEBAR
with st.sidebar:
    st.markdown(f"<h2 style='color:{C_PRIMARY};'>IMPOSTAZIONI</h2>", unsafe_allow_html=True)
    dominio_scelto = st.selectbox("DOMINIO APPLICATIVO", list(DOMINI.keys()))
    st.divider()
    st.markdown("**NOTA METODOLOGICA**")
    st.caption("LO STRUMENTO OPERA SECONDO IL MODELLO FOUR LEVELS (+1). I RISULTATI SONO BASATI SUL PRINCIPIO DI PONDERAZIONE DINAMICA.")

# INIZIALIZZAZIONE VARIABILI
punti_sistema = 0.0
cluster_identita = 0
dettagli_audit = []

def audit_item(label, key, weight=1.0, is_identity=False, tag=""):
    global punti_sistema, cluster_identita
    c1, c2 = st.columns([1.2, 1])
    with c1:
        checked = st.checkbox(label.upper(), key=key)
    with c2:
        if checked:
            punti_sistema += weight
            if is_identity: cluster_identita += 1
            nota = st.text_input("EVIDENZA", key=f"n_{key}", placeholder="...").upper()
            if tag: dettagli_audit.append(f"[{tag}] {label.upper()} | NOTA: {nota}")
    return checked

# LAYOUT PRINCIPALE
st.markdown(f"<h1 style='color:{C_PRIMARY};'>🛡️ IMAGES NAVIGATOR</h1>", unsafe_allow_html=True)
st.markdown("##### SISTEMA DI AUDIT PER L'INCLUSIVITÀ ALGORITMICA")

col_input, col_risultati = st.columns([0.65, 0.35], gap="large")

with col_input:
    tabs = st.tabs(["PREPARAZIONE", "DATI", "TEAM", "MODELLO", "UTENTI", "CONTESTO", "OUTPUT"])

    with tabs[0]:
        st.subheader("PREPARAZIONE")
        audit_item("DEFINIZIONE CASO D'USO E TARGET", "p1")
        audit_item("SELEZIONE INDICATORI RILEVANTI", "p2")

    with tabs[1]:
        st.subheader("LIVELLO DATI")
        w = 3.0 if dominio_scelto in ["SANITA E WELFARE", "GIUSTIZIA E SICUREZZA"] else 1.5
        audit_item("MANCATO CONFRONTO POPOLAZIONE REALE", "d1", w, True, "DATI")
        audit_item("PRESENZA ETICHETTE STEREOTIPATE", "d2", w, False, "DATI")
        audit_item("ASSENZA STRATEGIE RIEQUILIBRIO", "d3", w, True, "DATI")

    with tabs[2]:
        st.subheader("LIVELLO TEAM")
        w = 2.5 if dominio_scelto == "RECRUITING E HR" else 1.5
        audit_item("OMOGENEITÀ DEMOGRAFICA TEAM", "t1", w, False, "TEAM")
        audit_item("IDENTIFICAZIONE PROXY GRUPPI PROTETTI", "t2", w, True, "TEAM")
        audit_item("MANCANZA COMPETENZE SOCIALI/DEI", "t3", w, False, "TEAM")

    with tabs[3]:
        st.subheader("LIVELLO MODELLO")
        w = 3.0 if dominio_scelto in ["SANITA E WELFARE", "FINANZA E CREDITO"] else 2.0
        audit_item("MANCATE METRICHE DISAGGREGATE", "m1", w, True, "MODELLO")
        audit_item("ASSENZA TEST PROMPT SENSIBILI", "m2", w, True, "MODELLO")
        audit_item("MODEL CARD NON AGGIORNATA", "m3", w, False, "MODELLO")

    with tabs[4]:
        st.subheader("LIVELLO UTENTI")
        w = 3.0 if dominio_scelto == "MARKETING E MEDIA" else 1.5
        audit_item("MANCATA ANALISI ECHO-CHAMBER", "u1", w, False, "UTENTI")
        audit_item("ASSENZA CANALI SEGNALAZIONE", "u2", w, False, "UTENTI")
        audit_item("INTERFACCIA NON ACCESSIBILE", "u3", w, True, "UTENTI")

    with tabs[5]:
        st.subheader("LIVELLO CONTESTO")
        audit_item("NON CONFORMITÀ NORMATIVA", "c1", 2.5, False, "CONTESTO")
        audit_item("ASSENZA GOVERNANCE PARTECIPATIVA", "c2", 2.0, False, "CONTESTO")

    with tabs[6]:
        st.subheader("CONTROLLO OUTPUT")
        st.write("RILEVAZIONE PATTERN DISCRIMINATORI")
        out1 = st.checkbox("PATTERN VISIVI STEREOTIPATI", key="out1")
        out2 = st.checkbox("BIAS TESTUALI RILEVATI", key="out2")
        p_img = 1 if out1 else 0
        p_txt = 1 if out2 else 0

# CALCOLI FINALI
molt = DOMINI[dominio_scelto]["mult"] if cluster_identita > 1 else 1.0
score = punti_sistema * molt
threshold = DOMINI[dominio_scelto]["threshold"]

with col_risultati:
    st.markdown("<div class='result-card'>", unsafe_allow_html=True)
    st.subheader("SCORECARD")
    
    st.markdown("**RISCHI SISTEMICI**")
    if score >= threshold:
        st.error(f"🔴 ALTO: {score:.1f} / {threshold}")
    elif score >= (threshold / 2):
        st.warning(f"🟡 MEDIO: {score:.1f} / {threshold}")
    else:
        st.success(f"🟢 BASSO: {score:.1f} / {threshold}")
    
    if molt > 1.0:
        st.markdown(f"<p style='color:{C_PRIMARY}; font-weight:bold;'>⚠️ EFFETTO INTERSEZIONALE ATTIVO (x{molt})</p>", unsafe_allow_html=True)

    st.divider()
    st.markdown("**VALIDAZIONE OUTPUT**")
    st.write(f"VISIVO: {'🔴 CRITICO' if p_img > 0 else '🟢 REGOLARE'}")
    st.write(f"TESTUALE: {'🔴 CRITICO' if p_txt > 0 else '🟢 REGOLARE'}")
    
    st.markdown("</div>", unsafe_allow_html=True)

    # DOWNLOAD REPORT
    report_data = f"AUDIT IMAGES - {dominio_scelto}\nSCORE: {score:.2f}\n------------------\n" + "\n".join(dettagli_audit)
    st.download_button("SCARICA REPORT TECNICO", report_data, file_name=f"AUDIT_{dominio_scelto}.txt", use_container_width=True)

st.divider()
st.caption(f"PROGETTO PRIN PNRR | IMAGES NAVIGATOR | 2026")
