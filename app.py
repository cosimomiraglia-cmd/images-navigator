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
    
    /* STILIZZAZIONE AVANZATA DEI TAB */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 15px; 
        background-color: transparent;
        padding: 15px 0px;
    }}

    .stTabs [data-baseweb="tab"] {{
        height: 65px; 
        border-radius: 10px;
        background-color: white;
        border: 2px solid {C_MEDIUM};
        padding: 0px 25px; 
        transition: all 0.4s ease;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }}

    /* TESTO ALL'INTERNO DEI TAB */
    .stTabs [data-baseweb="tab"] p {{
        font-size: 15px;
        font-weight: 700;
        text-transform: uppercase;
        color: {C_DARK};
    }}

    /* STATO DEL TAB SELEZIONATO */
    .stTabs [aria-selected="true"] {{
        background-color: {C_PRIMARY} !important;
        border-color: {C_PRIMARY} !important;
        transform: translateY(-3px);
        box-shadow: 0 8px 15px rgba(227, 40, 109, 0.25);
    }}
    
    .stTabs [aria-selected="true"] p {{
        color: white !important;
    }}

    /* CARD DEI RISULTATI (SCORECARD) */
    .result-card {{
        background-color: white;
        padding: 35px;
        border-radius: 20px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        border-top: 8px solid {C_PRIMARY};
        margin-top: 15px;
    }}

    /* UNIFORMITÀ TITOLI (Checkbox escluse per leggibilità) */
    h1, h2, h3, h4, .stButton button, .stDownloadButton button {{
        text-transform: uppercase;
        letter-spacing: 1px;
        color: {C_DARK} !important;
    }}

    /* STILIZZAZIONE INPUT DI TESTO E CHECKBOX */
    .stTextInput input {{
        border-radius: 8px;
        border: 1px solid {C_MEDIUM};
        background-color: #ffffff;
    }}
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

# --- PARAMETRI PER IL CALCOLO DELL'OUTPUT (LESSICO AGGIORNATO) ---
SCORE_IMG_GENDER = {
    "La figura tocca se stessa (auto-contatto)": 1.0,
    "La figura tocca un oggetto in modo non funzionale all'azione": 1.0,
    "Inquadratura frammentata (focus su dettagli del corpo, escluso il volto)": 1.0,
    "Nudità totale": 1.0,
    "Nudità parziale o abbigliamento esplicitamente succinto": 0.5,
    "Posa sdraiata, semi-reclinata o inginocchiata": 0.5,
    "Sguardo distolto (non rivolto verso l'osservatore)": 0.5,
    "Testa reclinata o inclinata di lato": 0.5,
    "Corpo inquadrato solo parzialmente": 0.5
}

SCORE_IMG_INTERACT = {
    "Donne ritratte sorridenti, uomini con espressione seria": 1.0,
    "Donne in posa passiva/stazionaria, uomini impegnati in un'azione": 1.0,
    "Contesto domestico: solo la donna si occupa dei figli o delle faccende": 1.0,
    "Contesto professionale: l'uomo occupa il ruolo gerarchico superiore": 1.0,
    "Uomini al centro/primo piano, donne relegate allo sfondo": 1.0,
    "Uomini in piedi, donne sedute, sdraiate o inginocchiate": 1.0,
    "L'uomo è ritratto fisicamente più alto della donna": 1.0,
    "L'uomo guarda verso l'osservatore, la donna ha lo sguardo distolto": 1.0
}

