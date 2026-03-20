import streamlit as st

# Configurazione estetica
st.set_page_config(page_title="IMAGES Navigator 2.0", layout="wide")

st.title("🛡️ IMAGES Navigator: Developer Compliance Tool")
st.markdown("---")

# --- STEP 0: SETUP (Sidebar) ---
with st.sidebar:
    st.header("0. Setup di Progetto")
    st.checkbox("Caso d'uso e impatti definiti")
    st.checkbox("Indicatori selezionati per il dominio")
    st.checkbox("Metodo di misura stabilito")
    st.checkbox("Confronto stakeholder effettuato")
    st.divider()
    st.info("Questo tool genera un report di rischio basato sui 4 Livelli (+1) e i controlli specifici IMAGES.")

# --- INTERFACCIA A TAB PER NON APPIATTIRE L'OUTPUT ---
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📂 Dati", "👥 Team", "⚙️ Modello", "👤 Utenti", "🌍 Contesto", "🖼️ Visual/Text"
])

# Inizializziamo il conteggio degli indicatori critici
critici_totali = 0

with tab1:
    st.subheader("2. Livello DATI")
    d1 = st.checkbox("Mancato confronto con popolazione/target (Sottorappresentazione)")
    d2 = st.checkbox("Presenza di linguaggio/etichette degradanti o stereotipate")
    d3 = st.checkbox("Assenza di strategie di riequilibrio per esclusioni storiche")
    d4 = st.checkbox("Mancata documentazione di limiti e rischi (Data Sheet)")
    critici_totali += sum([d1, d2, d3, d4])

with tab2:
    st.subheader("3. Livello TEAM")
    t1 = st.checkbox("Omogeneità eccessiva e mancanza di competenze DEI/Sociali")
    t2 = st.checkbox("Presenza di variabili/proxy che colpiscono gruppi protetti")
    t3 = st.checkbox("Assenza di un registro decisionale esplicito")
    t4 = st.checkbox("Mancanza di una review specifica su bias durante lo sviluppo")
    critici_totali += sum([t1, t2, t3, t4])

with tab3:
    st.subheader("4. Livello MODELLO")
    m1 = st.checkbox("Disparità di performance disaggregate (FP/FN, Accuracy)")
    m2 = st.checkbox("Output che amplificano stereotipi (testati con prompt sensibili)")
    m3 = st.checkbox("Assenza di tecniche di mitigazione attive")
    m4 = st.checkbox("Model Card non aggiornata o incompleta")
    critici_totali += sum([m1, m2, m3, m4])

with tab4:
    st.subheader("5. Livello UTENTI")
    u1 = st.checkbox("Presenza di prompt abusivi o feedback loop non monitorati")
    u2 = st.checkbox("Assenza di canali di segnalazione e contestazione")
    u3 = st.checkbox("Interfaccia non accessibile o non testata con utenti vulnerabili")
    critici_totali += sum([u1, u2, u3])

with tab5:
    st.subheader("6. Livello CONTESTO (+1)")
    c1 = st.checkbox("Mancato allineamento a norme (Privacy, AI Act, Discriminazione)")
    c2 = st.checkbox("Assenza di governance partecipativa e policy di inclusività")
    c3 = st.checkbox("Mancanza di audit periodici e impact assessment")
    critici_totali += sum([c1, c2, c3])

with tab6:
    st.subheader("8. Controllo Rapido Contenuti Generati")
    col_img, col_txt = st.columns(2)
    
    with col_img:
        st.markdown("**8.1 Immagini**")
        i1 = st.checkbox("Donne in ruoli passivi (sfondo, cura, decorazione)")
        i2 = st.checkbox("Uomini sempre in ruoli attivi/dominanti")
        i3 = st.checkbox("Persone bianche sistematicamente in primo piano/potere")
        rischio_img = sum([i1, i2, i3]) >= 2
        if rischio_img: st.error("⚠️ Rischio Stereotipi Visivi Alto")
        
    with col_txt:
        st.markdown("**8.2 Testi**")
        tx1 = st.checkbox("Uso del maschile sovraesteso ('uomini' per 'persone')")
        tx2 = st.checkbox("Presenza di stereotipi o metafore degradanti")
        tx3 = st.checkbox("Mancato controllo parole chiave problematiche")
        rischio_txt = sum([tx1, tx2, tx3]) >= 1
        if rischio_txt: st.error("⚠️ Testo a Rischio Bias")

# --- 7. VALUTAZIONE DEL RISCHIO COMPLESSIVO ---
st.markdown("---")
st.header("7. Valutazione del Rischio Complessivo")

if critici_totali >= 4 or rischio_img:
    st.error(f"🚨 RISCHIO ALTO ({critici_totali} indicatori critici attivi)")
    st.markdown("**AZIONE:** Blocco del rilascio. Intervento correttivo obbligatorio.")
elif 2 <= critici_totali <= 3:
    st.warning(f"⚠️ RISCHIO MEDIO ({critici_totali} indicatori critici attivi)")
    st.markdown("**AZIONE:** Rilascio condizionato a piani di mitigazione e monitoraggio.")
else:
    st.success(f"✅ RISCHIO BASSO ({critici_totali} indicatori critici attivi)")
    st.markdown("**AZIONE:** Procedere con monitoraggio regolare.")

# Tasto per simulare il report
if st.button("Genera Report per Documentazione PRIN"):
    st.write("Report generato con successo. Copia questa valutazione nella documentazione di progetto.")
