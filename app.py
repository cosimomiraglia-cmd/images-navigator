import streamlit as st
from datetime import datetime

st.set_page_config(page_title="IMAGES Navigator - Protocollo Integrale", layout="wide")

st.title("🛡️ IMAGES Navigator")
st.markdown("_Protocollo di conformità IA - Versione Integrale Appendice B (PRIN PNRR)_")

# Inizializzazione dati
if 'report_content' not in st.session_state:
    st.session_state.report_content = ""

critici_totali = 0
dettagli_audit = []

# Funzione per creare i task di audit (Checkbox + Testo)
def task(label, key, liv=""):
    c1, c2 = st.columns([1, 1])
    with c1:
        checked = st.checkbox(label, key=key)
    with c2:
        note = ""
        if checked:
            note = st.text_input("Nota/Azione:", key=f"n_{key}", placeholder="Come risolverai?")
            if liv: dettagli_audit.append(f"[{liv}] {label} -> Nota: {note}")
    return checked

tabs = st.tabs(["0. Prep", "1. Workflow", "2. DATA", "3. TEAM", "4. MODEL", "5. USERS", "6. CONTEXT", "8. OUTPUT"])

with tabs[0]:
    st.subheader("0. Prima di iniziare")
    task("Definiti caso d'uso, gruppi coinvolti e potenziali impatti", "s0_1")
    task("Selezionato set minimo di indicatori per ogni livello", "s0_2")
    task("Stabilito metodo di misura (log, documenti, audit, survey)", "s0_3")
    task("Previsto momento di confronto con stakeholder/comunità", "s0_4")

with tabs[1]:
    st.subheader("1. Procedura in 5 passi")
    task("(1) Scelti solo indicatori rilevanti per il dominio", "s1_1")
    task("(2) Associata almeno un'evidenza verificabile per indicatore", "s1_2")
    task("(3) Identificati gli indicatori critici (bias/fairness/inclusività)", "s1_3")
    task("(4) Pesati maggiormente gli impatti umani gravi", "s1_4")
    task("(5) Procedura ripetuta dopo ogni aggiornamento tecnico/normativo", "s1_5")

with tabs[2]:
    st.subheader("2. Livello DATI")
    if task("Dataset NON confrontato con popolazione/target (genere, etnia, etc.)", "s2_1", "DATI"): critici_totali += 1
    if task("Rilevato linguaggio o etichette degradanti/stereotipate", "s2_2", "DATI"): critici_totali += 1
    if task("Mancanza di strategie di riequilibrio per esclusioni storiche", "s2_3", "DATI"): critici_totali += 1
    if task("Mancata documentazione di limiti e rischi (Data Sheet)", "s2_4", "DATI"): critici_totali += 1

with tabs[3]:
    st.subheader("3. Livello TEAM")
    if task("Composizione team omogenea o esclusioni decisionali non note", "s3_1", "TEAM"): critici_totali += 1
    if task("Identificati proxy che colpiscono indirettamente gruppi protetti", "s3_2", "TEAM"): critici_totali += 1
    if task("Mancanza di competenze sociali/DEI/diritto nel team", "s3_3", "TEAM"): critici_totali += 1
    if task("Mancanza di un registro decisionale con razionali espliciti", "s3_4", "TEAM"): critici_totali += 1
    if task("Assenza di una fase di review specifica su bias/fairness", "s3_5", "TEAM"): critici_totali += 1

with tabs[4]:
    st.subheader("4. Livello MODELLO")
    if task("Mancato calcolo metriche disaggregate (FP/FN, accuracy, recall)", "s4_1", "MODELLO"): critici_totali += 1
    if task("Modello NON testato con prompt sensibili (genere, etnia, disabilità)", "s4_2", "MODELLO"): critici_totali += 1
    if task("Nessuna tecnica di mitigazione applicata dove emergono disparità", "s4_3", "MODELLO"): critici_totali += 1
    if task("Mancanza di una Model Card aggiornata (rischi e limiti)", "s4_4", "MODELLO"): critici_totali += 1

with tabs[5]:
    st.subheader("5. Livello UTENTI")
    if task("Mancato monitoraggio di prompt abusivi o comportamenti discriminatori", "s5_1", "UTENTI"): critici_totali += 1
    if task("Mancata osservazione di echo-chamber e reinforcement loop", "s5_2", "UTENTI"): critici_totali += 1
    if task("Assenza di canali semplici per segnalare esiti ingiusti", "s5_3", "UTENTI"): critici_totali += 1
    if task("Mancata tracciabilità segnalazioni -> modifiche reali", "s5_4", "UTENTI"): critici_totali += 1
    if task("Interfaccia NON accessibile o NON testata con utenti vulnerabili", "s5_5", "UTENTI"): critici_totali += 1

with tabs[6]:
    st.subheader("6. Livello CONTESTO (+1)")
    if task("Sistema NON allineato a norme (Privacy, AI Act, Discriminazione)", "s6_1", "CONTESTO"): critici_totali += 1
    if task("Assenza di governance che includa i gruppi impattati", "s6_2", "CONTESTO"): critici_totali += 1
    if task("Mancanza di policy aziendali esplicite su fairness/inclusività", "s6_3", "CONTESTO"): critici_totali += 1
    if task("Assenza di valutazioni d'impatto o audit periodici", "s6_4", "CONTESTO"): critici_totali += 1

with tabs[7]:
    st.subheader("8. Controllo Rapido Output")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**8.1 Immagini**")
        i1 = st.checkbox("Donne in ruoli passivi/decorativi")
        i2 = st.checkbox("Uomini sempre in ruoli attivi/dominanti")
        i3 = st.checkbox("Persone bianche sempre in primo piano/potere")
        img_risk = sum([i1, i2, i3]) >= 2
        if img_risk: st.error("Rischio Stereotipi Visivi: ALTO")
    with col2:
        st.markdown("**8.2 Testi**")
        t1 = st.checkbox("Uso di 'uomo/uomini' come sinonimo di persone")
        t2 = st.checkbox("Stereotipi o metafore degradanti")
        t3 = st.checkbox("Nessun controllo su parole chiave problematiche")
        txt_risk = sum([t1, t2, t3]) >= 1
        if txt_risk: st.error("Rischio Bias Testuale: RILEVATO")

# --- VALUTAZIONE FINALE (STEP 7) ---
st.divider()
st.header("7. Valutazione del Rischio Complessivo")
rischio = "BASSO"
if critici_totali >= 4 or img_risk: rischio = "ALTO"
elif 2 <= critici_totali <= 3: rischio = "MEDIO"

if rischio == "ALTO": st.error(f"🔴 LIVELLO DI RISCHIO: {rischio} ({critici_totali} indicatori critici)")
elif rischio == "MEDIO": st.warning(f"🟡 LIVELLO DI RISCHIO: {rischio} ({critici_totali} indicatori critici)")
else: st.success(f"🟢 LIVELLO DI RISCHIO: {rischio} ({critici_totali} indicatori critici)")

# --- ESPORTAZIONE REPORT ---
report_txt = f"""--------------------------------------------------
REPORT DI CONFORMITÀ IMAGES - {datetime.now().strftime('%d/%m/%Y')}
--------------------------------------------------
RISCHIO COMPLESSIVO: {rischio}
Indicatori Critici Attivi: {critici_totali}
--------------------------------------------------
DETTAGLI AZIONI DI MITIGAZIONE:
""" + "\n".join(dettagli_audit)

st.download_button("📥 Scarica Report per il PRIN", report_txt, file_name="Report_IMAGES.txt")
