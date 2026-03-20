import streamlit as st

# Configurazione estetica
st.set_page_config(page_title="IMAGES Navigator - Protocollo Appendice B", layout="wide")

st.title("🛡️ IMAGES Navigator: Protocollo di Audit")
st.caption("Toolkit IMAGES - Versione conforme all'Appendice B (PRIN PNRR)")

# Inizializziamo il conteggio degli indicatori critici per il calcolo del rischio (Step 7)
critici_totali = 0

# --- TABS BASATI SULLA NUMERAZIONE DELL'APPENDICE ---
tabs = st.tabs([
    "0. Prep", "1. Procedura", "2. DATI", "3. TEAM", 
    "4. MODELLO", "5. UTENTI", "6. CONTESTO", "8. Visual/Text"
])

with tabs[0]:
    st.subheader("0. Prima di iniziare (Setup)")
    st.checkbox("Definizione caso d'uso, gruppi coinvolti e impatti")
    st.checkbox("Selezione set minimo di indicatori per livello")
    st.checkbox("Stabilizzazione dei metodi di misura (log, audit, survey)")
    st.checkbox("Confronto con stakeholder/comunità impattate")

with tabs[1]:
    st.subheader("1. Procedura in 5 passi")
    st.info("Istruzioni operative per il team di sviluppo")
    st.checkbox("(1) Scelta degli indicatori rilevanti (no liste standard)")
    st.checkbox("(2) Associazione evidenza verificabile per ogni indicatore")
    st.checkbox("(3) Identificazione indicatori critici")
    st.checkbox("(4) Ponderazione basata su gravità impatti umani")
    st.checkbox("(5) Iterazione post-aggiornamento (dati, modelli, norme)")

with tabs[2]:
    st.subheader("2. Livello DATI")
    d1 = st.checkbox("Mancato confronto dataset vs popolazione/target")
    d2 = st.checkbox("Presenza linguaggio o etichette degradanti/stereotipate")
    d3 = st.checkbox("Assenza strategie di riequilibrio (esclusioni storiche)")
    d4 = st.checkbox("Mancata documentazione limiti e rischi (Data Sheet)")
    critici_totali += sum([d1, d2, d3, d4])

with tabs[3]:
    st.subheader("3. Livello TEAM")
    t1 = st.checkbox("Mancata conoscenza composizione team/esclusioni decisionali")
    t2 = st.checkbox("Uso di variabili/proxy che colpiscono gruppi protetti")
    t3 = st.checkbox("Assenza competenze non tecniche (sociali, DEI, diritto)")
    t4 = st.checkbox("Assenza registro decisionale con razionali espliciti")
    t5 = st.checkbox("Mancanza review su bias in fase di sviluppo")
    critici_totali += sum([t1, t2, t3, t4, t5])

with tabs[4]:
    st.subheader("4. Livello MODELLO")
    m1 = st.checkbox("Mancato calcolo metriche disaggregate (FP/FN, accuracy)")
    m2 = st.checkbox("Mancato test con prompt sensibili (genere, etnia, disabilità)")
    m3 = st.checkbox("Assenza di tecniche di mitigazione su disparità emerse")
    m4 = st.checkbox("Mancata manutenzione Model Card aggiornata")
    critici_totali += sum([m1, m2, m3, m4])

with tabs[5]:
    st.subheader("5. Livello UTENTI")
    u1 = st.checkbox("Assenza monitoraggio prompt abusivi e comportamenti discriminatori")
    u2 = st.checkbox("Mancata osservazione echo-chamber e reinforcement loop")
    u3 = st.checkbox("Assenza canali semplici per segnalazione esiti ingiusti")
    u4 = st.checkbox("Mancata tracciabilità segnalazioni/modifiche reali")
    u5 = st.checkbox("Interfaccia non accessibile o non testata con utenti vulnerabili")
    critici_totali += sum([u1, u2, u3, u4, u5])

with tabs[6]:
    st.subheader("6. Livello CONTESTO (+1)")
    c1 = st.checkbox("Mancato allineamento norme (Privacy, AI Act, Discriminazione)")
    c2 = st.checkbox("Assenza strutture governance con gruppi impattati")
    c3 = st.checkbox("Assenza policy esplicite su fairness e inclusività")
    c4 = st.checkbox("Mancanza valutazioni d'impatto e audit periodici")
    critici_totali += sum([c1, c2, c3, c4])

with tabs[7]:
    st.subheader("8. Controllo rapido contenuti generati")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**8.1 Immagini**")
        i1 = st.checkbox("Donne sistematicamente in ruoli passivi/decorativi")
        i2 = st.checkbox("Uomini sempre in ruoli attivi/dominanti")
        i3 = st.checkbox("Persone bianche sistematicamente in primo piano/potere")
        pattern_img = sum([i1, i2, i3])
        if pattern_img >= 2: st.error("⚠️ Rischio alto stereotipi visivi")
    with col2:
        st.markdown("**8.2 Testi**")
        tx1 = st.checkbox("Uso di 'uomo/uomini' come sinonimo di persone")
        tx2 = st.checkbox("Presenza di stereotipi o metafore degradanti")
        tx3 = st.checkbox("Mancato controllo sistematico parole chiave")
        pattern_txt = sum([tx1, tx2, tx3])
        if pattern_txt >= 1: st.error("⚠️ Testo a rischio bias")

# --- 7. VALUTAZIONE DEL RISCHIO COMPLESSIVO ---
st.divider()
st.header("7. Valutazione del rischio complessivo")
st.write(f"Indicatori critici rilevati: **{critici_totali}**")

if critici_totali >= 4:
    st.error("🔴 RISCHIO ALTO: Bloccare il rilascio e intervenire.")
elif 2 <= critici_totali <= 3:
    st.warning("🟡 RISCHIO MEDIO: Rilascio condizionato a mitigazione.")
else:
    st.success("🟢 RISCHIO BASSO: Procedere con monitoraggio regolare.")

st.divider()
st.caption("Toolkit IMAGES - Progetto PRIN PNRR. Documentazione generata automaticamente dall'audit dello sviluppatore.")
