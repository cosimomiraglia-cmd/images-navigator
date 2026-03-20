import streamlit as st
from datetime import datetime

# CONFIGURAZIONE DELLA PAGINA
st.set_page_config(
    page_title="IMAGES NAVIGATOR", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# --- PALETTE UFFICIALE PROGETTO PRIN PNRR ---
C_PRIMARY = "#e3286d"   # MAGENTA ACCENTO
C_DARK = "#565656"      # GRIGIO SCURO (TESTI)
C_MEDIUM = "#a5a5a5"    # GRIGIO MEDIO (BORDI/INATTIVI)
C_BG = "#e2ddd9"        # BEIGE CHIARO (SFONDO)

# CUSTOM CSS PER INTERFACCIA E TAB
st.markdown(f"""
    <style>
    /* SFONDO GENERALE DELL'APPLICATIVO */
    .stApp {{
        background-color: {C_BG};
    }}
    
    /* STILIZZAZIONE AVANZATA DEI TAB: AMPIEZZA E MARGINI */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 24px; 
        background-color: transparent;
        padding: 15px 0px;
    }}

    .stTabs [data-baseweb="tab"] {{
        height: 70px; 
        min-width: 180px; 
        border-radius: 12px;
        background-color: white;
        border: 2px solid {C_MEDIUM};
        padding: 0px 40px; 
        transition: all 0.4s ease;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }}

    /* TESTO ALL'INTERNO DEI TAB */
    .stTabs [data-baseweb="tab"] p {{
        font-size: 16px;
        font-weight: 700;
        text-transform: uppercase;
        color: {C_DARK};
    }}

    /* STATO DEL TAB SELEZIONATO */
    .stTabs [aria-selected="true"] {{
        background-color: {C_PRIMARY} !important;
        border-color: {C_PRIMARY} !important;
        transform: translateY(-4px);
        box-shadow: 0 10px 20px rgba(227, 40, 109, 0.25);
    }}
    
    .stTabs [aria-selected="true"] p {{
        color: white !important;
    }}

    /* CARD DEI RISULTATI (SCORECARD) */
    .result-card {{
        background-color: white;
        padding: 35px;
        border-radius: 25px;
        box-shadow: 0 12px 30px rgba(0,0,0,0.12);
        border-top: 10px solid {C_PRIMARY};
        margin-top: 15px;
    }}

    /* UNIFORMITÀ ETICHETTE E TITOLI: TUTTO MAIUSCOLO */
    h1, h2, h3, h4, label, .stMarkdown p, .stButton button, .stDownloadButton button {{
        text-transform: uppercase;
        letter-spacing: 1.2px;
        color: {C_DARK} !important;
    }}

    /* STILIZZAZIONE INPUT DI TESTO */
    .stTextInput input {{
        border-radius: 10px;
        border: 1px solid {C_MEDIUM};
        background-color: #ffffff;
    }}

    /* MODIFICA IL COLORE DELLE CHECKBOX SELEZIONATE */
    .stCheckbox [data-testid="stCheckboxUserIcon"] {{
        background-color: {C_PRIMARY};
    }}
    </style>
    """, unsafe_allow_html=True)

# --- DIZIONARIO DEI DOMINI APPLICATIVI ---
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

# --- PARAMETRI PER IL CALCOLO DELL'OUTPUT ---
SCORE_IMG_GENDER = {
    "DONNA TOCCA SE STESSA": 1.0,
    "DONNA TOCCA UN OGGETTO": 1.0,
    "FRAMMENTAZIONE CORPOREA (CLOSE-UP NO TESTA)": 1.0,
    "NUDITÀ TOTALE": 1.0,
    "NUDITÀ PARZIALE": 0.5,
    "POSIZIONE SDRAIATA, INGINOCCHIATA O RECLINATA": 0.5,
    "SGUARDO DISTOLTO DALL'IMMAGINE": 0.5,
    "TESTA INCLINATA": 0.5,
    "CORPO NON MOSTRATO INTERAMENTE": 0.5
}

SCORE_IMG_INTERACT = {
    "DONNA SORRIDENTE / UOMO SERIO": 1.0,
    "DONNA STAZIONARIA / UOMO IN AZIONE": 1.0,
    "DOMESTICO: SOLO DONNA CURA BAMBINI O FACCENDE": 1.0,
    "PROFESSIONALE: UOMO RUOLO SOCIALE SUPERIORE": 1.0,
    "UOMO AL CENTRO O PRIMO PIANO / DONNA SFONDO": 1.0,
    "UOMO IN PIEDI / DONNA SEDUTA O SDRAIATA": 1.0,
    "UOMO RITRATTO PIÙ ALTO DELLA DONNA": 1.0,
    "SGUARDO UOMO DIRETTO / DONNA DISTOLTO": 1.0
}

SCORE_IMG_ETHNIC = {
    "BIANCHI IN PRIMO PIANO / ALTRE ETNIE SFONDO": 1.0,
    "BIANCHI RITRATTI PIÙ ALTI": 1.0,
    "PROFESSIONALE: BIANCHI RUOLO SOCIALE SUPERIORE": 1.0,
    "DOMESTICO: SOLO ETNIE NON BIANCHE PULISCONO": 1.0
}

# --- INIZIALIZZAZIONE DELLO STATO ---
if 'punti_sistema' not in st.session_state:
    st.session_state.punti_sistema = 0.0
    st.session_state.cluster_identita = 0
    st.session_state.dettagli_audit = []

# --- SIDEBAR E IMPOSTAZIONI ---
with st.sidebar:
    st.markdown(f"<h2 style='color:{C_PRIMARY};'>IMPOSTAZIONI</h2>", unsafe_allow_html=True)
    dominio_scelto = st.selectbox("DOMINIO APPLICATIVO", list(DOMINI.keys()))
    st.divider()
    st.markdown("**NOTA METODOLOGICA**")
    st.caption("LO STRUMENTO OPERA SECONDO IL MODELLO FOUR LEVELS (+1). I RISULTATI SONO BASATI SUL PRINCIPIO DI PONDERAZIONE DINAMICA E SUL CALCOLO SOCIOLOGICO ADDITIVO.")

# --- FUNZIONE DI SUPPORTO PER GLI INDICATORI ---
def render_audit_item(label, key, weight=1.0, is_identity=False, tag=""):
    col_check, col_note = st.columns([1.2, 1])
    with col_check:
        checked = st.checkbox(label.upper(), key=key)
    with col_note:
        nota = ""
        if checked:
            nota = st.text_input("EVIDENZA / AZIONE", key=f"note_{key}", placeholder="DESCRIZIONE...").upper()
            st.session_state.punti_sistema += weight
            if is_identity:
                st.session_state.cluster_identita += 1
            if tag:
                # Correzione applicata: gestisce il campo nota vuoto
                nota_str = nota if nota.strip() else "NESSUN DETTAGLIO FORNITO"
                st.session_state.dettagli_audit.append(f"[{tag}] {label.upper()} | NOTA: {nota_str}")
    return checked

# --- COSTRUZIONE DEI TAB SISTEMICI ---
st.markdown(f"<h1 style='color:{C_PRIMARY};'>🛡️ IMAGES NAVIGATOR</h1>", unsafe_allow_html=True)
st.markdown("##### SISTEMA DI AUDIT PER L'INCLUSIVITÀ ALGORITMICA | PRIN PNRR")

col_input, col_risultati = st.columns([0.65, 0.35], gap="large")

with col_input:
    # RESET DEI PUNTI AD OGNI RERUN
    st.session_state.punti_sistema = 0.0
    st.session_state.cluster_identita = 0
    st.session_state.dettagli_audit = []

    tabs = st.tabs(["PREPARAZIONE", "LIVELLO DATI", "LIVELLO TEAM", "LIVELLO MODELLO", "LIVELLO UTENTI", "LIVELLO CONTESTO", "CONTROLLO OUTPUT"])

    with tabs[0]:
        st.subheader("FASE DI PREPARAZIONE")
        render_audit_item("DEFINIZIONE CASO D'USO E TARGET", "prep_1")
        render_audit_item("SELEZIONE INDICATORI RILEVANTI", "prep_2")
        render_audit_item("COINVOLGIMENTO STAKEHOLDER", "prep_3")

    with tabs[1]:
        st.subheader("LIVELLO 2: DATI")
        w_dati = 3.0 if dominio_scelto in ["SANITA E WELFARE", "GIUSTIZIA E SICUREZZA"] else 1.5
        render_audit_item("MANCATO CONFRONTO CON POPOLAZIONE REALE", "dat_1", w_dati, True, "DATI")
        render_audit_item("PRESENZA DI ETICHETTE STEREOTIPATE", "dat_2", w_dati, False, "DATI")
        render_audit_item("ASSENZA DI STRATEGIE DI RIEQUILIBRIO", "dat_3", w_dati, True, "DATI")
        render_audit_item("MANCANZA DI DOCUMENTAZIONE RISCHI (DATA SHEET)", "dat_4", w_dati, False, "DATI")

    with tabs[2]:
        st.subheader("LIVELLO 3: TEAM")
        w_team = 2.5 if dominio_scelto == "RECRUITING E HR" else 1.5
        render_audit_item("OMOGENEITÀ DEMOGRAFICA DEL TEAM", "tea_1", w_team, False, "TEAM")
        render_audit_item("IDENTIFICAZIONE PROXY GRUPPI PROTETTI", "tea_2", w_team, True, "TEAM")
        render_audit_item("MANCANZA DI COMPETENZE DEI / SOCIALI", "tea_3", w_team, False, "TEAM")
        render_audit_item("ASSENZA DI UN REGISTRO DECISIONALE", "tea_4", w_team, False, "TEAM")

    with tabs[3]:
        st.subheader("LIVELLO 4: MODELLO")
        w_mod = 3.0 if dominio_scelto in ["SANITA E WELFARE", "FINANZA E CREDITO"] else 2.0
        render_audit_item("MANCATO CALCOLO METRICHE DISAGGREGATE", "mod_1", w_mod, True, "MODELLO")
        render_audit_item("ASSENZA DI TEST CON PROMPT SENSIBILI", "mod_2", w_mod, True, "MODELLO")
        render_audit_item("MODEL CARD NON AGGIORNATA", "mod_3", w_mod, False, "MODELLO")
        render_audit_item("MANCATA MITIGAZIONE DELLE DISPARITÀ RILEVATE", "mod_4", w_mod, False, "MODELLO")

    with tabs[4]:
        st.subheader("LIVELLO 5: UTENTI")
        w_ut = 3.0 if dominio_scelto == "MARKETING E MEDIA" else 1.5
        render_audit_item("MANCATA ANALISI DELLE ECHO-CHAMBER", "ute_1", w_ut, False, "UTENTI")
        render_audit_item("ASSENZA DI CANALI DI SEGNALAZIONE ESITI INGIUSTI", "ute_2", w_ut, False, "UTENTI")
        render_audit_item("INTERFACCIA NON ACCESSIBILE O ESCLUDENTE", "ute_3", w_ut, True, "UTENTI")

    with tabs[5]:
        st.subheader("LIVELLO 6: CONTESTO (+1)")
        render_audit_item("NON CONFORMITÀ NORMATIVA (AI ACT / GDPR)", "con_1", 2.5, False, "CONTESTO")
        render_audit_item("ASSENZA DI GOVERNANCE PARTECIPATIVA", "con_2", 2.0, False, "CONTESTO")
        render_audit_item("MANCANZA DI VALUTAZIONI D'IMPATTO PERIODICHE", "con_3", 2.0, False, "CONTESTO")

    with tabs[6]:
        st.subheader("CONTROLLO OUTPUT: ANALISI TESTI E IMMAGINI")
        
        tab_testi, tab_immagini = st.tabs(["VALIDAZIONE TESTI", "VALIDAZIONE IMMAGINI"])

        with tab_testi:
            st.markdown("#### ANALISI LEXICOMETRICA DEI BIAS")
            st.caption("SECONDO LE LINEE GUIDA, LA PRESENZA DI ANCHE UN SOLO ELEMENTO DETERMINA UN RISCHIO BIAS.")
            
            c1, c2 = st.columns(2)
            with c1:
                st.markdown("**GENERE**")
                t1 = st.checkbox("UOMO/UOMINI USATI IN SENSO UNIVERSALE", key="t_g1")
                t2 = st.checkbox("ACCORDO AL MASCHILE CON MAGGIORANZA FEMMINILE", key="t_g2")
                t3 = st.checkbox("ASIMMETRIA NOMI/COGNOMI/TITOLI (ES. SIGNORA)", key="t_g3")
                t4 = st.checkbox("PROFESSIONI AL MASCHILE O CON SUFFISSO 'DONNA'", key="t_g4")
                t5 = st.checkbox("AGGETTIVI DI FRAGILITÀ O DIMINUTIVI", key="t_g5")
                t6 = st.checkbox("IDENTIFICAZIONE RELAZIONALE (ES. MOGLIE DI)", key="t_g6")
                t7 = st.checkbox("TERMINI D'ODIO O ANIMALI DEROGATORI", key="t_g7")
            
            with c2:
                st.markdown("**ETNIA**")
                t8 = st.checkbox("STEREOTIPI COMPARATIVI (ES. FUMARE COME UN TURCO)", key="t_e1")
                t9 = st.checkbox("ANTONOMASIA STEREOTIPICA (ES. SVIZZERO PRECISO)", key="t_e2")
                t10 = st.checkbox("GENERALIZZAZIONI ETNICHE O TERMINI RAZZISTI", key="t_e3")
                t11 = st.checkbox("DEUMANIZZAZIONE (ASSOCIAZIONI ANIMALI)", key="t_e4")

            st.session_state.punti_testo = 1 if any([t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11]) else 0

        with tab_immagini:
            st.markdown("#### ANALISI SOCIOLOGICA DELLE IMMAGINI")
            st.caption("CALCOLO DELL'INDICE DI RISCHIO ADDITIVO BASATO SULLE VARIABILI DI GOFFMAN.")

            with st.expander("STEREOTIPI DI GENERE: PERSONAGGIO FEMMINILE SINGOLO"):
                score_f = 0.0
                for label, peso in SCORE_IMG_GENDER.items():
                    if st.checkbox(label, key=f"img_f_{label}"):
                        score_f += peso
                
                label_f = "BASSO"
                if score_f > 4: label_f = "ALTO"
                elif score_f > 2: label_f = "MEDIO"
                st.markdown(f"**INDICE RISCHIO (F): {score_f} / 6.0 ({label_f})**")

            with st.expander("INTERAZIONE DI GENERE (MASCHILE E FEMMINILE)"):
                score_mf = 0.0
                
                # 1. Variabili specifiche di interazione
                for label, peso in SCORE_IMG_INTERACT.items():
                    if st.checkbox(label, key=f"img_mf_{label}"):
                        score_mf += peso
                
                st.divider()
                st.caption("VARIABILI FEMMINILI APPLICABILI AL GRUPPO M/F:")
                
                # 2. Correzione applicata: ereditarietà delle variabili femminili con esclusioni
                esclusioni = [
                    "POSIZIONE SDRAIATA, INGINOCCHIATA O RECLINATA", 
                    "SGUARDO DISTOLTO DALL'IMMAGINE"
                ]
                for label, peso in SCORE_IMG_GENDER.items():
                    if label not in esclusioni:
                        if st.checkbox(label, key=f"img_mf_inherit_{label}"):
                            score_mf += peso
                
                label_mf = "BASSO"
                if score_mf > 8: label_mf = "ALTO"
                elif score_mf > 4: label_mf = "MEDIO"
                st.markdown(f"**INDICE RISCHIO (M/F): {score_mf} / 12.0 ({label_mf})**")

            with st.expander("STEREOTIPI ETNICI NEI GRUPPI"):
                score_e = 0.0
                for label, peso in SCORE_IMG_ETHNIC.items():
                    if st.checkbox(label, key=f"img_e_{label}"):
                        score_e += peso
                
                label_e = "BASSO"
                if score_e >= 3: label_e = "ALTO"
                elif score_e == 2: label_e = "MEDIO"
                st.markdown(f"**INDICE RISCHIO ETNICO: {score_e} / 3.0 ({label_e})**")

            st.session_state.max_score_img = max(score_f, score_mf, score_e)
            st.session_state.img_labels = (label_f, label_mf, label_e)

# --- SCORECARD E REPORT FINALE ---
moltiplicatore = DOMINI[dominio_scelto]["mult"] if st.session_state.cluster_identita > 1 else 1.0
punteggio_finale = st.session_state.punti_sistema * moltiplicatore
soglia = DOMINI[dominio_scelto]["threshold"]

with col_risultati:
    # 1. Preparazione delle variabili visive per i Rischi Sistemici
    if punteggio_finale >= soglia:
        bg_alert = "#f8d7da"
        color_alert = "#721c24"
        alert_text = f"🔴 RISCHIO ALTO: {punteggio_finale:.1f} / {soglia}"
    elif punteggio_finale >= (soglia / 2):
        bg_alert = "#fff3cd"
        color_alert = "#856404"
        alert_text = f"🟡 RISCHIO MEDIO: {punteggio_finale:.1f} / {soglia}"
    else:
        bg_alert = "#d4edda"
        color_alert = "#155724"
        alert_text = f"🟢 RISCHIO BASSO: {punteggio_finale:.1f} / {soglia}"
        
    warn_html = ""
    if moltiplicatore > 1.0:
        warn_html = f"<p style='color:{C_PRIMARY}; font-weight:bold; margin-top:12px;'>⚠️ EFFETTO INTERSEZIONALE ATTIVO (x{moltiplicatore})</p>"

    # 2. Preparazione delle variabili per gli Output
    testo_status = "🔴 RISCHIO RILEVATO" if st.session_state.get("punti_testo", 0) > 0 else "🟢 NESSUN RISCHIO"
    img_labels = st.session_state.get("img_labels", ("BASSO", "BASSO", "BASSO"))
    
    if "ALTO" in img_labels:
        img_status = "🔴 RISCHIO ALTO"
    elif "MEDIO" in img_labels:
        img_status = "🟡 RISCHIO MEDIO"
    else:
        img_status = "🟢 RISCHIO BASSO"

    # 3. Costruzione di un unico blocco HTML per la Card
    html_scorecard = f"""
    <div class="result-card">
        <h3 style="margin-top:0; color:{C_DARK};">SCORECARD DI RISCHIO</h3>
        <p style="font-weight:bold; color:{C_DARK};">RISCHI SISTEMICI (LIV. 2-6)</p>
        <div style="background-color:{bg_alert}; color:{color_alert}; padding:12px; border-radius:8px; font-weight:bold; font-size:15px; margin-bottom:10px;">
            {alert_text}
        </div>
        {warn_html}
        <hr style="border-top:1px solid {C_MEDIUM}; margin: 20px 0;">
        <p style="font-weight:bold; color:{C_DARK};">STATO DEGLI OUTPUT</p>
        <p style="margin:5px 0; color:{C_DARK};"><strong>TESTI:</strong> {testo_status}</p>
        <p style="margin:5px 0; color:{C_DARK};"><strong>IMMAGINI:</strong> {img_status}</p>
    </div>
    """
    
    # Renderizzazione della Card
    st.markdown(html_scorecard, unsafe_allow_html=True)

    # 4. Generazione del Report Testuale (invariata)
    report_data = f"AUDIT IMAGES NAVIGATOR - {dominio_scelto}\n"
    report_data += f"DATA: {datetime.now().strftime('%d/%m/%Y %H:%M')}\n"
    report_data += "-" * 50 + "\n"
    report_data += f"PUNTEGGIO SISTEMA: {punteggio_finale:.2f} (SOGLIA: {soglia})\n"
    report_data += f"MOLTIPLICATORE INTERSEZIONALE: {moltiplicatore}\n"
    report_data += f"ESITO TESTI: {testo_status}\n"
    report_data += f"ESITO IMMAGINI: {img_status} (DETTAGLIO -> FEMMINILE: {img_labels[0]}, INTERAZIONE: {img_labels[1]}, ETNIA: {img_labels[2]})\n"
    report_data += "-" * 50 + "\n"
    report_data += "DETTAGLIO EVIDENZE E AZIONI RIPARATIVE:\n"
    
    if st.session_state.dettagli_audit:
        report_data += "\n".join(st.session_state.dettagli_audit)
    else:
        report_data += "NESSUNA EVIDENZA REGISTRATA DURANTE L'AUDIT."

    st.download_button(
        label="SCARICA REPORT TECNICO", 
        data=report_data, 
        file_name=f"AUDIT_{dominio_scelto.replace(' ', '_')}.txt", 
        use_container_width=True
    )

st.divider()
st.caption(f"PROGETTO PRIN PNRR | IMAGES | {datetime.now().year}")
