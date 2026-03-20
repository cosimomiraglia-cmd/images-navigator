import streamlit as st
from datetime import datetime

# Configurazione Pagina
st.set_page_config(page_title="IMAGES Navigator - Official Report", layout="wide")

st.title("🛡️ IMAGES Navigator: Accountability & Audit")
st.markdown("_Protocollo di conformità per lo sviluppo di IA inclusive (PRIN PNRR)_")

# --- INIZIALIZZAZIONE DATI PER IL REPORT ---
if 'report_content' not in st.session_state:
    st.session_state.report_content = ""

critici_totali = 0
dettagli_audit = []

# --- FUNZIONE HELPER PER CHECKBOX E LOGICA REPORT ---
def audit_step(label, key, level_name):
    col_check, col_txt = st.columns([1, 1])
    with col_check:
        checked = st.checkbox(label, key=key)
    with col_txt:
        comment = ""
        if checked:
            comment = st.text_input("Giustificazione / Piano d'azione:", key=f"note_{key}", placeholder="Es: Azione di mitigazione prevista...")
            dettagli_audit.append(f"[{level_name}] CRITICITÀ: {label}\n   PIANO D'AZIONE: {comment if comment else 'Non specificato'}\n")
    return checked

# --- TABS ---
tabs = st.tabs(["0-1. Setup", "2. DATA", "3. TEAM", "4. MODEL", "5. USERS", "6. CONTEXT", "8. OUTPUT CHECK"])

with tabs[0]:
    st.subheader("🚀 0-1. Fasi Preparatorie")
    s1 = st.checkbox("Definizione caso d'uso e gruppi coinvolti")
    s2 = st.checkbox("Selezione indicatori minimi obbligatori")
    s3 = st.checkbox("Pianificazione co-progettazione")

with tabs[1]:
    st.subheader("📂 Livello 1: DATI")
    if audit_step("Sottorappresentazione sistematica", "d1", "DATI"): critici_totali += 1
    if audit_step("Etichette stereotipate", "d2", "DATI"): critici_totali += 1
    if audit_step("Assenza strategie riparative", "d3", "DATI"): critici_totali += 1
    if audit_step("Mancanza Data Sheet", "d4", "DATI"): critici_totali += 1

with tabs[2]:
    st.subheader("👥 Livello 2: TEAM")
    if audit_step("Omogeneità del team", "t1", "TEAM"): critici_totali += 1
    if audit_step("Assenza registro decisionale", "t2", "TEAM"): critici_totali += 1
    if audit_step("Mancanza competenze DEI/Sociali", "t3", "TEAM"): critici_totali += 1

with tabs[3]:
    st.subheader("⚙️ Livello 3: MODELLO")
    if audit_step("Disparità performance (FPR/FNR)", "m1", "MODELLO"): critici_totali += 1
    if audit_step("Amplificazione stereotipi", "m2", "MODELLO"): critici_totali += 1
    if audit_step("Model Card non aggiornata", "m3", "MODELLO"): critici_totali += 1

with tabs[4]:
    st.subheader("👤 Livello 4: UTENTI")
    if audit_step("Assenza canali segnalazione", "u1", "UTENTI"): critici_totali += 1
    if audit_step("Interfaccia non accessibile", "u2", "UTENTI"): critici_totali += 1

with tabs[5]:
    st.subheader("🌍 Livello 5: CONTESTO (+1)")
    if audit_step("Non-compliance normativa (AI Act)", "c1", "CONTESTO"): critici_totali += 1
    if audit_step("Assenza governance partecipativa", "c2", "CONTESTO"): critici_totali += 1

with tabs[6]:
    st.subheader("🖼️ 8. Controllo Rapido Output")
    col_i, col_t = st.columns(2)
    with col_i: i_crit = st.checkbox("Pattern visivi stereotipati (>=2)")
    with col_t: t_crit = st.checkbox("Bias testuale (>=1)")

# --- GENERAZIONE VERDETTO ---
st.divider()
st.header("⚖️ 7. Valutazione Finale")

rischio = "BASSO"
if critici_totali >= 4 or i_crit: rischio = "ALTO"
elif 2 <= critici_totali <= 3: rischio = "MEDIO"

if rischio == "ALTO": st.error(f"🔴 RISCHIO {rischio}")
elif rischio == "MEDIO": st.warning(f"🟡 RISCHIO {rischio}")
else: st.success(f"🟢 RISCHIO {rischio}")

# --- COSTRUZIONE DEL TESTO DEL REPORT ---
data_attuale = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
report_txt = f"""--------------------------------------------------
REPORT DI CONFORMITÀ IA - TOOLKIT IMAGES
Progetto: PRIN PNRR
Data: {data_attuale}
--------------------------------------------------

LIVELLO DI RISCHIO COMPLESSIVO: {rischio}
Indicatori critici rilevati: {critici_totali}

DETTAGLIO AUDIT:
"""
if dettagli_audit:
    report_txt += "\n".join(dettagli_audit)
else:
    report_txt += "Nessuna criticità rilevata."

report_txt += f"\n\nControllo Rapido Output:\n- Bias Visivo: {'RILEVATO' if i_crit else 'NON RILEVATO'}\n- Bias Testuale: {'RILEVATO' if t_crit else 'NON RILEVATO'}"
report_txt += "\n\n--------------------------------------------------\nFine del Report"

# --- TASTO DI DOWNLOAD ---
st.download_button(
    label="📥 Scarica Report Ufficiale (.txt)",
    data=report_txt,
    file_name=f"Report_IMAGES_{datetime.now().strftime('%Y%m%d')}.txt",
    mime="text/plain"
)
