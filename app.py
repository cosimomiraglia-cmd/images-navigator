import streamlit as st

st.set_page_config(page_title="IMAGES Navigator - Professional Report", layout="wide")

st.title("🛡️ IMAGES Navigator: Accountability Tool")
st.markdown("_Protocollo di conformità per lo sviluppo di IA inclusive (PRIN PNRR)_")

# Dizionario per raccogliere i commenti e generare il report finale
if 'comments' not in st.session_state:
    st.session_state.comments = {}

critici_totali = 0
notifiche_report = []

tabs = st.tabs([
    "0. Start", "1. Workflow", "2. DATA", "3. TEAM", 
    "4. MODEL", "5. USERS", "6. CONTEXT", "8. OUTPUT CHECK"
])

# --- TAB 0 & 1: ISTRUZIONI E SETUP ---
with tabs[0]:
    st.subheader("🚀 Checklist di Avvio")
    st.checkbox("Definizione caso d'uso e gruppi impattati")
    st.checkbox("Selezione indicatori minimi per livello")
    st.checkbox("Metodi di misura stabiliti")
    st.checkbox("Confronto stakeholder effettuato")

with tabs[1]:
    st.subheader("🔄 Procedura Operativa")
    st.info("Passi: (1) Filtra, (2) Documenta, (3) Identifica, (4) Pesa, (5) Itera.")

# --- FUNZIONE HELPER PER CHECKBOX + COMMENTO ---
def audit_item(label, key):
    checked = st.checkbox(label, key=key)
    comment = ""
    if checked:
        comment = st.text_area(f"👉 Piano d'azione / Giustificazione per: {label}", key=f"comm_{key}", placeholder="Descrivi come intendi mitigare questo rischio...")
    return checked, comment

# --- TAB 2: DATA ---
with tabs[2]:
    st.subheader("📂 Livello 1: Qualità dei DATI")
    c1, comm1 = audit_item("Il dataset non riflette la popolazione reale (Sottorappresentazione).", "d1")
    c2, comm2 = audit_item("Etichette o tag contengono termini stereotipati/offensivi.", "d2")
    c3, comm3 = audit_item("Assenza di strategie riparative per esclusioni storiche.", "d3")
    c4, comm4 = audit_item("Mancanza di Data Sheet sui limiti del dataset.", "d4")
    
    items = [(c1, "Dati sottorappresentati", comm1), (c2, "Tag stereotipati", comm2), (c3, "No strategie riparative", comm3), (c4, "No Data Sheet", comm4)]
    for status, name, msg in items:
        if status:
            critici_totali += 1
            notifiche_report.append(f"**{name}**: {msg}")

# --- TAB 3: TEAM ---
with tabs[3]:
    st.subheader("👥 Livello 2: Governance del TEAM")
    c_t1, comm_t1 = audit_item("Team omogeneo (mancanza di diversità demografica/disciplinare).", "t1")
    c_t2, comm_t2 = audit_item("Uso di proxy sensibili non giustificati.", "t2")
    c_t3, comm_t3 = audit_item("Assenza registro decisionale (Decision Log).", "t3")
    
    for status, name, msg in [(c_t1, "Team omogeneo", comm_t1), (c_t2, "Proxy sensibili", comm_t2), (c_t3, "No Decision Log", comm_t3)]:
        if status:
            critici_totali += 1
            notifiche_report.append(f"**{name}**: {msg}")

# --- TAB 4: MODEL ---
with tabs[4]:
    st.subheader("⚙️ Livello 3: Performance del MODELLO")
    c_m1, comm_m1 = audit_item("Disparità di performance tra gruppi (Errori differenziali).", "m1")
    c_m2, comm_m2 = audit_item("Amplificazione di stereotipi rilevata nei test.", "m2")
    
    for status, name, msg in [(c_m1, "Disparità performance", comm_m1), (c_m2, "Amplificazione stereotipi", comm_m2)]:
        if status:
            critici_totali += 1
            notifiche_report.append(f"**{name}**: {msg}")

# --- TAB 5: USERS ---
with tabs[5]:
    st.subheader("👤 Livello 4: Esperienza UTENTI")
    c_u1, comm_u1 = audit_item("Assenza canali di segnalazione e contestazione.", "u1")
    c_u2, comm_u2 = audit_item("Interfaccia non accessibile a utenti vulnerabili.", "u2")
    
    for status, name, msg in [(c_u1, "No canali segnalazione", comm_u1), (c_u2, "No accessibilità", comm_u2)]:
        if status:
            critici_totali += 1
            notifiche_report.append(f"**{name}**: {msg}")

# --- TAB 6: CONTEXT ---
with tabs[6]:
    st.subheader("🌍 Livello 5: CONTESTO (+1)")
    c_c1, comm_c1 = audit_item("Mancato allineamento a norme (AI Act / GDPR).", "c1")
    c_c2, comm_c2 = audit_item("Assenza di governance partecipativa.", "c2")
    
    for status, name, msg in [(c_c1, "Non-compliance normativa", comm_c1), (c_c2, "No governance partecipativa", comm_c2)]:
        if status:
            critici_totali += 1
            notifiche_report.append(f"**{name}**: {msg}")

# --- TAB 8: OUTPUT CHECK ---
with tabs[7]:
    st.subheader("🖼️ Test Rapido Output")
    col1, col2 = st.columns(2)
    with col1:
        img_check = st.checkbox("Rilevati pattern visivi stereotipati (>=2)")
    with col2:
        txt_check = st.checkbox("Rilevati bias testuali (>=1)")

# --- 7. VERDETTO E REPORT FINALE ---
st.divider()
st.header("⚖️ 7. Valutazione e Report Finale")

col_a, col_b = st.columns([1, 2])

with col_a:
    if critici_totali >= 4 or img_check:
        st.error(f"🔴 **RISCHIO ALTO**\n\nCriticità: {critici_totali}")
    elif 2 <= critici_totali <= 3:
        st.warning(f"🟡 **RISCHIO MEDIO**\n\nCriticità: {critici_totali}")
    else:
        st.success(f"🟢 **RISCHIO BASSO**\n\nCriticità: {critici_totali}")

with col_b:
    st.subheader("Sintesi delle Mitigazioni")
    if notifiche_report:
        for nota in notifiche_report:
            st.markdown(nota)
    else:
        st.write("Nessuna criticità dichiarata o nessun commento inserito.")

# Funzione per simulare l'export (stampa pagina o copia testo)
st.button("🖨️ Esporta Report per Rendicontazione")
