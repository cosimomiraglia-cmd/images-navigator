import streamlit as st
from datetime import datetime

# 1. Configurazione Pagina - Corretta virgoletta mancante
st.set_page_config(page_title="IMAGES Developer Guidelines", layout="wide")

# --- 2. IDENTITÀ ISTITUZIONALE ---
st.title("🛡️ Sistema integrato di audit per l'inclusività algoritmica")

# --- 3. ORIENTAMENTO METODOLOGICO ---
st.markdown("""
Questo strumento operativo implementa il protocollo **IMAGES** per l'identificazione e la mitigazione dei bias di genere ed etnici. 
L'equità del sistema viene valutata attraverso il modello **Four Levels (+1)**: *Dati, Team, Modello, Utenti e Contesto*.
---
""")

# Inizializzazione variabili di scoring e report
critici_sistema = 0 
punti_img = 0       
punti_txt = 0       
dettagli_audit = []

# Funzione per gestire i task
def audit_item(label, key, level_code=""):
    c1, c2 = st.columns([1, 1])
    with c1:
        checked = st.checkbox(label, key=key)
    with c2:
        note = ""
        if checked:
            note = st.text_input("Evidenza / Piano d'azione:", key=f"n_{key}", placeholder="Specificare l'evidenza o l'azione correttiva...")
            if level_code:
                dettagli_audit.append(f"[{level_code}] {label}\n   NOTA: {note if note else 'Nessuna nota inserita'}")
    return checked

# --- DEFINIZIONE COLONNE PER RISULTATI SEMPRE A VISTA ---
col_input, col_risultati = st.columns([0.65, 0.35], gap="large")

with col_input:
    # --- ARCHITETTURA TABS ---
    tabs = st.tabs([
        "0. Prep", "1. Procedura", "2. DATI", "3. TEAM", 
        "4. MODELLO", "5. UTENTI", "6. CONTESTO (+1)", 
        "8. OUTPUT CHECK", "7. RISULTATI & REPORT"
    ])

    with tabs[0]:
        st.subheader("0. Prima di iniziare")
        audit_item("Ho definito il caso d’uso, i gruppi coinvolti e i potenziali impatti.", "s0_1")
        audit_item("Ho selezionato un set minimo di indicatori per ciascun livello (Dati, Team, Modello, Utenti, Contesto).", "s0_2")
        audit_item("Ho stabilito come misurare ogni indicatore (numeri, log, documenti, audit, survey).", "s0_3")
        audit_item("Ho previsto almeno un momento di confronto con stakeholder/comunità impattate.", "s0_4")

    with tabs[1]:
        st.subheader("1. Procedura in 5 passi")
        audit_item("(1) Scelgo solo gli indicatori rilevanti, evitando liste standard.", "s1_1")
        audit_item("(2) Associo a ogni indicatore almeno un’evidenza verificabile.", "s1_2")
        audit_item("(3) Identifico gli indicatori critici per bias, fairness o inclusività.", "s1_3")
        audit_item("(4) Peso maggiormente gli indicatori che hanno impatti umani gravi.", "s1_4")
        audit_item("(5) Ripeto la procedura dopo aggiornamenti di dati, modelli o norme.", "s1_5")

    with tabs[2]:
        st.subheader("2. Livello DATI – chi è rappresentato e come")
        if audit_item("Il dataset è confrontato con popolazione/target (genere, etnia, status, intersezionalità).", "s2_1", "DATI"): critici_sistema += 1
        if audit_item("Ho verificato la presenza di linguaggio o etichette degradanti/stereotipate.", "s2_2", "DATI"): critici_sistema += 1
        if audit_item("Dove esistono esclusioni storiche, ho adottato strategie di riequilibrio.", "s2_3", "DATI"): critici_sistema += 1
        if audit_item("Ho documentato limiti, distorsioni e rischi del dataset.", "s2_4", "DATI"): critici_sistema += 1

    with tabs[3]:
        st.subheader("3. Livello TEAM – chi decide e su quali basi")
        if audit_item("Conosco la composizione del team e chi è escluso dai processi decisionali.", "s3_1", "TEAM"): critici_sistema += 1
        if audit_item("Ho identificato variabili o proxy che colpiscono indirettamente gruppi protetti.", "s3_2", "TEAM"): critici_sistema += 1
        if audit_item("Il team integra competenze non solo tecniche (studi sociali, DEI, diritto, dominio).", "s3_3", "TEAM"): critici_sistema += 1
        if audit_item("Esiste un registro decisionale con razionali espliciti.", "s3_4", "TEAM"): critici_sistema += 1
        if audit_item("Almeno una fase di sviluppo prevede una review su bias, fairness e inclusività.", "s3_5", "TEAM"): critici_sistema += 1

    with tabs[4]:
        st.subheader("4. Livello MODELLO – performance e comportamento")
        if audit_item("Ho calcolato metriche disaggregate per gruppo (FP/FN, accuracy, recall).", "s4_1", "MODELLO"): critici_sistema += 1
        if audit_item("Ho testato il modello con input/prompt sensibili (genere, etnia, disabilità).", "s4_2", "MODELLO"): critici_sistema += 1
        if audit_item("Dove emergono disparità, applico almeno una tecnica di mitigazione.", "s4_3", "MODELLO"): critici_sistema += 1
        if audit_item("Mantengo una Model Card aggiornata con rischi, limiti e gruppi vulnerabili.", "s4_4", "MODELLO"): critici_sistema += 1

    with tabs[5]:
        st.subheader("5. Livello UTENTI – uso reale, abusi, contestabilità")
        if audit_item("Monitoro prompt abusivi e comportamenti discriminatori.", "s5_1", "UTENTI"): critici_sistema += 1
        if audit_item("Osservo la formazione di echo-chamber e reinforcement loop.", "s5_2", "UTENTI"): critici_sistema += 1
        if audit_item("Esistono canali semplici per segnalare esiti ingiusti.", "s5_3", "UTENTI"): critici_sistema += 1
        if audit_item("Traccio quante segnalazioni portano a modifiche reali.", "s5_4", "UTENTI"): critici_sistema += 1
        if audit_item("L’interfaccia è accessibile e testata con utenti vulnerabili.", "s5_5", "UTENTI"): critici_sistema += 1

    with tabs[6]:
        st.subheader("6. Livello CONTESTO (+1) – norme, governance, poteri")
        if audit_item("Il sistema è allineato a norme su privacy, discriminazione e IA.", "s6_1", "CONTESTO"): critici_sistema += 1
        if audit_item("Esistono strutture di governance che includono gruppi impattati.", "s6_2", "CONTESTO"): critici_sistema += 1
        if audit_item("L’organizzazione ha policy esplicite su fairness e inclusività.", "s6_3", "CONTESTO"): critici_sistema += 1
        if audit_item("Sono previste valutazioni d’impatto e audit periodici.", "s6_4", "CONTESTO"): critici_sistema += 1

    with tabs[7]:
        st.subheader("7. Controllo rapido su contenuti generati")
        st.info("Esegui l'audit visivo e testuale a campione prima di consultare il verdetto finale.")
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

    with tabs[8]:
        st.write("Usa la colonna a destra per visualizzare i risultati e scaricare il report.")

