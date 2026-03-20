import streamlit as st
from datetime import datetime

# Configurazione Pagina
st.set_page_config(page_title="IMAGES Developer Guidelines", layout="wide")

# --- 1. IDENTITÀ ISTITUZIONALE ---
st.title("🛡️ Sistema integrato di audit per l'inclusività algoritmica")

# --- 2. ORIENTAMENTO METODOLOGICO ---
st.markdown("""
Questo strumento operativo implementa il protocollo **IMAGES** per l'identificazione e la mitigazione dei bias di genere ed etnici. 
L'equità del sistema viene valutata come esito di processi sociotecnici attraverso il modello **Four Levels (+1)**: *Dati, Team, Modello, Utenti e Contesto*.
---
""")

# Inizializzazione variabili di scoring e report
critici_sistema = 0 
punti_img = 0       
punti_txt = 0       
dettagli_audit = []

# Funzione per gestire i task con coerenza testuale
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

# --- ARCHITETTURA TABS ---
tabs = st.tabs(["0. Prep", "1. Procedura", "2. DATI", "3. TEAM", "4. MODELLO", "5. UTENTI", "6. CONTESTO (+1)", "8. OUTPUT CHECK"])

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
    audit_item("(4) Peso maggiormente gli indicatori che hanno impatti umani più gravi.", "s1_4")
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
    st.subheader("8. Controllo rapido su contenuti generati")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**8.1 Immagini**")
        i1 = st.checkbox("Le immagini non rappresentano sistematicamente donne come sfondo, cura, decorazione.")
        i2 = st.checkbox("Gli uomini non appaiono sempre in ruoli attivi/dominanti.")
        i3 = st.checkbox("Le persone bianche non sono sistematicamente in primo piano o in ruoli di potere.")
        # Nota: Qui la logica inverte il senso del check per contare i pattern negativi
        if i1 or i2 or i3:
             st.info("Seleziona i pattern negativi riscontrati per il calcolo del rischio.")
        punti_img = sum([i1, i2, i3])
    with c2:
        st.markdown("**8.2 Testi**")
        t1 = st.checkbox("Il testo non usa “uomo/uomini” come sinonimo di “persone”.")
        t2 = st.checkbox("Non contiene stereotipi o metafore degradanti verso gruppi sociali.")
        t3 = st.checkbox("Ho effettuato un controllo sistematico di parole chiave problematiche.")
        # La logica del testo scatta se almeno una condizione di qualità NON è soddisfatta
        punti_txt = 3 - sum([t1, t2, t3])

# --- 7. VALUTAZIONE FINALE SEPARATA ---
st.divider()
st.header("⚖️ 7. Valutazione del rischio complessivo")

col_a, col_b, col_c = st.columns(3)

with col_a:
    st.subheader("Rischio di Sistema")
    if critici_sistema >= 4: st.error(f"🔴 ALTO ({critici_sistema} criticità)")
    elif 2 <= critici_sistema <= 3: st.warning(f"🟡 MEDIO ({critici_sistema} criticità)")
    else: st.success(f"🟢 BASSO ({critici_sistema} criticità)")
    st.caption("Soglie: 0-1 Basso, 2-3 Medio, >=4 Alto")

with col_b:
    st.subheader("Rischio Immagini")
    if punti_img >= 2: st.error(f"🔴 ALTO ({punti_img} pattern ricorrenti)")
    else: st.success("🟢 BASSO / CONTROLLATO")
    st.caption("Soglia: >= 2 pattern ricorrenti")

with col_c:
    st.subheader("Rischio Testi")
    if punti_txt >= 1: st.error(f"🔴 RILEVATO ({punti_txt} occorrenze)")
    else: st.success("🟢 NON RILEVATO")
    st.caption("Soglia: >= 1 occorrenza discriminatoria")

# --- ESPORTAZIONE REPORT ---
data_str = datetime.now().strftime('%d/%m/%Y %H:%M')
report_txt = f"""--------------------------------------------------
REPORT DI CONFORMITÀ IMAGES - PRIN PNRR
Data: {data_str}
--------------------------------------------------
SINTESI VALUTAZIONE:
- Rischio Sistema (Livelli 2-6): {critici_sistema} criticità rilevate
- Rischio Immagini (Step 8.1): {punti_img} pattern rilevati
- Rischio Testi (Step 8.2): {punti_txt} occorrenze rilevate
--------------------------------------------------
DETTAGLIO AUDIT E PIANI D'AZIONE:
""" + "\n".join(dettagli_audit)

st.divider()
st.download_button("📥 Scarica Report Tecnico (TXT)", report_txt, file_name=f"Audit_IMAGES_{datetime.now().strftime('%Y%m%d')}.txt")
