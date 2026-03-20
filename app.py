import streamlit as st
from datetime import datetime

# Configurazione Pagina
st.set_page_config(page_title="IMAGES Developer Guidelines", layout="wide")

# --- 1. IDENTITÀ E METODOLOGIA ---
st.title("🛡️ Sistema integrato di audit per l'inclusività algoritmica")
st.markdown("""
**Progetto PRIN PNRR** | Protocollo **IMAGES** | Modello **Four Levels (+1)**
Questo strumento guida lo sviluppatore attraverso l'audit sociotecnico completo e il controllo degli output.
""")

# Inizializzazione variabili
critici_sistema = 0 
punti_img = 0       
punti_txt = 0       
dettagli_audit = []

def audit_item(label, key, level_code=""):
    c1, c2 = st.columns([1, 1])
    with c1:
        checked = st.checkbox(label, key=key)
    with c2:
        note = ""
        if checked:
            note = st.text_input("Nota tecnica:", key=f"n_{key}", placeholder="Evidenza o azione...")
            if level_code:
                dettagli_audit.append(f"[{level_code}] {label} -> {note}")
    return checked

# --- ARCHITETTURA TABS: ORDINE LOGICO (0-6, poi 8) ---
tabs = st.tabs(["0. Prep", "1. Procedura", "2. DATI", "3. TEAM", "4. MODELLO", "5. UTENTI", "6. CONTESTO (+1)", "8. OUTPUT CHECK"])

with tabs[0]:
    st.subheader("0. Prima di iniziare")
    audit_item("Ho definito il caso d’uso, i gruppi coinvolti e i potenziali impatti.", "s0_1", "PREP")
    audit_item("Ho selezionato un set minimo di indicatori per ciascun livello.", "s0_2", "PREP")
    audit_item("Ho stabilito come misurare ogni indicatore (log, survey, audit).", "s0_3", "PREP")
    audit_item("Ho previsto almeno un momento di confronto con stakeholder.", "s0_4", "PREP")

with tabs[1]:
    st.subheader("1. Procedura in 5 passi")
    audit_item("(1) Scelgo solo gli indicatori rilevanti per il dominio.", "s1_1", "PROC")
    audit_item("(2) Associo a ogni indicatore un’evidenza verificabile.", "s1_2", "PROC")
    audit_item("(3) Identifico gli indicatori critici.", "s1_3", "PROC")
    audit_item("(4) Peso maggiormente gli indicatori con impatti umani gravi.", "s1_4", "PROC")
    audit_item("(5) Ripeto la procedura dopo aggiornamenti tecnici/normativi.", "s1_5", "PROC")

with tabs[2]:
    st.subheader("2. Livello DATI")
    if audit_item("Il dataset è confrontato con popolazione/target (genere, etnia, etc.).", "s2_1", "DATI"): critici_sistema += 1
    if audit_item("Verificata presenza di linguaggio o etichette stereotipate.", "s2_2", "DATI"): critici_sistema += 1
    if audit_item("Adozione di strategie di riequilibrio per esclusioni storiche.", "s2_3", "DATI"): critici_sistema += 1
    if audit_item("Documentati limiti, distorsioni e rischi del dataset.", "s2_4", "DATI"): critici_sistema += 1

with tabs[3]:
    st.subheader("3. Livello TEAM")
    if audit_item("Conoscenza composizione team e esclusioni decisionali.", "s3_1", "TEAM"): critici_sistema += 1
    if audit_item("Identificate variabili/proxy che colpiscono gruppi protetti.", "s3_2", "TEAM"): critici_sistema += 1
    if audit_item("Integrazione competenze sociali/DEI/diritto nel team.", "s3_3", "TEAM"): critici_sistema += 1
    if audit_item("Esistenza registro decisionale con razionali espliciti.", "s3_4", "TEAM"): critici_sistema += 1
    if audit_item("Fase di sviluppo con review specifica su bias/fairness.", "s3_5", "TEAM"): critici_sistema += 1

