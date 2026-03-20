import streamlit as st
from datetime import datetime

# 1. Configurazione Pagina (Corretta virgoletta alla riga 5)
st.set_page_config(page_title="IMAGES Developer Guidelines", layout="wide")

# --- 2. IDENTITÀ ISTITUZIONALE ---
st.title("🛡️ Sistema integrato di audit per l'inclusività algoritmica")

# --- 3. ORIENTAMENTO METODOLOGICO ---
st.markdown("""
Questo strumento operativo implementa il protocollo **IMAGES** per l'identificazione e la mitigazione dei bias di genere ed etnici. 
L'equità del sistema viene valutata come esito di processi sociotecnici attraverso il modello **Four Levels (+1)**: *Dati, Team, Modello, Utenti e Contesto*.
---
""")

# Inizializzazione variabili
critici_sistema = 0 
punti_img = 0       
punti_txt = 0       
dettagli_audit = []

# Funzione per gestire i task con coerenza testuale e salvataggio note
def audit_item(label, key, level_code=""):
    c1, c2 = st.columns([1, 1])
    with c1:
        checked = st.checkbox(label, key=key)
    with c2:
        note = ""
        if checked:
            note = st.text_input("Evidenza / Piano d'azione:", key=f"n_{key}", placeholder="Specificare l'azione correttiva...")
            if level_code:
                dettagli_audit.append(f"[{level_code}] {label}\n   NOTA: {note if note else 'Nessuna nota inserita'}")
    return checked

# --- ARCHITETTURA TABS ---
tabs = st.tabs(["0. Prep", "1. Procedura", "2. DATI", "3. TEAM", "4. MODELLO", "5. UTENTI", "6. CONTESTO (+1)", "8. OUTPUT CHECK"])

with tabs[0]:
    st.subheader("0. Prima di iniziare")
    audit_item("Ho definito il caso d’uso, i gruppi coinvolti e i potenziali impatti.", "s0_1", "PREP")
    audit_item("Ho selezionato un set minimo di indicatori per ciascun livello.", "s0_2", "PREP")
    audit_item("Ho stabilito come misurare ogni indicatore (log, survey, audit).", "s0_3", "PREP")
    audit_item("Ho previsto un momento di confronto con stakeholder coinvolti.", "s0_4", "PREP")

with tabs[1]:
    st.subheader("1. Procedura in 5 passi")
    audit_item("(1) Scelgo solo gli indicatori rilevanti, evitando liste standard.", "s1_1", "PROC")
    audit_item("(2) Associo a ogni indicatore almeno un’evidenza verificabile.", "s1_2", "PROC")
    audit_item("(3) Identifico gli indicatori critici per bias o inclusività.", "s1_3", "PROC")
    audit_item("(4) Peso maggiormente gli indicatori con impatti umani gravi.", "s1_4", "PROC")
    audit_item("(5) Ripeto la procedura dopo aggiornamenti di dati o norme.", "s1_5", "PROC")

with tabs[2]:
    st.subheader("2. Livello DATI")
    if audit_item("Il dataset NON è confrontato con popolazione/target reale.", "s2_1", "DATI"): critici_sistema += 1
    if audit_item("Rilevata presenza di linguaggio o etichette stereotipate.", "s2_2", "DATI"): critici_sistema += 1
    if audit_item("Assenza di strategie di riequilibrio per esclusioni storiche.", "s2_3", "DATI"): critici_sistema += 1
    if audit_item("Mancata documentazione di limiti, distorsioni e rischi del dataset.", "s2_4", "DATI"): critici_sistema += 1

with tabs[3]:
    st.subheader("3. Livello TEAM")
    if audit_item("Composizione team omogenea o esclusioni decisionali non note.", "s3_1", "TEAM"): critici_sistema += 1
    if audit_item("Identificate variabili proxy che colpiscono gruppi protetti.", "s3_2", "TEAM"): critici_sistema += 1
    if audit_item("Mancanza di competenze sociali/DEI/diritto nel team.", "s3_3", "TEAM"): critici_sistema += 1
    if audit_item("Assenza di un registro decisionale con razionali espliciti.", "s3_4", "TEAM"): critici_sistema += 1
    if audit_item("Mancanza di una review specifica su bias in fase di sviluppo.", "s3_5", "TEAM"): critici_sistema += 1

