import streamlit as st
from datetime import datetime

# 1. Configurazione Pagina
st.set_page_config(page_title="IMAGES Developer Guidelines", layout="wide")

# --- DATASET PESI E DOMINI (Logica dell'Esperto) ---
DOMINI = {
    "Giustizia & Sicurezza": {"mult": 2.2, "threshold": 6.0},
    "Sanità & Welfare": {"mult": 2.0, "threshold": 6.0},
    "Pubblica Amministrazione": {"mult": 2.0, "threshold": 7.0},
    "Finanza & Credito": {"mult": 1.9, "threshold": 7.5},
    "Istruzione & Ricerca": {"mult": 1.8, "threshold": 8.0},
    "Recruiting & HR": {"mult": 1.7, "threshold": 8.0},
    "Marketing & Media": {"mult": 1.3, "threshold": 10.0},
    "Gaming & Entertainment": {"mult": 1.1, "threshold": 12.0}
}

# --- 2. IDENTITÀ ISTITUZIONALE ---
st.title("🛡️ Sistema integrato di audit per l'inclusività algoritmica")
st.caption("Toolkit IMAGES | Progetto PRIN PNRR | Modello Four Levels (+1)")

# --- 3. SELEZIONE CONTESTUALE (Passo 1 & 4) ---
with st.sidebar:
    st.header("⚙️ Configurazione Audit")
    dominio_scelto = st.selectbox("Seleziona il dominio applicativo:", list(DOMINI.keys()))
    st.info(f"**Configurazione:** {dominio_scelto}\n\nIl sistema applicherà pesi e soglie specifiche per questo settore, come previsto dal principio di selezione contestuale.")
    st.divider()
    st.markdown("🔍 *L'uso dello strumento è discrezionale. I risultati costituiscono una guida all'audit e non un verdetto automatico.*")

# Inizializzazione variabili
punti_sistema = 0.0
cluster_identita = 0 # Per moltiplicatore intersezionale
dettagli_audit = []

def audit_item(label, key, weight=1.0, is_identity=False, level_code=""):
    global punti_sistema, cluster_identita
    c1, c2 = st.columns([1, 1])
    with c1:
        checked = st.checkbox(label, key=key)
    with c2:
        note = ""
        if checked:
            punti_sistema += weight
            if is_identity: cluster_identita += 1
            note = st.text_input("Evidenza / Piano d'azione:", key=f"n_{key}", placeholder="Specificare l'evidenza...")
            if level_code:
                dettagli_audit.append(f"[{level_code}] {label}\n   NOTA: {note if note else 'Nessuna nota'}")
    return checked

# --- LAYOUT A DUE COLONNE ---
col_input, col_risultati = st.columns([0.65, 0.35], gap="large")