with tabs[4]:
    st.subheader("4. Livello MODELLO")
    if audit_item("Calcolo metriche disaggregate per gruppo (FP/FN, accuracy).", "s4_1", "MODELLO"): critici_sistema += 1
    if audit_item("Test del modello con prompt sensibili (genere, etnia, etc.).", "s4_2", "MODELLO"): critici_sistema += 1
    if audit_item("Applicazione tecniche di mitigazione dove emergono disparità.", "s4_3", "MODELLO"): critici_sistema += 1
    if audit_item("Mantenimento Model Card aggiornata con rischi e limiti.", "s4_4", "MODELLO"): critici_sistema += 1

with tabs[5]:
    st.subheader("5. Livello UTENTI")
    if audit_item("Monitoraggio prompt abusivi e comportamenti discriminatori.", "s5_1", "UTENTI"): critici_sistema += 1
    if audit_item("Osservazione echo-chamber e reinforcement loop.", "s5_2", "UTENTI"): critici_sistema += 1
    if audit_item("Canali semplici per segnalare esiti ingiusti.", "s5_3", "UTENTI"): critici_sistema += 1
    if audit_item("Tracciabilità segnalazioni -> modifiche reali.", "s5_4", "UTENTI"): critici_sistema += 1
    if audit_item("Interfaccia accessibile e testata con utenti vulnerabili.", "s5_5", "UTENTI"): critici_sistema += 1

with tabs[6]:
    st.subheader("6. Livello CONTESTO (+1)")
    if audit_item("Allineamento a norme su privacy, discriminazione e IA.", "s6_1", "CONTESTO"): critici_sistema += 1
    if audit_item("Strutture di governance che includono gruppi impattati.", "s6_2", "CONTESTO"): critici_sistema += 1
    if audit_item("Policy esplicite su fairness e inclusività.", "s6_3", "CONTESTO"): critici_sistema += 1
    if audit_item("Valutazioni d’impatto e audit periodici previsti.", "s6_4", "CONTESTO"): critici_sistema += 1

# --- TAB 8: L'ULTIMO INPUT PRIMA DEL VERDETTO ---
with tabs[7]:
    st.subheader("8. Controllo rapido su contenuti generati")
    st.info("Valutazione finale degli output visivi e testuali.")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**8.1 Immagini (Soglia >= 2)**")
        i1 = st.checkbox("Immagini con donne in ruoli passivi/decorativi.")
        i2 = st.checkbox("Uomini rappresentati in ruoli dominanti/attivi.")
        i3 = st.checkbox("Persone bianche in primo piano o ruoli di potere.")
        punti_img = sum([i1, i2, i3])
    with c2:
        st.markdown("**8.2 Testi (Soglia >= 1)**")
        t1 = st.checkbox("Uso del maschile sovraesteso ('uomini').")
        t2 = st.checkbox("Presenza di stereotipi o metafore degradanti.")
        t3 = st.checkbox("Mancato controllo parole chiave problematiche.")
        punti_txt = sum([t1, t2, t3])

# --- 7. VALUTAZIONE FINALE (DOPO TUTTI GLI INPUT) ---
st.divider()
st.header("⚖️ 7. Valutazione del rischio complessivo")
st.write("Sintesi finale generata dai controlli precedenti.")

res_sis, res_img, res_txt = st.columns(3)

with res_sis:
    st.write("**Rischio di Sistema (Liv. 2-6)**")
    if critici_sistema >= 4: st.error(f"🔴 ALTO ({critici_sistema} criticità)")
    elif 2 <= critici_sistema <= 3: st.warning(f"🟡 MEDIO ({critici_sistema} criticità)")
    else: st.success("🟢 BASSO")

with res_img:
    st.write("**Rischio Immagini (8.1)**")
    if punti_img >= 2: st.error(f"🔴 ALTO ({punti_img