with tabs[4]:
    st.subheader("4. Livello MODELLO")
    if audit_item("Mancato calcolo metriche disaggregate (FP/FN, accuracy).", "s4_1", "MODELLO"): critici_sistema += 1
    if audit_item("Modello NON testato con prompt sensibili (genere/etnia).", "s4_2", "MODELLO"): critici_sistema += 1
    if audit_item("Nessuna tecnica di mitigazione applicata dove emergono disparità.", "s4_3", "MODELLO"): critici_sistema += 1
    if audit_item("Model Card non aggiornata con rischi e gruppi vulnerabili.", "s4_4", "MODELLO"): critici_sistema += 1

with tabs[5]:
    st.subheader("5. Livello UTENTI")
    if audit_item("Mancato monitoraggio di comportamenti discriminatori.", "s5_1", "UTENTI"): critici_sistema += 1
    if audit_item("Mancata osservazione di echo-chamber o reinforcement loop.", "s5_2", "UTENTI"): critici_sistema += 1
    if audit_item("Assenza di canali semplici per segnalare esiti ingiusti.", "s5_3", "UTENTI"): critici_sistema += 1
    if audit_item("Mancata tracciabilità segnalazioni -> modifiche reali.", "s5_4", "UTENTI"): critici_sistema += 1
    if audit_item("Interfaccia non accessibile o non testata con utenti vulnerabili.", "s5_5", "UTENTI"): critici_sistema += 1

with tabs[6]:
    st.subheader("6. Livello CONTESTO (+1)")
    if audit_item("Sistema NON allineato a norme (AI Act, GDPR).", "s6_1", "CONTESTO"): critici_sistema += 1
    if audit_item("Assenza di governance che includa i gruppi impattati.", "s6_2", "CONTESTO"): critici_sistema += 1
    if audit_item("Mancanza di policy esplicite su fairness e inclusività.", "s6_3", "CONTESTO"): critici_sistema += 1
    if audit_item("Assenza di valutazioni d’impatto o audit periodici.", "s6_4", "CONTESTO"): critici_sistema += 1

with tabs[7]:
    st.subheader("8. Controllo Rapido Output")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**8.1 Immagini**")
        i1 = st.checkbox("Donne in ruoli passivi/decorativi.")
        i2 = st.checkbox("Uomini in ruoli dominanti/attivi.")
        i3 = st.checkbox("Persone bianche in primo piano/potere.")
        punti_img = sum([i1, i2, i3])
    with col2:
        st.markdown("**8.2 Testi**")
        t1 = st.checkbox("Uso del maschile sovraesteso ('uomini').")
        t2 = st.checkbox("Presenza di stereotipi o metafore degradanti.")
        t3 = st.checkbox("Mancato controllo parole chiave problematiche.")
        punti_txt = sum([t1, t2, t3])

# --- 7. VALUTAZIONE FINALE SEPARATA ---
st.divider()
st.header("⚖️ 7. Risultati dell'Audit")

res_a, res_b, res_c = st.columns(3)

with res_a:
    st.subheader("Rischio Sistema")
    if critici_sistema >= 4: st.error(f"🔴 ALTO ({critici_sistema} criticità)")
    elif 2 <= critici_sistema <= 3: st.warning(f"🟡 MEDIO ({critici_sistema} criticità)")
    else: st.success("🟢 BASSO")

with res_b:
    st.subheader("Rischio Immagini")
    if punti_img >= 2: st.error("🔴 ALTO (Pattern rilevati)")
    else: st.success("🟢 BASSO")

with res_c:
    st.subheader("Rischio Testi")
    if punti_txt >= 1: st.error("🔴 RILEVATO")
    else: st.success("🟢 NON RILEVATO")

# --- ESPORTAZIONE REPORT ---
report_txt = f"""REPORT IMAGES - {datetime.now().strftime('%d/%m/%Y %H:%M')}
--------------------------------------------------
RISULTATI AUDIT:
- Rischio Sistema: {critici_sistema} criticità
- Rischio Immagini: {'ALTO' if punti_img >= 2 else 'BASSO'}
- Rischio Testi: {'RILEVATO' if punti_txt >= 1 else 'NON RILEVATO'}
--------------------------------------------------
PIANI D'AZIONE:
""" + "\n".join(dettagli_audit)

st.divider()
st.download_button("📥 Scarica Report Tecnico (TXT)", report_txt, file_name="Audit_IMAGES_PNRR.txt")