# --- COLONNA DESTRA: SEZIONE 7 (RISULTATI SEMPRE VISIBILI) ---
with col_risultati:
    st.header("⚖️ Scorecard di rischio")
    st.info("I risultati si aggiornano dinamicamente mentre completi l'audit.")
    
    # BOX 1: SISTEMA
    st.subheader("Rischi sistemici")
    if critici_sistema >= 4:
        st.error(f"🔴 ALTO ({critici_sistema} criticità)")
    elif 2 <= critici_sistema <= 3:
        st.warning(f"🟡 MEDIO ({critici_sistema} criticità)")
    else:
        st.success("🟢 BASSO (Stato ottimale)")
    
    # BOX 2: IMMAGINI
    st.subheader("Rischio nelle immagini")
    if punti_img >= 2:
        st.error(f"🔴 ALTO ({punti_img} pattern)")
    else:
        st.success("🟢 BASSO")
        
    # BOX 3: TESTI
    st.subheader("Rischio nei esti") # Mantenuta etichetta originale
    if punti_txt >= 1:
        st.error(f"🔴 RILEVATO ({punti_txt} occorrenze)")
    else:
        st.success("🟢 NON RILEVATO")

    st.divider()

    # --- ESPORTAZIONE REPORT ---
    report_txt = f"""REPORT DI CONFORMITÀ IMAGES - PRIN PNRR
Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}
--------------------------------------------------
VERDETTO FINALE:
- Rischio Sistema: {critici_sistema} criticità
- Rischio Immagini: {punti_img} pattern rilevati
- Rischio Testi: {punti_txt} occorrenze rilevate
--------------------------------------------------
DETTAGLIO AUDIT:
""" + "\n".join(dettagli_audit)

    st.download_button("📥 Scarica Report Tecnico (TXT)", report_txt, file_name="Audit_IMAGES_PNRR.txt", use_container_width=True)

st.divider()
st.caption("Toolkit IMAGES | Progetto PRIN PNRR | Risposta automatica basata sui dati di input.")
