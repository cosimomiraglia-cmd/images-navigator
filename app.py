import streamlit as st
from datetime import datetime

# CONFIGURAZIONE PAGINA
st.set_page_config(page_title="IMAGES NAVIGATOR", layout="wide", initial_sidebar_state="expanded")

# CUSTOM CSS PER ESTETICA AVANZATA
st.markdown("""
    <style>
    /* Sfondo e font generale */
    .main {
        background-color: #f8f9fa;
    }
    /* Stilizzazione dei Tab */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #ffffff;
        padding: 10px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        border-radius: 5px;
        background-color: #f1f3f5;
        border: none;
    }
    .stTabs [aria-selected="true"] {
        background-color: #228be6 !important;
        color: white !important;
    }
    /* Card per i risultati */
    .result-card {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        margin-bottom: 20px;
        border-left: 5px solid #228be6;
    }
    /* Etichette uniformi */
    h1, h2, h3, label, .stMarkdown {
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    </style>
    """, unsafe_allow_html=True)

# DATASET PESI E DOMINI
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

# SIDEBAR CONFIGURAZIONE
with st.sidebar:
    st.title("IMPOSTAZIONI")
    dominio_scelto = st.selectbox("DOMINIO APPLICATIVO", list(DOMINI.keys()))
    st.divider()
    st.markdown("🔍 **NOTA METODOLOGICA**")
    st.caption("L'USO DELLO STRUMENTO È DISCREZIONALE. I RISULTATI COSTITUISCONO UNA GUIDA ALL'AUDIT BASATA SUI PESI CONTESTUALI E SULLA LOGICA INTERSEZIONALE.")

# INIZIALIZZAZIONE LOGICA
punti_sistema = 0.0
cluster_identita = 0
dettagli_audit = []

def audit_item(label, key, weight=1.0, is_identity=False, level_tag=""):
    global punti_sistema, cluster_identita
    col_check, col_note = st.columns([1, 1])
    with col_check:
        checked = st.checkbox(label.upper(), key=key)
    with col_note:
        note = ""
        if checked:
            punti_sistema += weight
            if is_identity: cluster_identita += 1
            note = st.text_input("EVIDENZA / PIANO D'AZIONE", key=f"n_{key}", placeholder="INSERIRE DETTAGLI...")
            if level_tag:
                dettagli_audit.append(f"[{level_tag}] {label.upper()}\n   NOTA: {note if note else 'NON SPECIFICATA'}")
    return checked

# LAYOUT PRINCIPALE
st.title("🛡️ IMAGES NAVIGATOR")
st.markdown("### SISTEMA INTEGRATO DI AUDIT PER L'INCLUSIVITÀ ALGORITMICA")

col_input, col_risultati = st.columns([0.6, 0.4], gap="large")

