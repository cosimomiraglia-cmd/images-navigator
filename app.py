import streamlit as st

st.set_page_config(page_title="IMAGES Navigator - Dev Tool", layout="wide")

st.title("🛡️ IMAGES Navigator")
st.markdown("_Strumento operativo per lo sviluppo di IA inclusive_")

critici_totali = 0

tabs = st.tabs([
    "0. Start", "1. Workflow", "2. DATA", "3. TEAM", 
    "4. MODEL", "5. USERS", "6. CONTEXT", "8. OUTPUT CHECK"
])

with tabs[0]:
    st.subheader("🚀 Checklist di Avvio")
    st.write("Assicurati di aver impostato le basi del progetto prima di procedere.")
    st.checkbox("Ho definito chiaramente chi sono gli utenti finali e chi potrebbe essere penalizzato dal sistema.")
    st.checkbox("Ho scelto gli indicatori di inclusività specifici per il mio settore (es. Sanità vs Marketing).")
    st.checkbox("Ho stabilito come misurerò i risultati (metriche, log tecnici o survey).")
    st.checkbox("Ho previsto un momento di confronto con esperti esterni o comunità coinvolte.")

with tabs[1]:
    st.subheader("🔄 Procedura Operativa")
    st.info("Segui questi 5 passi durante il ciclo di sviluppo (Sprint/Release).")
    st.markdown("""
    1. **Filtra:** Non usare tutti gli indicatori, scegli solo quelli che impattano sul tuo caso d'uso.
    2. **Documenta:** Per ogni 'Sì' nella checklist, tieni pronta l'evidenza (un file, un test, un verbale).
    3. **Identifica:** Trova i punti critici che potrebbero bloccare il rilascio.
    4. **Pesa:** Dai la priorità ai problemi che causano danni fisici, legali o reputazionali gravi.
    5. **Itera:** Riesegui questo audit ogni volta che cambi il dataset o aggiorni il modello.
    """)

with tabs[2]:
    st.subheader("📂 Livello 1: Qualità dei DATI")
    st.write("Controlla la 'materia prima' del tuo sistema.")
    d1 = st.checkbox("Il dataset NON riflette la popolazione reale (es. mancano minoranze o generi).")
    d2 = st.checkbox("Le etichette/tag contengono termini offensivi, datati o stereotipati.")
    d3 = st.checkbox("Mancano dati 'riparativi' (non è stato fatto nulla per compensare esclusioni storiche).")
    d4 = st.checkbox("Manca un 'Data Sheet' che spieghi da dove vengono i dati e quali sono i loro limiti.")
    if any([d1, d2, d3, d4]):
        st.info("**💡 Quick Fix:** Applica tecniche di *oversampling* sui gruppi mancanti o usa tool di *de-biasing* sulle etichette.")
    critici_totali += sum([d1, d2, d3, d4])

with tabs[3]:
    st.subheader("👥 Livello 2: Governance del TEAM")
    st.write("Chi progetta influenza il risultato. Valuta il processo decisionale.")
    t1 = st.checkbox("Il team è troppo omogeneo (stessa formazione, genere o background).")
    t2 = st.checkbox("Usiamo variabili 'nascoste' (proxy) che potrebbero discriminare (es. CAP o titolo di studio).")
    t3 = st.checkbox("Nel team mancano esperti di impatto sociale, etica o diritto.")
    t4 = st.checkbox("Le decisioni tecniche critiche non sono tracciate in un registro (Decision Log).")
    t5 = st.checkbox("Non è prevista una 'Bias Review' formale durante lo sviluppo.")
    critici_totali += sum([t1, t2, t3, t4, t5])

with tabs[4]:
    st.subheader("⚙️ Livello 3: Performance del MODELLO")
    st.write("Verifica se l'algoritmo si comporta in modo equo tra gruppi diversi.")
    m1 = st.checkbox("Il modello sbaglia molto più spesso su un gruppo specifico (es. falsi negativi alti per le donne).")
    m2 = st.checkbox("Il modello genera output stereotipati se stimolato con prompt sensibili.")
    m3 = st.checkbox("Non sono state applicate tecniche per bilanciare i risultati (mitigazione post-processing).")
    m4 = st.checkbox("La 'Model Card' non è aggiornata con i limiti tecnici del sistema.")
    critici_totali += sum([m1, m2, m3, m4])

with tabs[5]:
    st.subheader("👤 Livello 4: Esperienza UTENTI")
    st.write("Come interagiscono le persone con l'IA?")
    u1 = st.checkbox("Non monitoriamo se gli utenti usano il sistema in modo discriminatorio o tossico.")
    u2 = st.checkbox("Il sistema rischia di creare 'bolle' (echo-chamber) che rinforzano pregiudizi.")
    u3 = st.checkbox("Non c'è un tasto 'Segnala' o un modo facile per contestare un output ingiusto.")
    u4 = st.checkbox("Le segnalazioni degli utenti non vengono analizzate per migliorare il modello.")
    u5 = st.checkbox("L'interfaccia è difficile da usare per persone con disabilità o bassa alfabetizzazione digitale.")
    critici_totali += sum([u1, u2, u3, u4, u5])

with tabs[6]:
    st.subheader("🌍 Livello 5: CONTESTO (+1)")
    st.write("Il sistema nel mondo reale: norme e responsabilità.")
    c1 = st.checkbox("Il sistema non è ancora allineato all'AI Act o al GDPR.")
    c2 = st.checkbox("Non esiste un comitato o un processo che includa il parere di chi subirà l'IA.")
    c3 = st.checkbox("L'azienda/ente non ha una policy scritta sull'uso etico dell'IA.")
    c4 = st.checkbox("Non abbiamo fatto un audit esterno o una valutazione d'impatto periodica.")
    critici_totali += sum([c1, c2, c3, c4])

with tabs[7]:
    st.subheader("🖼️ Test Rapido Output (Immagini/Testi)")
    st.write("Analizza a campione i risultati generati.")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Check Visivo**")
        i1 = st.checkbox("Donne in ruoli passivi o decorativi.")
        i2 = st.checkbox("Uomini in ruoli dominanti o tecnologici.")
        i3 = st.checkbox("Minoranze etniche assenti o in ruoli marginali.")
        if sum([i1, i2, i3]) >= 2: st.error("Rischio Stereotipo Visivo")
    with col2:
        st.markdown("**Check Testuale**")
        tx1 = st.checkbox("Uso sistematico del maschile universale.")
        tx2 = st.checkbox("Aggettivi o metafore che ridicolizzano gruppi sociali.")
        tx3 = st.checkbox("Mancato filtro su parole chiave d'odio o bias.")
        if sum([tx1, tx2, tx3]) >= 1: st.error("Rischio Bias Testuale")

# --- VALUTAZIONE FINALE ---
st.divider()
st.header("⚖️ Verdetto di Conformità")
if critici_totali >= 4:
    st.error(f"**RISCHIO ALTO ({critici_totali} criticità)**: Il sistema non è pronto. Necessario intervento immediato.")
elif 2 <= critici_totali <= 3:
    st.warning(f"**RISCHIO MEDIO ({critici_totali} criticità)**: Il rilascio è possibile solo con un piano di monitoraggio.")
else:
    st.success(f"**RISCHIO BASSO ({critici_totali} criticità)**: Il sistema rispetta i criteri minimi di inclusività.")

st.caption("Toolkit IMAGES | PRIN PNRR | Risposta automatica basata sui dati di input.")