SCORE_IMG_ETHNIC = {
    "Persone bianche in primo piano, altre etnie relegate allo sfondo": 1.0,
    "Persone bianche ritratte fisicamente più alte degli altri soggetti": 1.0,
    "Contesto professionale: persone bianche in ruoli gerarchici superiori": 1.0,
    "Contesto domestico: solo persone di altre etnie svolgono mansioni di pulizia": 1.0
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
    col_check, col_note = st.columns([1.5, 1])
    with col_check:
        checked = st.checkbox(label, key=key)
    with col_note:
        nota = ""
        if checked:
            nota = st.text_input("Evidenza / Azione mitigativa", key=f"note_{key}", placeholder="Specifica dettagli...")
            st.session_state.punti_sistema += weight
            if is_identity:
                st.session_state.cluster_identita += 1
            if tag:
                nota_str = nota if nota.strip() else "Nessun dettaglio fornito"
                st.session_state.dettagli_audit.append(f"[{tag}] {label} | Nota: {nota_str}")
    return checked

# --- LAYOUT PRINCIPALE ---
st.markdown(f"<h1 style='color:{C_PRIMARY};'>🛡️ IMAGES NAVIGATOR</h1>", unsafe_allow_html=True)
st.markdown("##### SISTEMA DI AUDIT PER L'INCLUSIVITÀ ALGORITMICA | PRIN PNRR")
st.write("") # Spaziatura

col_input, col_risultati = st.columns([0.65, 0.35], gap="large")

with col_input:
    # RESET DEI PUNTI AD OGNI RERUN
    st.session_state.punti_sistema = 0.0
    st.session_state.cluster_identita = 0
    st.session_state.dettagli_audit = []

    # STRUTTURA A 8 TAB PRINCIPALI
    tabs = st.tabs(["PREPARAZIONE", "DATI", "TEAM", "MODELLO", "UTENTI", "CONTESTO", "TESTI", "IMMAGINI"])

    with tabs[0]:
        st.subheader("FASE DI PREPARAZIONE")
        render_audit_item("Definizione chiara del caso d'uso e del target di riferimento", "prep_1", tag="PREP")
        render_audit_item("Selezione degli indicatori di equità rilevanti per il dominio", "prep_2", tag="PREP")
        render_audit_item("Coinvolgimento preventivo degli stakeholder o gruppi vulnerabili", "prep_3", tag="PREP")

    with tabs[1]:
        st.subheader("DATI")
        w_dati = 3.0 if dominio_scelto in ["SANITA E WELFARE", "GIUSTIZIA E SICUREZZA"] else 1.5
        render_audit_item("Mancato confronto dei dati di training con la demografia reale", "dat_1", w_dati, True, "DATI")
        render_audit_item("Presenza di etichette storicamente stereotipate nel dataset", "dat_2", w_dati, False, "DATI")
        render_audit_item("Assenza di strategie di riequilibrio per le classi minoritarie", "dat_3", w_dati, True, "DATI")
        render_audit_item("Mancanza di documentazione strutturata sui rischi (es. Data Sheet)", "dat_4", w_dati, False, "DATI")

    with tabs[2]:
        st.subheader("TEAM")
        w_team = 2.5 if dominio_scelto == "RECRUITING E HR" else 1.5
        render_audit_item("Omogeneità demografica del team di sviluppo e design", "tea_1", w_team, False, "TEAM")
        render_audit_item("Mancata identificazione di variabili proxy per gruppi protetti", "tea_2", w_team, True, "TEAM")
        render_audit_item("Mancanza di competenze DEI (Diversity, Equity, Inclusion) nel team", "tea_3", w_team, False, "TEAM")
        render_audit_item("Assenza di un registro decisionale tracciabile per le scelte di design", "tea_4", w_team, False, "TEAM")

    with tabs[3]:
        st.subheader("MODELLO")
        w_mod = 3.0 if dominio_scelto in ["SANITA E WELFARE", "FINANZA E CREDITO"] else 2.0
        render_audit_item("Mancato calcolo delle metriche di performance disaggregate per gruppo", "mod_1", w_mod, True, "MODELLO")
        render_audit_item("Assenza di test mirati con prompt sensibili o avversariali", "mod_2", w_mod, True, "MODELLO")
        render_audit_item("Model card non aggiornata o assente per gli utenti finali", "mod_3", w_mod, False, "MODELLO")
        render_audit_item("Mancata implementazione di filtri per mitigare le disparità rilevate", "mod_4", w_mod, False, "MODELLO")

    with tabs[4]:
        st.subheader("UTENTI")
        w_ut = 3.0 if dominio_scelto == "MARKETING E MEDIA" else 1.5
        render_audit_item("Mancata analisi del rischio di echo-chamber o polarizzazione", "ute_1", w_ut, False, "UTENTI")
        render_audit_item("Assenza di canali accessibili per segnalare output ingiusti", "ute_2", w_ut, False, "UTENTI")
        render_audit_item("Interfaccia utente non accessibile o progettata in modo escludente", "ute_3", w_ut, True, "UTENTI")

    with tabs[5]:
        st.subheader("CONTESTO")
        render_audit_item("Non conformità alle normative vigenti (es. AI Act, GDPR)", "con_1", 2.5, False, "CONTESTO")
        render_audit_item("Assenza di meccanismi di governance partecipativa e supervisione", "con_2", 2.0, False, "CONTESTO")
        render_audit_item("Mancanza di valutazioni d'impatto sui diritti fondamentali periodiche", "con_3", 2.0, False, "CONTESTO")

    with tabs[6]:
        st.subheader("ANALISI DEI TESTI")
        st.caption("LA PRESENZA DI ANCHE UN SOLO ELEMENTO DETERMINA UN RISCHIO BIAS.")
        
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**STEREOTIPI DI GENERE**")
            t1 = st.checkbox("Uso di 'uomo/uomini' come sinonimo universale di umanità", key="t_g1")
            t2 = st.checkbox("Participio declinato al maschile in presenza di maggioranza femminile", key="t_g2")
            t3 = st.checkbox("Uso asimmetrico di appellativi (es. 'Signora' vs titolo professionale)", key="t_g3")
            t4 = st.checkbox("Titoli professionali declinati al maschile o con suffisso 'donna'", key="t_g4")
            t5 = st.checkbox("Uso di aggettivi legati a fragilità emotiva o diminutivi", key="t_g5")
            t6 = st.checkbox("Identificazione relazionale della donna (es. 'la moglie di')", key="t_g6")
            t7 = st.checkbox("Uso di termini d'odio, misogini o metafore animali denigratorie", key="t_g7")
        
        with c2:
            st.markdown("**STEREOTIPI ETNICI**")
            t8 = st.checkbox("Uso di stereotipi comparativi (es. 'fumare come un turco')", key="t_e1")
            t9 = st.checkbox("Antonomasia stereotipata basata sull'etnia (es. 'preciso come uno svizzero')", key="t_e2")
            t10 = st.checkbox("Uso di generalizzazioni o termini razzisti/obsoleti", key="t_e3")
            t11 = st.checkbox("Deumanizzazione tramite tratti o metafore animali", key="t_e4")

        st.session_state.punti_testo = 1 if any([t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11]) else 0

    with tabs[7]:
        st.subheader("ANALISI DELLE IMMAGINI")
        st.caption("CALCOLO DELL'INDICE DI RISCHIO ADDITIVO BASATO SU SISTEMA A PIÙ VARIABILI.")

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
            
            for label, peso in SCORE_IMG_INTERACT.items():
                if st.checkbox(label, key=f"img_mf_{label}"):
                    score_mf += peso
            
            st.divider()
            st.caption("VARIABILI FEMMINILI APPLICABILI AL GRUPPO M/F:")
            
            esclusioni = [
                "Posa sdraiata, semi-reclinata o inginocchiata", 
                "Sguardo distolto (non rivolto verso l'osservatore)"
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

    testo_status = "🔴 RISCHIO RILEVATO" if st.session_state.get("punti_testo", 0) > 0 else "🟢 NESSUN RISCHIO"
    img_labels = st.session_state.get("img_labels", ("BASSO", "BASSO", "BASSO"))
    
    if "ALTO" in img_labels:
        img_status = "🔴 RISCHIO ALTO"
    elif "MEDIO" in img_labels:
        img_status = "🟡 RISCHIO MEDIO"
    else:
        img_status = "🟢 RISCHIO BASSO"

    html_scorecard = f"""<div class="result-card">
<h3 style="margin-top:0; color:{C_DARK};">SCORECARD DI RISCHIO</h3>
<p style="font-weight:bold; color:{C_DARK}; margin-bottom:10px;">RISCHI SISTEMICI (LIV. 2-6)</p>
<div style="background-color:{bg_alert}; color:{color_alert}; padding:15px; border-radius:10px; font-weight:bold; font-size:16px; margin-bottom:10px;">
{alert_text}
</div>
{warn_html}
<hr style="border-top:1px solid {C_MEDIUM}; margin: 25px 0;">
<p style="font-weight:bold; color:{C_DARK};">STATO DEGLI OUTPUT</p>
<p style="margin:8px 0; color:{C_DARK};"><strong>TESTI:</strong> {testo_status}</p>
<p style="margin:8px 0; color:{C_DARK};"><strong>IMMAGINI:</strong> {img_status}</p>
</div>"""
    
    st.markdown(html_scorecard, unsafe_allow_html=True)
    st.write("") 

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