with col_input:
    tabs = st.tabs(["PREPARAZIONE", "PROCEDURA", "DATI", "TEAM", "MODELLO", "UTENTI", "CONTESTO", "CONTROLLO OUTPUT"])

    with tabs[0]:
        st.subheader("PREPARAZIONE")
        audit_item("DEFINIZIONE CASO D'USO E GRUPPI COINVOLTI", "s0_1")
        audit_item("SELEZIONE INDICATORI RILEVANTI", "s0_2")
        audit_item("DEFINIZIONE METRICHE DI MISURAZIONE", "s0_3")
        audit_item("COINVOLGIMENTO STAKEHOLDER", "s0_4")

    with tabs[1]:
        st.subheader("PROCEDURA")
        audit_item("SELEZIONE CONTESTUALE INDICATORI", "s1_1")
        audit_item("ASSOCIAZIONE EVIDENZE VERIFICABILI", "s1_2")
        audit_item("IDENTIFICAZIONE CRITICITÀ BIAS", "s1_3")
        audit_item("PONDERAZIONE IMPATTI UMANI", "s1_4")
        audit_item("PIANIFICAZIONE VALIDAZIONE ITERATIVA", "s1_5")

    with tabs[2]:
        st.subheader("DATI")
        w_dati = 3.0 if dominio_scelto in ["SANITA E WELFARE", "GIUSTIZIA E SICUREZZA"] else 1.5
        audit_item("MANCATO CONFRONTO CON POPOLAZIONE REALE", "s2_1", weight=w_dati, is_identity=True, level_tag="DATI")
        audit_item("PRESENZA ETICHETTE STEREOTIPATE", "s2_2", weight=w_dati, level_tag="DATI")
        audit_item("ASSENZA STRATEGIE DI RIEQUILIBRIO", "s2_3", weight=w_dati, is_identity=True, level_tag="DATI")
        audit_item("MANCANZA DATA SHEET O DOCUMENTAZIONE RISCHI", "s2_4", weight=w_dati, level_tag="DATI")

    with tabs[3]:
        st.subheader("TEAM")
        w_team = 2.5 if dominio_scelto == "RECRUITING E HR" else 1.5
        audit_item("OMOGENEITÀ DEMOGRAFICA DEL TEAM", "s3_1", weight=w_team, level_tag="TEAM")
        audit_item("IDENTIFICAZIONE PROXY CATEGORIE PROTETTE", "s3_2", weight=w_team, is_identity=True, level_tag="TEAM")
        audit_item("ASSENZA COMPETENZE DEI O SOCIOLOGICHE", "s3_3", weight=w_team, level_tag="TEAM")
        audit_item("MANCANZA REGISTRO DECISIONALE", "s3_4", weight=w_team, level_tag="TEAM")

    with tabs[4]:
        st.subheader("MODELLO")
        w_mod = 3.0 if dominio_scelto in ["SANITA E WELFARE", "FINANZA E CREDITO"] else 2.0
        audit_item("MANCATO CALCOLO METRICHE DISAGGREGATE", "s4_1", weight=w_mod, is_identity=True, level_tag="MODELLO")
        audit_item("ASSENZA TEST CON PROMPT SENSIBILI", "s4_2", weight=w_mod, is_identity=True, level_tag="MODELLO")
        audit_item("MANCATA APPLICAZIONE TECNICHE MITIGAZIONE", "s4_3", weight=w_mod, level_tag="MODELLO")
        audit_item("MODEL CARD NON AGGIORNATA", "s4_4", weight=w_mod, level_tag="MODELLO")

    with tabs[5]:
        st.subheader("UTENTI")
        w_ut = 3.0 if dominio_scelto == "MARKETING E MEDIA" else 1.5
        audit_item("ASSENZA MONITORAGGIO COMPORTAMENTI ABUSIVI", "s5_1", weight=w_ut, level_tag="UTENTI")
        audit_item("MANCATA ANALISI ECHO-CHAMBER", "s5_2", weight=w_ut, level_tag="UTENTI")
        audit_item("ASSENZA CANALI DI SEGNALAZIONE ESITI INGIUSTI", "s5_3", weight=w_ut, level_tag="UTENTI")
        audit_item("INTERFACCIA NON ACCESSIBILE", "s5_4", weight=w_ut, is_identity=True, level_tag="UTENTI")

    with tabs[6]:
        st.subheader("CONTESTO")
        audit_item("NON CONFORMITÀ NORMATIVA (AI ACT/GDPR)", "s6_1", weight=2.5, level_tag="CONTESTO")
        audit_item("ASSENZA GOVERNANCE PARTECIPATIVA", "s6_2", weight=2.0, level_tag="CONTESTO")
        audit_item("MANCANZA VALUTAZIONI D'IMPATTO PERIODICHE", "s6_3", weight=2.0, level_tag="CONTESTO")

    with tabs[7]:
        st.subheader("CONTROLLO OUTPUT")
        st.markdown("#### ANALISI VISIVA")
        v1 = st.checkbox("DONNE IN RUOLI PASSIVI O DECORATIVI", key="v1")
        v2 = st.checkbox("UOMINI IN RUOLI DOMINANTI", key="v2")
        v3 = st.checkbox("SOTTORAPPRESENTAZIONE ETNICA", key="v3")
        punti_img = sum([v1, v2, v3])
        st.divider()
        st.markdown("#### ANALISI TESTUALE")
        t1 = st.checkbox("USO DEL MASCHILE SOVRAESTESO", key="t1")
        t2 = st.checkbox("STEREOTIPI O METAFORE DEGRADANTI", key="t2")
        punti_txt = sum([t1, t2])

# CALCOLO RISULTATI
moltiplicatore = DOMINI[dominio_scelto]["mult"] if cluster_identita > 1 else 1.0
punteggio_finale = punti_sistema * moltiplicatore
soglia = DOMINI[dominio_scelto]["threshold"]

with col_risultati:
    st.markdown(f"<div class='result-card'>", unsafe_allow_html=True)
    st.subheader("SCORECARD DI RISCHIO")
    
    # RISCHI SISTEMICI
    st.markdown("**RISCHI SISTEMICI**")
    if punteggio_finale >= soglia:
        st.error(f"🔴 RISCHIO ALTO: {punteggio_finale:.1f} / {soglia}")
    elif punteggio_finale >= (soglia / 2):
        st.warning(f"🟡 RISCHIO MEDIO: {punteggio_finale:.1f} / {soglia}")
    else:
        st.success(f"🟢 RISCHIO BASSO: {punteggio_finale:.1f} / {soglia}")
    
    if moltiplicatore > 1.0:
        st.info(f"⚠️ **EFFETTO INTERSEZIONALE ATTIVO**\nMOLTIPLICATORE APPLICATO: x{moltiplicatore}")

    st.divider()

    # OUTPUT CHECK
    st.markdown("**CONTROLLO OUTPUT**")
    c_img = "🔴 CRITICO" if punti_img >= 2 else "🟢 REGOLARE"
    st.write(f"IMMAGINI: {c_img}")
    
    c_txt = "🔴 CRITICO" if punti_txt >= 1 else "🟢 REGOLARE"
    st.write(f"TESTI: {c_txt}")
    
    st.markdown("</div>", unsafe_allow_html=True)

    # REPORT DOWNLOAD
    report = f"""REPORT TECNICO IMAGES - {dominio_scelto}
DATA: {datetime.now().strftime('%d/%m/%Y %H:%M')}
--------------------------------------------------
VERDETTO SISTEMA: {punteggio_finale:.2f} / {soglia}
MOLTIPLICATORE INTERSEZIONALE: {moltiplicatore}
--------------------------------------------------
DETTAGLIO AUDIT:
""" + "\n".join(dettagli_audit)

    st.download_button("SCARICA REPORT TECNICO", report, file_name=f"AUDIT_{dominio_scelto}.txt", use_container_width=True)

st.divider()
st.caption("SVILUPPATO NEL QUADRO DEL PROGETTO PRIN PNRR - TUTTI I DIRITTI RISERVATI")
