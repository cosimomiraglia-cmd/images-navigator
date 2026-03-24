import json
import streamlit as st
from datetime import datetime

# ═══════════════════════════════════════════════════════════
# CONFIGURAZIONE DELLA PAGINA
# ═══════════════════════════════════════════════════════════
st.set_page_config(
    page_title="IMAGES NAVIGATOR",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ═══════════════════════════════════════════════════════════
# PALETTE UFFICIALE PROGETTO PRIN PNRR
# ═══════════════════════════════════════════════════════════
C_PRIMARY = "#e3286d"
C_DARK    = "#565656"
C_MEDIUM  = "#a5a5a5"
C_BG      = "#e2ddd9"

# ═══════════════════════════════════════════════════════════
# CUSTOM CSS
# ═══════════════════════════════════════════════════════════
st.markdown(f"""
    <style>
    .stApp {{ background-color: {C_BG}; }}

    .stTabs [data-baseweb="tab-list"] {{
        gap: 15px;
        background-color: transparent;
        padding: 15px 0px;
    }}
    .stTabs [data-baseweb="tab"] {{
        height: 65px;
        border-radius: 10px;
        background-color: white;
        border: 2px solid {C_MEDIUM};
        padding: 0px 25px;
        transition: all 0.4s ease;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }}
    .stTabs [data-baseweb="tab"] p {{
        font-size: 15px;
        font-weight: 700;
        text-transform: uppercase;
        color: {C_DARK};
    }}
    .stTabs [aria-selected="true"] {{
        background-color: {C_PRIMARY} !important;
        border-color: {C_PRIMARY} !important;
        transform: translateY(-3px);
        box-shadow: 0 8px 15px rgba(227, 40, 109, 0.25);
    }}
    .stTabs [aria-selected="true"] p {{ color: white !important; }}

    .result-card {{
        background-color: white;
        padding: 28px;
        border-radius: 16px;
        box-shadow: 0 6px 20px rgba(0,0,0,0.08);
        margin-bottom: 10px;
    }}
    .measure-label {{
        font-size: 10px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        color: {C_MEDIUM};
        margin-bottom: 6px;
    }}
    .measure-value {{
        font-size: 15px;
        font-weight: 700;
        padding: 12px 14px;
        border-radius: 8px;
    }}
    h1, h2, h3, h4, .stButton button, .stDownloadButton button {{
        text-transform: uppercase;
        letter-spacing: 1px;
        color: {C_DARK} !important;
    }}
    .stTextInput input {{
        border-radius: 8px;
        border: 1px solid {C_MEDIUM};
        background-color: #ffffff;
    }}
    .stCheckbox [data-testid="stCheckboxUserIcon"] {{
        background-color: {C_PRIMARY};
    }}
    input:disabled {{
        opacity: 0.35 !important;
        background-color: #f9f9f9 !important;
    }}
    </style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════
# DOMINI APPLICATIVI
# Moltiplicatori ricalibrati: tetto minimo ×1.6
# ═══════════════════════════════════════════════════════════
DOMINI = {
    "GIUSTIZIA E SICUREZZA":    {"mult": 2.2, "threshold": 6.0},
    "SANITA E WELFARE":         {"mult": 2.0, "threshold": 6.0},
    "PUBBLICA AMMINISTRAZIONE": {"mult": 1.9, "threshold": 7.0},
    "FINANZA E CREDITO":        {"mult": 1.8, "threshold": 7.5},
    "ISTRUZIONE E RICERCA":     {"mult": 1.7, "threshold": 8.0},
    "RECRUITING E HR":          {"mult": 1.7, "threshold": 8.0},
    "MARKETING E MEDIA":        {"mult": 1.6, "threshold": 10.0},
    "GAMING E ENTERTAINMENT":   {"mult": 1.6, "threshold": 12.0},
}

# ═══════════════════════════════════════════════════════════
# BENCHMARK PERCENTILI
# Valori empirici: None finché non calibrati su dataset reale.
# Il fallback teorico usa threshold come proxy p75 e p75/3 come p25.
# ═══════════════════════════════════════════════════════════
PERCENTILI_BENCHMARK = {
    dominio: {"p25": None, "p75": None}
    for dominio in DOMINI
}

TUTTE_DIMENSIONI = [
    "genere", "etnia", "età",
    "disabilità", "orientamento", "status_socioeconomico"
]

# ═══════════════════════════════════════════════════════════
# MOLTIPLICATORE INTERSEZIONALE — Curva concava (Proposta B+)
#
# Logica: l'intersezionalità non è somma ma amplificazione.
# La curva concava (esponente 0.6) enfatizza il salto qualitativo
# nei primi assi attivi, coerentemente con la letteratura.
# Saturazione normalizzata su massimo teorico: 3 dim × 5 liv = 15.
# ═══════════════════════════════════════════════════════════
def get_intersectional_multiplier(n_dim, n_livelli, dominio):
    """
    n_dim     : n. dimensioni protette attive (dichiarate + rilevate)
    n_livelli : n. livelli pipeline con almeno un item spuntato
    dominio   : chiave DOMINI
    Restituisce il moltiplicatore ∈ [1.0, m_max].
    """
    if n_dim <= 1 or n_livelli <= 1:
        return 1.0

    m_max = DOMINI[dominio]["mult"]
    saturazione = (n_dim * n_livelli) / 15
    saturazione_curva = min(saturazione, 1.0) ** 0.6
    valore = 1.0 + (m_max - 1.0) * saturazione_curva
    return round(valore, 2)

# ═══════════════════════════════════════════════════════════
# METODO PERCENTILE CON FALLBACK TEORICO
#
# Se il benchmark empirico non è disponibile, usa:
#   p75 = threshold del dominio (proxy del 75° percentile)
#   p25 = p75 / 3              (terzile inferiore — difendibile come
#                               limite prudenziale del rischio basso)
# Il label "(Stima Teorica)" segnala all'utente l'assenza di dati reali.
# ═══════════════════════════════════════════════════════════
def esito_percentile(punteggio, dominio):
    p = PERCENTILI_BENCHMARK.get(dominio, {})
    soglia_teorica = DOMINI[dominio]["threshold"]

    p75 = p.get("p75") or soglia_teorica
    p25 = p.get("p25") or round(p75 / 3, 2)

    is_empirical = p.get("p75") is not None
    label_status = "" if is_empirical else " (Stima Teorica)"

    if punteggio >= p75:
        return f"🔴 ALTO (> 75° pct){label_status}", "#f8d7da", "#721c24"
    if punteggio <= p25:
        return f"🟢 BASSO (< 25° pct){label_status}", "#d4edda", "#155724"
    return f"🟡 MEDIO (25°–75° pct){label_status}", "#fff3cd", "#856404"

# ═══════════════════════════════════════════════════════════
# METODO CONTEGGIO — Metodo operativo IMAGES
#
# Soglie dal Toolkit IMAGES:
#   ≥ 4 indicatori critici → ALTO
#   2–3 indicatori critici → MEDIO
#   0–1 indicatori critici → BASSO
# ═══════════════════════════════════════════════════════════
def esito_conteggio(n):
    if n >= 4:
        return f"🔴 ALTO ({n} indicatori critici)", "#f8d7da", "#721c24"
    elif n >= 2:
        return f"🟡 MEDIO ({n} indicatori critici)", "#fff3cd", "#856404"
    else:
        return f"🟢 BASSO ({n} indicatori critici)", "#d4edda", "#155724"

def conta_critici_per_livello():
    """Restituisce {gruppo: n_critici} per visualizzazione breakdown."""
    return {
        gruppo: sum(
            1 for item in items
            if st.session_state.get(item["key"], False)
        )
        for gruppo, items in AUDIT_ITEMS.items()
    }

# ═══════════════════════════════════════════════════════════
# METODO PUNTEGGIO PESATO
#
# Usa il colore basato sul confronto con la soglia di dominio.
# ═══════════════════════════════════════════════════════════
def esito_punteggio(punteggio_finale, soglia):
    if punteggio_finale >= soglia:
        return f"🔴 ALTO ({punteggio_finale:.1f} / {soglia})", "#f8d7da", "#721c24"
    elif punteggio_finale >= soglia / 2:
        return f"🟡 MEDIO ({punteggio_finale:.1f} / {soglia})", "#fff3cd", "#856404"
    else:
        return f"🟢 BASSO ({punteggio_finale:.1f} / {soglia})", "#d4edda", "#155724"

# ═══════════════════════════════════════════════════════════
# STRUTTURA DATI DEGLI ITEM DI AUDIT
# ═══════════════════════════════════════════════════════════
AUDIT_ITEMS = {
    "PREP": [
        {"key": "prep_1", "label": "Definizione chiara del caso d'uso e del target di riferimento",
         "weight": 1.0, "dimensions": [], "level": "", "tag": "PREP"},
        {"key": "prep_2", "label": "Selezione degli indicatori di equità rilevanti per il dominio",
         "weight": 1.0, "dimensions": [], "level": "", "tag": "PREP"},
        {"key": "prep_3", "label": "Coinvolgimento preventivo degli stakeholder o gruppi vulnerabili",
         "weight": 1.0, "dimensions": ["genere", "etnia"], "level": "", "tag": "PREP"},
    ],
    "DATI": [
        {"key": "dat_1", "label": "Mancato confronto dei dati di training con la demografia reale",
         "weight": None, "dimensions": ["genere", "etnia", "età"], "level": "dati", "tag": "DATI"},
        {"key": "dat_2", "label": "Presenza di etichette storicamente stereotipate nel dataset",
         "weight": None, "dimensions": ["genere", "etnia"], "level": "dati", "tag": "DATI"},
        {"key": "dat_3", "label": "Assenza di strategie di riequilibrio per le classi minoritarie",
         "weight": None, "dimensions": ["genere", "etnia"], "level": "dati", "tag": "DATI"},
        {"key": "dat_4", "label": "Mancanza di documentazione strutturata sui rischi (es. Data Sheet)",
         "weight": None, "dimensions": [], "level": "dati", "tag": "DATI"},
    ],
    "TEAM": [
        {"key": "tea_1", "label": "Omogeneità demografica del team di sviluppo e design",
         "weight": None, "dimensions": ["genere", "etnia"], "level": "team", "tag": "TEAM"},
        {"key": "tea_2", "label": "Mancata identificazione di variabili proxy per gruppi protetti",
         "weight": None, "dimensions": ["genere", "etnia", "età", "disabilità"], "level": "team", "tag": "TEAM"},
        {"key": "tea_3", "label": "Mancanza di competenze DEI (Diversity, Equity, Inclusion) nel team",
         "weight": None, "dimensions": [], "level": "team", "tag": "TEAM"},
        {"key": "tea_4", "label": "Assenza di un registro decisionale tracciabile per le scelte di design",
         "weight": None, "dimensions": [], "level": "team", "tag": "TEAM"},
    ],
    "MODELLO": [
        {"key": "mod_1", "label": "Mancato calcolo delle metriche di performance disaggregate per gruppo",
         "weight": None, "dimensions": ["genere", "etnia", "età"], "level": "modello", "tag": "MODELLO"},
        {"key": "mod_2", "label": "Assenza di test mirati con prompt sensibili o avversariali",
         "weight": None, "dimensions": ["genere", "etnia"], "level": "modello", "tag": "MODELLO"},
        {"key": "mod_3", "label": "Model card non aggiornata o assente per gli utenti finali",
         "weight": None, "dimensions": [], "level": "modello", "tag": "MODELLO"},
        {"key": "mod_4", "label": "Mancata implementazione di filtri per mitigare le disparità rilevate",
         "weight": None, "dimensions": [], "level": "modello", "tag": "MODELLO"},
    ],
    "UTENTI": [
        {"key": "ute_1", "label": "Mancata analisi del rischio di echo-chamber o polarizzazione",
         "weight": None, "dimensions": [], "level": "utenti", "tag": "UTENTI"},
        {"key": "ute_2", "label": "Assenza di canali accessibili per segnalare output ingiusti",
         "weight": None, "dimensions": [], "level": "utenti", "tag": "UTENTI"},
        {"key": "ute_3", "label": "Interfaccia utente non accessibile o progettata in modo escludente",
         "weight": None, "dimensions": ["disabilità", "età"], "level": "utenti", "tag": "UTENTI"},
    ],
    "CONTESTO": [
        {"key": "con_1", "label": "Non conformità alle normative vigenti (es. AI Act, GDPR)",
         "weight": 2.5, "dimensions": [], "level": "contesto", "tag": "CONTESTO"},
        {"key": "con_2", "label": "Assenza di meccanismi di governance partecipativa e supervisione",
         "weight": 2.0, "dimensions": ["genere", "etnia"], "level": "contesto", "tag": "CONTESTO"},
        {"key": "con_3", "label": "Mancanza di valutazioni d'impatto sui diritti fondamentali periodiche",
         "weight": 2.0, "dimensions": [], "level": "contesto", "tag": "CONTESTO"},
    ],
}

def get_pesi_dinamici(dominio, w_dati, w_team, w_mod, w_ut):
    return {
        "dat_1": w_dati, "dat_2": w_dati, "dat_3": w_dati, "dat_4": w_dati,
        "tea_1": w_team, "tea_2": w_team, "tea_3": w_team, "tea_4": w_team,
        "mod_1": w_mod,  "mod_2": w_mod,  "mod_3": w_mod,  "mod_4": w_mod,
        "ute_1": w_ut,   "ute_2": w_ut,   "ute_3": w_ut,
    }

# ═══════════════════════════════════════════════════════════
# PARAMETRI IMMAGINI
# ═══════════════════════════════════════════════════════════
SCORE_IMG_GENDER = {
    "La figura tocca se stessa (auto-contatto)": 1.0,
    "La figura tocca un oggetto in modo non funzionale all'azione": 1.0,
    "Inquadratura frammentata (focus su dettagli del corpo, escluso il volto)": 1.0,
    "Nudità totale": 1.0,
    "Nudità parziale o abbigliamento esplicitamente succinto": 0.5,
    "Posa sdraiata, semi-reclinata o inginocchiata": 0.5,
    "Sguardo distolto (non rivolto verso l'osservatore)": 0.5,
    "Testa reclinata o inclinata di lato": 0.5,
    "Corpo inquadrato solo parzialmente": 0.5,
}

SCORE_IMG_INTERACT = {
    "Donne ritratte sorridenti, uomini con espressione seria": 1.0,
    "Donne in posa passiva/stazionaria, uomini impegnati in un'azione": 1.0,
    "Contesto domestico: solo la donna si occupa dei figli o delle faccende": 1.0,
    "Contesto professionale: l'uomo occupa il ruolo gerarchico superiore": 1.0,
    "Uomini al centro/primo piano, donne relegate allo sfondo": 1.0,
    "Uomini in piedi, donne sedute, sdraiate o inginocchiate": 1.0,
    "L'uomo è ritratto fisicamente più alto della donna": 1.0,
    "L'uomo guarda verso l'osservatore, la donna ha lo sguardo distolto": 1.0,
}

SCORE_IMG_ETHNIC = {
    "Persone bianche in primo piano, altre etnie relegate allo sfondo": 1.0,
    "Persone bianche ritratte fisicamente più alte degli altri soggetti": 1.0,
    "Contesto professionale: persone bianche in ruoli gerarchici superiori": 1.0,
    "Contesto domestico: solo persone di altre etnie svolgono mansioni di pulizia": 1.0,
}

ESCLUSIONI_MF = [
    "Posa sdraiata, semi-reclinata o inginocchiata",
    "Sguardo distolto (non rivolto verso l'osservatore)",
]

# ═══════════════════════════════════════════════════════════
# INIZIALIZZAZIONE SESSION STATE
# ═══════════════════════════════════════════════════════════
_defaults = {
    "punti_sistema": 0.0,
    "dettagli_audit": [],
    "punti_testo": 0,
    "dimensioni_rilevate": set(),
    "livelli_rilevati": set(),
    "_session_restored": False,
    "_session_timestamp": "",
    "_last_upload_hash": None,
    "_restored_dominio": "",
    "_restored_dimensioni": [],
}
for k, v in _defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ═══════════════════════════════════════════════════════════
# RENDERING ITEM AUDIT
# ═══════════════════════════════════════════════════════════
def render_audit_item(item, weight_override=None):
    col_check, col_note = st.columns([1.5, 1])
    with col_check:
        st.checkbox(item["label"], key=item["key"])
    with col_note:
        checked = st.session_state.get(item["key"], False)
        st.text_input(
            "Evidenza / Azione mitigativa",
            key=f"note_{item['key']}",
            placeholder="Specifica dettagli..." if checked else "—",
            disabled=not checked,
            label_visibility="visible" if checked else "collapsed",
        )

# ═══════════════════════════════════════════════════════════
# CALCOLO PUNTEGGIO
# ═══════════════════════════════════════════════════════════
def calcola_punteggio(pesi_dinamici):
    punteggio = 0.0
    dimensioni_rilevate = set()
    livelli_rilevati = set()
    dettagli = []

    for gruppo, items in AUDIT_ITEMS.items():
        for item in items:
            if st.session_state.get(item["key"], False):
                weight = pesi_dinamici.get(item["key"], item["weight"]) or 1.0
                punteggio += weight
                if item["dimensions"]:
                    dimensioni_rilevate.update(item["dimensions"])
                if item["level"]:
                    livelli_rilevati.add(item["level"])
                nota = st.session_state.get(f"note_{item['key']}", "").strip()
                dettagli.append(
                    f"[{item['tag']}] {item['label']} | "
                    f"Nota: {nota or 'Nessun dettaglio fornito'}"
                )

    return punteggio, dimensioni_rilevate, livelli_rilevati, dettagli

# ═══════════════════════════════════════════════════════════
# PROGRESSO AUDIT
# ═══════════════════════════════════════════════════════════
def calcola_progresso():
    sezioni_visitate = 0
    for gruppo, items in AUDIT_ITEMS.items():
        for item in items:
            if item["key"] in st.session_state:
                sezioni_visitate += 1
                break

    testi_visitati    = any(f"t_g{i}" in st.session_state for i in range(1, 8))
    immagini_visitate = any(
        f"img_f_{label}" in st.session_state for label in SCORE_IMG_GENDER
    )
    sezioni_visitate += int(testi_visitati) + int(immagini_visitate)
    totale = len(AUDIT_ITEMS) + 2
    pct = int((sezioni_visitate / totale) * 100)
    return sezioni_visitate, totale, pct

# ═══════════════════════════════════════════════════════════
# PERSISTENZA SESSIONE
# ═══════════════════════════════════════════════════════════
def serialize_session(info):
    dati_audit = {}
    for gruppo, items in AUDIT_ITEMS.items():
        for item in items:
            dati_audit[item["key"]] = st.session_state.get(item["key"], False)
            dati_audit[f"note_{item['key']}"] = st.session_state.get(f"note_{item['key']}", "")

    for k in [f"t_g{i}" for i in range(1, 8)] + [f"t_e{i}" for i in range(1, 5)]:
        dati_audit[k] = st.session_state.get(k, False)

    for label in SCORE_IMG_GENDER:
        dati_audit[f"img_f_{label}"]          = st.session_state.get(f"img_f_{label}", False)
        dati_audit[f"img_mf_inherit_{label}"] = st.session_state.get(f"img_mf_inherit_{label}", False)
    for label in SCORE_IMG_INTERACT:
        dati_audit[f"img_mf_{label}"] = st.session_state.get(f"img_mf_{label}", False)
    for label in SCORE_IMG_ETHNIC:
        dati_audit[f"img_e_{label}"] = st.session_state.get(f"img_e_{label}", False)

    return {
        "versione": "1.0",
        "timestamp": datetime.now().isoformat(),
        "info": info,
        "audit": dati_audit,
    }

def restore_session(payload):
    try:
        if payload.get("versione") != "1.0":
            return False, "Versione file non compatibile."
        for key, value in payload.get("audit", {}).items():
            st.session_state[key] = value
        st.session_state["_session_restored"] = True
        st.session_state["_session_timestamp"] = payload.get("timestamp", "—")
        info = payload.get("info", {})
        st.session_state["_restored_dominio"]    = info.get("dominio", "")
        st.session_state["_restored_dimensioni"] = info.get("dimensioni_dichiarate", [])
        return True, ""
    except Exception as e:
        return False, str(e)

# ═══════════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown(f"<h2 style='color:{C_PRIMARY};'>IMPOSTAZIONI</h2>",
                unsafe_allow_html=True)

    dominio_index = 0
    if st.session_state["_restored_dominio"] in DOMINI:
        dominio_index = list(DOMINI.keys()).index(st.session_state["_restored_dominio"])
    dominio_scelto = st.selectbox(
        "DOMINIO APPLICATIVO",
        list(DOMINI.keys()),
        index=dominio_index
    )

    st.divider()
    st.markdown("**DIMENSIONI PROTETTE**")
    st.caption("Seleziona quelle note a priori. Altre potranno emergere durante l'audit.")
    dimensioni_dichiarate = st.multiselect(
        "Dimensioni coinvolte dal sistema",
        options=TUTTE_DIMENSIONI,
        default=st.session_state.get("_restored_dimensioni", []),
        format_func=lambda x: x.replace("_", " ").title(),
        label_visibility="collapsed",
    )

    st.divider()
    n_vis, n_tot, pct = calcola_progresso()
    st.markdown("**AVANZAMENTO AUDIT**")
    st.progress(pct / 100)
    if pct == 100:
        colore_prog, stato_prog = "#28a745", "✅ Completato"
    elif pct >= 50:
        colore_prog, stato_prog = "#856404", f"In corso — {n_vis}/{n_tot} sezioni"
    else:
        colore_prog, stato_prog = "#a5a5a5", f"Avviato — {n_vis}/{n_tot} sezioni"
    st.markdown(
        f"<p style='font-size:12px;color:{colore_prog};margin-top:4px;'>{stato_prog}</p>",
        unsafe_allow_html=True
    )

    st.divider()
    st.markdown("**SESSIONE DI AUDIT**")
    if st.session_state["_session_restored"]:
        ts = st.session_state["_session_timestamp"]
        st.success(f"Sessione ripristinata\n{ts[:16].replace('T', ' ')}")

    info_correnti = {
        "dominio": dominio_scelto,
        "dimensioni_dichiarate": dimensioni_dichiarate,
    }
    session_json = json.dumps(
        serialize_session(info_correnti),
        ensure_ascii=False,
        indent=2
    )
    st.download_button(
        label="💾 Salva sessione",
        data=session_json,
        file_name=f"audit_session_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
        mime="application/json",
        use_container_width=True,
    )

    st.markdown("**Riprendi audit**")
    uploaded = st.file_uploader(
        "Carica file sessione (.json)",
        type=["json"],
        key="session_upload",
        label_visibility="collapsed",
    )
    if uploaded is not None:
        file_hash = hash(uploaded.getvalue())
        if st.session_state.get("_last_upload_hash") != file_hash:
            try:
                payload = json.loads(uploaded.getvalue())
                ok, errore = restore_session(payload)
                if ok:
                    st.session_state["_last_upload_hash"] = file_hash
                    st.rerun()
                else:
                    st.error(f"Errore nel ripristino: {errore}")
            except json.JSONDecodeError:
                st.error("File non valido. Carica un .json generato da questo strumento.")

    if st.button("🔄 Nuovo audit", use_container_width=True):
        preserve = {"session_upload", "_last_upload_hash"}
        for key in [k for k in st.session_state if k not in preserve]:
            del st.session_state[key]
        st.rerun()

    st.divider()
    st.markdown("**NOTA METODOLOGICA**")
    st.caption(
        "Strumento basato sul modello Four Levels (+1). "
        "Il metodo primario è il conteggio degli indicatori critici (Toolkit IMAGES). "
        "Il punteggio pesato e il percentile forniscono letture complementari."
    )

# ═══════════════════════════════════════════════════════════
# PESI DINAMICI PER DOMINIO
# ═══════════════════════════════════════════════════════════
w_dati  = 3.0 if dominio_scelto in ["SANITA E WELFARE", "GIUSTIZIA E SICUREZZA"] else 1.5
w_team  = 2.5 if dominio_scelto == "RECRUITING E HR" else 1.5
w_mod   = 3.0 if dominio_scelto in ["SANITA E WELFARE", "FINANZA E CREDITO"] else 2.0
w_ut    = 3.0 if dominio_scelto == "MARKETING E MEDIA" else 1.5
pesi_dinamici = get_pesi_dinamici(dominio_scelto, w_dati, w_team, w_mod, w_ut)

# ═══════════════════════════════════════════════════════════
# LAYOUT PRINCIPALE
# ═══════════════════════════════════════════════════════════
st.markdown(f"<h1 style='color:{C_PRIMARY};'>🛡️ IMAGES NAVIGATOR</h1>",
            unsafe_allow_html=True)
st.markdown("##### SISTEMA DI AUDIT PER L'INCLUSIVITÀ ALGORITMICA | PRIN PNRR")
st.write("")

col_input, col_risultati = st.columns([0.65, 0.35], gap="large")

# ═══════════════════════════════════════════════════════════
# COLONNA INPUT — TAB DI AUDIT
# ═══════════════════════════════════════════════════════════
with col_input:
    tabs = st.tabs([
        "PREPARAZIONE", "DATI", "TEAM",
        "MODELLO", "UTENTI", "CONTESTO",
        "TESTI", "IMMAGINI"
    ])

    with tabs[0]:
        st.subheader("FASE DI PREPARAZIONE")
        for item in AUDIT_ITEMS["PREP"]:
            render_audit_item(item)

    with tabs[1]:
        st.subheader("DATI")
        for item in AUDIT_ITEMS["DATI"]:
            render_audit_item(item, weight_override=w_dati)

    with tabs[2]:
        st.subheader("TEAM")
        for item in AUDIT_ITEMS["TEAM"]:
            render_audit_item(item, weight_override=w_team)

    with tabs[3]:
        st.subheader("MODELLO")
        for item in AUDIT_ITEMS["MODELLO"]:
            render_audit_item(item, weight_override=w_mod)

    with tabs[4]:
        st.subheader("UTENTI")
        for item in AUDIT_ITEMS["UTENTI"]:
            render_audit_item(item, weight_override=w_ut)

    with tabs[5]:
        st.subheader("CONTESTO")
        for item in AUDIT_ITEMS["CONTESTO"]:
            render_audit_item(item)

    with tabs[6]:
        st.subheader("ANALISI DEI TESTI")
        st.caption("La presenza di anche un solo elemento determina un rischio bias.")

        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**Stereotipi di genere**")
            t1  = st.checkbox("Uso di 'uomo/uomini' come sinonimo universale di umanità",                    key="t_g1")
            t2  = st.checkbox("Participio declinato al maschile in presenza di maggioranza femminile",        key="t_g2")
            t3  = st.checkbox("Uso asimmetrico di appellativi (es. 'Signora' vs titolo professionale)",       key="t_g3")
            t4  = st.checkbox("Titoli professionali declinati al maschile o con suffisso 'donna'",            key="t_g4")
            t5  = st.checkbox("Uso di aggettivi legati a fragilità emotiva o diminutivi",                     key="t_g5")
            t6  = st.checkbox("Identificazione relazionale della donna (es. 'la moglie di')",                 key="t_g6")
            t7  = st.checkbox("Uso di termini d'odio, misogini o metafore animali denigratorie",              key="t_g7")

        with c2:
            st.markdown("**Stereotipi etnici**")
            t8  = st.checkbox("Uso di stereotipi comparativi (es. 'fumare come un turco')",                   key="t_e1")
            t9  = st.checkbox("Antonomasia stereotipata basata sull'etnia (es. 'preciso come uno svizzero')", key="t_e2")
            t10 = st.checkbox("Uso di generalizzazioni o termini razzisti/obsoleti",                          key="t_e3")
            t11 = st.checkbox("Deumanizzazione tramite tratti o metafore animali",                            key="t_e4")

        st.session_state.punti_testo = (
            1 if any([t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11]) else 0
        )

    with tabs[7]:
        st.subheader("ANALISI DELLE IMMAGINI")
        st.caption("Calcolo dell'indice di rischio additivo basato su sistema a più variabili.")

        with st.expander("STEREOTIPI DI GENERE: PERSONAGGIO FEMMINILE SINGOLO"):
            score_f = 0.0
            for label, peso in SCORE_IMG_GENDER.items():
                if st.checkbox(label, key=f"img_f_{label}"):
                    score_f += peso
            if score_f > 4:   label_f = "ALTO"
            elif score_f > 2: label_f = "MEDIO"
            else:             label_f = "BASSO"
            st.markdown(f"**INDICE RISCHIO (F): {score_f} / 6.0 ({label_f})**")

        with st.expander("INTERAZIONE DI GENERE (MASCHILE E FEMMINILE)"):
            score_mf = 0.0
            for label, peso in SCORE_IMG_INTERACT.items():
                if st.checkbox(label, key=f"img_mf_{label}"):
                    score_mf += peso
            st.divider()
            st.caption("Variabili femminili applicabili al gruppo M/F:")
            for label, peso in SCORE_IMG_GENDER.items():
                if label not in ESCLUSIONI_MF:
                    if st.checkbox(label, key=f"img_mf_inherit_{label}"):
                        score_mf += peso
            if score_mf > 8:   label_mf = "ALTO"
            elif score_mf > 4: label_mf = "MEDIO"
            else:              label_mf = "BASSO"
            st.markdown(f"**INDICE RISCHIO (M/F): {score_mf} / 12.0 ({label_mf})**")

        with st.expander("STEREOTIPI ETNICI NEI GRUPPI"):
            score_e = 0.0
            for label, peso in SCORE_IMG_ETHNIC.items():
                if st.checkbox(label, key=f"img_e_{label}"):
                    score_e += peso
            if score_e >= 3:   label_e = "ALTO"
            elif score_e >= 2: label_e = "MEDIO"
            else:              label_e = "BASSO"
            st.markdown(f"**INDICE RISCHIO ETNICO: {score_e} / 4.0 ({label_e})**")

        st.session_state.max_score_img = max(score_f, score_mf, score_e)
        st.session_state.img_labels    = (label_f, label_mf, label_e)

# ═══════════════════════════════════════════════════════════
# CALCOLO PUNTEGGIO — indipendente dal tab attivo
# ═══════════════════════════════════════════════════════════
punteggio_base, dim_rilevate, liv_rilevati, dettagli_audit = calcola_punteggio(pesi_dinamici)

dimensioni_attive = set(dimensioni_dichiarate) | dim_rilevate
n_dim     = len(dimensioni_attive)
n_livelli = len(liv_rilevati)

moltiplicatore   = get_intersectional_multiplier(n_dim, n_livelli, dominio_scelto)
punteggio_finale = round(punteggio_base * moltiplicatore, 2)
soglia           = DOMINI[dominio_scelto]["threshold"]

# Conteggio indicatori critici (metodo IMAGES primario)
n_critici        = sum(
    1 for items in AUDIT_ITEMS.values()
    for item in items
    if st.session_state.get(item["key"], False)
)
critici_per_livello = conta_critici_per_livello()

# ═══════════════════════════════════════════════════════════
# COLONNA RISULTATI — SCORECARD A TRE MISURE
# ═══════════════════════════════════════════════════════════
with col_risultati:

    audit_avviato = n_critici > 0 or st.session_state.get("punti_testo", 0) > 0

    if not audit_avviato:
        st.markdown(f"""
            <div style='background:white; border:1px dashed {C_MEDIUM};
                        border-radius:16px; padding:40px 24px;
                        text-align:center; margin-top:15px;'>
                <div style='font-size:32px; margin-bottom:12px;'>🛡️</div>
                <p style='color:{C_MEDIUM}; font-size:14px; margin:0;
                          text-transform:uppercase; letter-spacing:1px;'>
                    Completa almeno una sezione<br>per visualizzare la scorecard
                </p>
            </div>
        """, unsafe_allow_html=True)

    else:
        # ── Calcola i tre esiti ──────────────────────────────────────
        lbl_cnt, bg_cnt, fg_cnt   = esito_conteggio(n_critici)
        lbl_pts, bg_pts, fg_pts   = esito_punteggio(punteggio_finale, soglia)
        lbl_pct, bg_pct, fg_pct   = esito_percentile(punteggio_finale, dominio_scelto)

        # ── MISURA 1: Conteggio indicatori (IMAGES puro) — PRIMARIA ──
        st.markdown(f"""
            <div class="result-card" style="border-top: 6px solid {C_PRIMARY};">
                <div class="measure-label">① METODO IMAGES — CONTEGGIO INDICATORI</div>
                <div class="measure-value" style="background:{bg_cnt}; color:{fg_cnt};">
                    {lbl_cnt}
                </div>
            </div>
        """, unsafe_allow_html=True)

        # Breakdown per livello
        with st.expander("Dettaglio per livello"):
            for gruppo, n in critici_per_livello.items():
                _, bg, fg = esito_conteggio(n)
                st.markdown(f"""
                    <div style="display:flex; justify-content:space-between;
                                align-items:center; padding:5px 0;
                                border-bottom:1px solid #eee; font-size:13px;">
                        <span style="color:{C_DARK}; font-weight:600;">{gruppo}</span>
                        <span style="background:{bg}; color:{fg}; padding:2px 10px;
                                     border-radius:6px; font-weight:700; font-size:12px;">
                            {n} critici
                        </span>
                    </div>
                """, unsafe_allow_html=True)

        # ── MISURA 2: Punteggio pesato con moltiplicatore ────────────
        st.markdown(f"""
            <div class="result-card" style="border-top: 6px solid {C_MEDIUM};">
                <div class="measure-label">② PUNTEGGIO PESATO (× INTERSEZIONALE)</div>
                <div class="measure-value" style="background:{bg_pts}; color:{fg_pts};">
                    {lbl_pts}
                </div>
            </div>
        """, unsafe_allow_html=True)

        # Dettaglio intersezionale — solo se attivo
        if moltiplicatore > 1.0:
            dim_labels = ", ".join(
                d.replace("_", " ").title() for d in sorted(dimensioni_attive)
            )
            liv_labels = ", ".join(l.title() for l in sorted(liv_rilevati))
            st.markdown(f"""
                <div style="background:#fdf0f5; border:1px solid {C_PRIMARY};
                            border-radius:8px; padding:10px 14px; margin-top:-6px;
                            margin-bottom:10px; font-size:12px; color:{C_DARK};">
                    <strong style="color:{C_PRIMARY};">
                        ⚠️ Intersezionale attivo ×{moltiplicatore}
                    </strong><br>
                    Dim.: {dim_labels or '—'} &nbsp;|&nbsp; Livelli: {liv_labels or '—'}
                </div>
            """, unsafe_allow_html=True)

        # ── MISURA 3: Percentile ─────────────────────────────────────
        st.markdown(f"""
            <div class="result-card" style="border-top: 6px solid {C_MEDIUM};">
                <div class="measure-label">③ POSIZIONE PERCENTILE</div>
                <div class="measure-value" style="background:{bg_pct}; color:{fg_pct};">
                    {lbl_pct}
                </div>
            </div>
        """, unsafe_allow_html=True)

        # ── Stato output Testi e Immagini ────────────────────────────
        testo_status = (
            "🔴 RISCHIO RILEVATO"
            if st.session_state.get("punti_testo", 0) > 0
            else "🟢 Nessun rischio"
        )
        img_labels = st.session_state.get("img_labels", ("BASSO", "BASSO", "BASSO"))
        if "ALTO" in img_labels:
            img_status = "🔴 RISCHIO ALTO"
        elif "MEDIO" in img_labels:
            img_status = "🟡 RISCHIO MEDIO"
        else:
            img_status = "🟢 Rischio basso"

        st.markdown(f"""
            <div class="result-card">
                <div class="measure-label">STATO DEGLI OUTPUT</div>
                <p style="margin:6px 0; color:{C_DARK}; font-size:14px;">
                    <strong>TESTI:</strong> {testo_status}
                </p>
                <p style="margin:6px 0; color:{C_DARK}; font-size:14px;">
                    <strong>IMMAGINI:</strong> {img_status}
                </p>
            </div>
        """, unsafe_allow_html=True)

        st.write("")

        # ── Report scaricabile ───────────────────────────────────────
        report_data  = f"AUDIT IMAGES NAVIGATOR — {dominio_scelto}\n"
        report_data += f"DATA: {datetime.now().strftime('%d/%m/%Y %H:%M')}\n"
        report_data += "=" * 50 + "\n"
        report_data += "METODO IMAGES (CONTEGGIO):\n"
        report_data += f"  Indicatori critici totali: {n_critici}\n"
        report_data += f"  Esito: {lbl_cnt}\n"
        report_data += "  Dettaglio per livello:\n"
        for gruppo, n in critici_per_livello.items():
            report_data += f"    {gruppo}: {n} critici\n"
        report_data += "-" * 50 + "\n"
        report_data += "PUNTEGGIO PESATO:\n"
        report_data += f"  Base: {punteggio_base:.2f}\n"
        report_data += f"  Moltiplicatore intersezionale: ×{moltiplicatore}\n"
        report_data += f"  Finale: {punteggio_finale:.2f} (soglia dominio: {soglia})\n"
        report_data += f"  Esito: {lbl_pts}\n"
        if moltiplicatore > 1.0:
            report_data += f"  Dimensioni: {', '.join(sorted(dimensioni_attive))}\n"
            report_data += f"  Livelli implicati: {', '.join(sorted(liv_rilevati))}\n"
        report_data += "-" * 50 + "\n"
        report_data += f"PERCENTILE: {lbl_pct}\n"
        report_data += "-" * 50 + "\n"
        report_data += f"TESTI: {testo_status}\n"
        report_data += (
            f"IMMAGINI: {img_status} "
            f"(F: {img_labels[0]}, M/F: {img_labels[1]}, ETNIA: {img_labels[2]})\n"
        )
        report_data += "=" * 50 + "\n"
        report_data += "DETTAGLIO EVIDENZE:\n"
        report_data += (
            "\n".join(dettagli_audit)
            if dettagli_audit
            else "Nessuna evidenza registrata."
        )

        st.download_button(
            label="SCARICA REPORT TECNICO",
            data=report_data,
            file_name=f"AUDIT_{dominio_scelto.replace(' ', '_')}.txt",
            use_container_width=True,
        )

# ═══════════════════════════════════════════════════════════
# FOOTER
# ═══════════════════════════════════════════════════════════
st.divider()
st.caption(f"PROGETTO PRIN PNRR | IMAGES | {datetime.now().year}")