with col_input:
    tabs = st.tabs(["0. Prep", "1. Procedura", "2. DATI", "3. TEAM", "4. MODELLO", "5. UTENTI", "6. CONTESTO (+1)", "8. OUTPUT CHECK"])

    with tabs[0]:
        st.subheader("0. Prima di iniziare")
        audit_item("Ho definito il caso d’uso, i gruppi coinvolti e i potenziali impatti.", "s0_1")
        audit_item("Ho selezionato un set minimo di indicatori per ciascun livello.", "s0_2")
        audit_item("Ho stabilito come misurare ogni indicatore (log, survey, audit).", "s0_3")
        audit_item("Ho previsto almeno un momento di confronto con stakeholder.", "s0_4")

    with tabs[1]:
        st.subheader("1. Procedura in 5 passi")
        audit_item("(1) Scelgo solo gli indicatori rilevanti per il dominio.", "s1_1")
        audit_item("(2) Associo a ogni indicatore almeno un’evidenza verificabile.", "s1_2")
        audit_item("(3) Identifico gli indicatori critici per bias o inclusività.", "s1_3")
        audit_item("(4) Peso maggiormente gli indicatori con impatti umani gravi.", "s1_4")
        audit_item("(5) Ripeto la procedura dopo aggiornamenti tecnici o normativi.", "s1_5")

    with tabs[2]:
        st.subheader("2. Livello DATI")
        # Pesi differenziati in base al dominio
        w_dati = 3.0 if dominio_scelto in ["Sanità & Welfare", "Giustizia & Sicurezza"] else 1.5
        audit_item("Il dataset NON è confrontato con popolazione/target reale.", "s2_1", weight=w_dati, is_identity=True, level_code="DATI")
        audit_item("Rilevata presenza di linguaggio o etichette stereotipate.", "s2_2", weight=w_dati, level_code="DATI")
        audit_item("Assenza di strategie di riequilibrio per esclusioni storiche.", "s2_3", weight=w_dati, is_identity=True, level_code="DATI")
        audit_item("Mancata documentazione di limiti, distorsioni e rischi del dataset.", "s2_4", weight=w_dati, level_code="DATI")

    with tabs[3]:
        st.subheader("3. Livello TEAM")
        w_team = 2.5 if dominio_scelto == "Recruiting & HR" else 1.5
        audit_item("Composizione team omogenea o esclusioni decisionali non note.", "s3_1", weight=w_team, level_code="TEAM")
        audit_item("Identificate variabili proxy che colpiscono gruppi protetti.", "s3_2", weight=w_team, is_identity=True, level_code="TEAM")
        audit_item("Mancanza di competenze sociali/DEI/diritto nel team.", "s3_3", weight=w_team, level_code="TEAM")
        audit_item("Assenza di un registro decisionale con razionali espliciti.", "s3_4", weight=w_team, level_code="TEAM")
        audit_item("Mancanza di una review specifica su bias in fase di sviluppo.", "s3_5", weight=w_team, level_code="TEAM")

    with tabs[4]:
        st.subheader("4. Livello MODELLO")
        w_mod = 3.0 if dominio_scelto in ["Sanità & Welfare", "Finanza & Credito"] else 2.0
        audit_item("Mancato calcolo metriche disaggregate (FP/FN, accuracy).", "s4_1", weight=w_mod, is_identity=True, level_code="MODELLO")
        audit_item("Modello NON testato con prompt sensibili (genere/etnia).", "s4_2", weight=w_mod, is_identity=True, level_code="MODELLO")
        audit_item("Nessuna tecnica di mitigazione applicata dove emergono disparità.", "s4_3", weight=w_mod, level_code="MODELLO")
        audit_item("Model Card non aggiornata con rischi e gruppi vulnerabili.", "s4_4", weight=w_mod, level_code="MODELLO")

    with tabs[5]:
        st.subheader("5. Livello UTENTI")
        w_ut = 3.0 if dominio_scelto == "Marketing & Media" else 1.5
        audit_item("Mancato monitoraggio di comportamenti discriminatori.", "s5_1", weight=w_ut, level_code="UTENTI")
        audit_item("Mancata osservazione di echo-chamber o reinforcement loop.", "s5_2", weight=w_ut, level_code="UTENTI")
        audit_item("Assenza canali semplici per segnalare esiti ingiusti.", "s5_3", weight=w_ut, level_code="UTENTI")
        audit_item("Mancata tracciabilità segnalazioni -> modifiche reali.", "s5_4", weight=w_ut, level_code="UTENTI")
        audit_item("Interfaccia non accessibile o non testata con utenti vulnerabili.", "s5_5", weight=w_ut, is_identity=True, level_code="UTENTI")

    with tabs[6]:
        st.subheader("6. Livello CONTESTO (+1)")
        audit_item("Sistema NON allineato a norme (AI Act, GDPR).", "s6_1", weight=2.5, level_code="CONTESTO")
        audit_item("Assenza di governance che includa i gruppi impattati.", "s6_2", weight=2.0, level_code="CONTESTO")
        audit_item("Mancanza di policy esplicite su fairness e inclusività.", "s6_3", weight=1.5, level_code="CONTESTO")
        audit_item("Assenza di valutazioni d’impatto o audit periodici.", "s6_4", weight=2.0, level_code="CONTESTO")

    with tabs[7]:
        st.subheader("7. Controllo rapido su contenuti generati")
        c_img, c_txt = st.columns(2)
        with c_img:
            st.markdown("**7.1 Immagini (Soglia >= 2)**")
            i1 = st.checkbox("Presenza di donne in ruoli passivi o decorativi.", key="i1")
            i2 = st.checkbox("Presenza di uomini in ruoli dominanti o attivi.", key="i2")
            i3 = st.checkbox("Presenza di persone bianche in primo piano o potere.", key="i3")
            punti_img = sum([i1, i2, i3])
        with c_txt:
            st.markdown("**7.2 Testi (Soglia >= 1)**")
            t1 = st.checkbox("Uso del maschile sovraesteso ('uomini').", key="t1")
            t2 = st.checkbox("Presenza di stereotipi o metafore degradanti.", key="t2")
            t3 = st.checkbox("Assenza di controllo sistematico parole chiave.", key="t3")
            punti_txt = sum([t1, t2, t3])

# --- CALCOLO FINALE CON MOLTIPLICATORE ---
moltiplicatore = DOMINI[dominio_scelto]["mult"] if cluster_identita > 1 else 1.0
punteggio_finale = punti_sistema * moltiplicatore
soglia_critica = DOMINI[dominio_scelto]["threshold"]

with col_risultati:
    st.header("⚖️ 7. Scorecard di rischio")
    
    if moltiplicatore > 1.0:
        st.warning(f"⚠️ **Effetto Intersezionale:** Rilevate {cluster_identita} criticità su categorie protette. Il rischio è potenziato (x{moltiplicatore}).")

    # BOX 1: SISTEMA (Pesato e Situato)
    st.subheader("Rischi sistemici (Liv. 2-6)")
    if punteggio_finale >= soglia_critica:
        st.error(f"🔴 ALTO ({punteggio_finale:.1f} / {soglia_critica})")
    elif punteggio_finale >= (soglia_critica / 2):
        st.warning(f"🟡 MEDIO ({punteggio_finale:.1f} / {soglia_critica})")
    else:
        st.success(f"🟢 BASSO ({punteggio_finale:.1f} / {soglia_critica})")
    
    # BOX 2: IMMAGINI
    st.subheader("Rischio nelle immagini (7.1)")
    if punti_img >= 2: st.error(f"🔴 ALTO ({punti_img} pattern)")
    else: st.success("🟢 BASSO")
        
    # BOX 3: TESTI
    st.subheader("Rischio nei testi (7.2)")
    if punti_txt >= 1: st.error(f"🔴 RILEVATO ({punti_txt} occorrenze)")
    else: st.success("🟢 NON RILEVATO")

    st.divider()
    
    # REPORT
    report_txt = f"""REPORT DI CONFORMITÀ IMAGES - PRIN PNRR
Dominio: {dominio_scelto} | Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}
--------------------------------------------------
7. VERDETTO FINALE:
- Punteggio Sistema Pesato: {punteggio_finale:.2f} (Soglia: {soglia_critica})
- Moltiplicatore Intersezionale applicato: {moltiplicatore}
- Rischio Immagini: {punti_img} pattern
- Rischio Testi: {punti_txt} occorrenze
--------------------------------------------------
DETTAGLIO AUDIT:
""" + "\n".join(dettagli_audit)

    st.download_button("📥 Scarica Report Tecnico (TXT)", report_txt, file_name=f"Audit_IMAGES_{dominio_scelto}.txt", use_container_width=True)
