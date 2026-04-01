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
    /* Stile per i radio button come gruppo di opzioni */
    div[data-testid="stRadio"] > div[role="radiogroup"] {{
        gap: 6px;
    }}
    div[data-testid="stRadio"] > div[role="radiogroup"] label {{
        border: 1.5px solid {C_MEDIUM};
        border-radius: 6px;
        padding: 4px 12px;
        background: white;
        font-size: 13px;
        font-weight: 500;
        transition: all 0.15s;
    }}
    .item-divider {{
        border: none;
        border-top: 1px solid #ede9e1;
        margin: 10px 0;
    }}
    </style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════
# DOMINI APPLICATIVI
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
# STATO ITEM — tre valori possibili
# "SI"  → verificato, nessun problema → contributo rischio = 0
# "NO"  → verificato, problema rilevato → contributo rischio = peso pieno
# "NV"  → non ancora verificato / non applicabile → contributo = 0
#          ma decrementa la copertura
# ═══════════════════════════════════════════════════════════
STATO_OPTIONS  = ["NV", "SI", "NO"]
STATO_LABELS   = {
    "NV": "N.A.",
    "SI": "Sì",
    "NO": "No",
}

# ═══════════════════════════════════════════════════════════
# MOLTIPLICATORE INTERSEZIONALE — curva concava
# ═══════════════════════════════════════════════════════════
def get_intersectional_multiplier(n_dim, n_livelli, dominio):
    if n_dim <= 1 or n_livelli <= 1:
        return 1.0
    m_max = DOMINI[dominio]["mult"]
    saturazione = (n_dim * n_livelli) / 15
    saturazione_curva = min(saturazione, 1.0) ** 0.6
    valore = 1.0 + (m_max - 1.0) * saturazione_curva
    return round(valore, 2)

# ═══════════════════════════════════════════════════════════
# METODO CONTEGGIO — metodo operativo IMAGES
# ═══════════════════════════════════════════════════════════
def esito_conteggio(n):
    if n >= 4:
        return f"🔴 ALTO ({n} problemi rilevati)", "#f8d7da", "#721c24"
    elif n >= 2:
        return f"🟡 MEDIO ({n} problemi rilevati)", "#fff3cd", "#856404"
    else:
        return f"🟢 BASSO ({n} problemi rilevati)", "#d4edda", "#155724"

def conta_critici_per_livello():
    return {
        gruppo: sum(
            1 for item in items
            if st.session_state.get(item["key"], "NV") == "NO"
        )
        for gruppo, items in AUDIT_ITEMS.items()
    }

# ═══════════════════════════════════════════════════════════
# METODO PUNTEGGIO PESATO
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
# Label riformulati come domande valutative — contenuto invariato
# rispetto alle linee guida IMAGES.
# Stato "NO" = problema rilevato (contribuisce al rischio).
# ═══════════════════════════════════════════════════════════
AUDIT_ITEMS = {
    "PREP": [
        {"key": "prep_1",
         "label": "Il caso d'uso del sistema è stato chiaramente definito e documentato?",
         "help": None,
         "weight": 1.0, "dimensions": [], "level": "", "tag": "PREP"},
        {"key": "prep_2",
         "label": "Il target di utenti e le popolazioni impattate dal sistema sono stati identificati?",
         "help": None,
         "weight": 1.0, "dimensions": [], "level": "", "tag": "PREP"},
        {"key": "prep_3",
         "label": "Per ciascun gruppo identificato, sono state valutate le possibili forme di discriminazione a cui potrebbe essere esposto (es. di genere, etnica, per età, per disabilità)?",
         "help": None,
         "weight": 1.0, "dimensions": ["genere", "etnia", "età", "disabilità"], "level": "", "tag": "PREP"},
        {"key": "prep_4",
         "label": "Gruppi marginalizzati o potenzialmente impattati sono stati coinvolti nella fase di progettazione?",
         "help": None,
         "weight": 1.0, "dimensions": ["genere", "etnia"], "level": "", "tag": "PREP"},
    ],
    "DATI": [
        {"key": "dat_1",
         "label": "I dati di training includono esempi rappresentativi di tutti i gruppi demografici rilevanti per il caso d'uso?",
         "help": "Es. un sistema di riconoscimento facciale addestrato su immagini che includono persone di diverse età, etnie e generi in proporzioni simili a quelle della popolazione che utilizzerà il sistema.",
         "weight": None, "dimensions": ["genere", "etnia", "età"], "level": "dati", "tag": "DATI"},
        {"key": "dat_2",
         "label": "Le etichette del dataset sono state verificate per escludere associazioni stereotipate o discriminatorie?",
         "help": "Le etichette sono le categorie o annotazioni usate per classificare i dati. Es. un dataset di immagini professionali in cui \"medico\" è associato quasi esclusivamente a figure maschili e \"infermiere\" a figure femminili.",
         "weight": None, "dimensions": ["genere", "etnia"], "level": "dati", "tag": "DATI"},
        {"key": "dat_3",
         "label": "Eventuali squilibri nella rappresentazione dei gruppi sono stati corretti con strategie specifiche?",
         "help": "Se alcuni gruppi sono numericamente minoritari nel dataset, tecniche come oversampling o pesatura dei campioni possono correggere lo squilibrio. Rilevante soprattutto se l'item precedente ha evidenziato problemi di rappresentatività.",
         "weight": None, "dimensions": ["genere", "etnia"], "level": "dati", "tag": "DATI"},
        {"key": "dat_4",
         "label": "Il dataset è documentato in modo da rendere tracciabili origine, limiti e rischi noti?",
         "help": "Un Data Sheet descrive origine, composizione, limitazioni e rischi noti del dataset. Non deve necessariamente chiamarsi così: va bene qualsiasi documento che renda tracciabili queste informazioni per chi usa o audita il sistema.",
         "weight": None, "dimensions": [], "level": "dati", "tag": "DATI"},
    ],
    "TEAM": [
        {"key": "tea_1",
         "label": "Il team include o ha consultato prospettive diverse per genere, etnia e background disciplinare?",
         "help": "Es. un team che include oltre agli ingegneri anche figure con competenze in scienze sociali, diritto antidiscriminatorio o design dell'accessibilità.",
         "weight": None, "dimensions": ["genere", "etnia"], "level": "team", "tag": "TEAM"},
        {"key": "tea_2",
         "label": "Le variabili del sistema sono state verificate per escludere l'uso indiretto di caratteristiche sensibili come genere o etnia?",
         "help": "Una variabile proxy è un dato apparentemente neutro che in realtà riflette indirettamente una caratteristica sensibile. Es. il codice postale come indicatore indiretto di etnia o classe sociale, il nome come indicatore di genere o origine culturale.",
         "weight": None, "dimensions": ["genere", "etnia", "età", "disabilità"], "level": "team", "tag": "TEAM"},
        {"key": "tea_3",
         "label": "Il team include o ha consultato competenze specifiche in ambito di equità, diversità e inclusione?",
         "help": "Es. consulenza con associazioni che rappresentano gruppi marginalizzati, revisione esterna da parte di esperti di discriminazione algoritmica, o formazione specifica del team su questi temi.",
         "weight": None, "dimensions": [], "level": "team", "tag": "TEAM"},
        {"key": "tea_4",
         "label": "Le scelte progettuali rilevanti sono documentate con la relativa motivazione?",
         "help": "Es. un documento che riporti perché sono state scelte certe variabili di input, quali alternative sono state scartate e con quale motivazione — utile sia per l'audit interno che per la rendicontazione esterna.",
         "weight": None, "dimensions": [], "level": "team", "tag": "TEAM"},
    ],
    "MODELLO": [
        {"key": "mod_1",
         "label": "Le metriche di performance sono state calcolate separatamente per i gruppi demografici rilevanti, non solo in aggregato?",
         "help": "Es. un sistema di selezione del credito che ha un'accuratezza complessiva del 90% ma produce errori sistematici per le donne o per determinate etnie — un problema invisibile guardando solo il dato aggregato.",
         "weight": None, "dimensions": ["genere", "etnia", "età"], "level": "modello", "tag": "MODELLO"},
        {"key": "mod_2",
         "label": "Il sistema produce risultati coerenti quando gli input variano solo per caratteristiche demografiche?",
         "help": "Es. due profili identici in tutto tranne che per il nome — uno tipicamente maschile, uno femminile — producono la stessa risposta dal sistema.",
         "weight": None, "dimensions": ["genere", "etnia"], "level": "modello", "tag": "MODELLO"},
        {"key": "mod_3",
         "label": "Il sistema è documentato con i suoi limiti, i casi d'uso per cui non è stato validato e i gruppi per cui le performance potrebbero essere ridotte?",
         "help": "Es. \"questo sistema è stato sviluppato e testato su popolazione adulta italiana — l'uso su altri contesti geografici o demografici richiede una nuova validazione\".",
         "weight": None, "dimensions": [], "level": "modello", "tag": "MODELLO"},
        {"key": "mod_4",
         "label": "Quando sono state rilevate disparità di performance tra gruppi, sono state adottate misure correttive?",
         "help": "Es. se il sistema mostrava tassi di approvazione diversi per uomini e donne con lo stesso profilo, sono stati introdotti aggiustamenti che hanno ridotto o eliminato il divario.",
         "weight": None, "dimensions": [], "level": "modello", "tag": "MODELLO"},
    ],
    "UTENTI": [
        {"key": "ute_1",
         "label": "Il sistema è stato valutato rispetto al rischio di amplificare contenuti polarizzanti o di limitare la diversità delle informazioni a cui gli utenti sono esposti?",
         "help": None,
         "weight": None, "dimensions": [], "level": "utenti", "tag": "UTENTI"},
        {"key": "ute_2",
         "label": "Gli utenti hanno un modo semplice e diretto per segnalare quando il sistema produce un risultato che percepiscono come scorretto o discriminatorio?",
         "help": None,
         "weight": None, "dimensions": [], "level": "utenti", "tag": "UTENTI"},
        {"key": "ute_3",
         "label": "L'interfaccia è stata progettata per essere accessibile a utenti con esigenze e abilità diverse?",
         "help": None,
         "weight": None, "dimensions": ["disabilità", "età"], "level": "utenti", "tag": "UTENTI"},
    ],
    "CONTESTO": [
        {"key": "con_1",
         "label": "Il sistema è conforme alle normative vigenti in materia (es. AI Act, GDPR)?",
         "help": None,
         "weight": 2.5, "dimensions": [], "level": "contesto", "tag": "CONTESTO"},
        {"key": "con_2",
         "label": "Le persone o i gruppi direttamente impattati dal sistema hanno avuto modo di contribuire alla sua progettazione o di esprimere feedback sul suo funzionamento?",
         "help": None,
         "weight": 2.0, "dimensions": ["genere", "etnia"], "level": "contesto", "tag": "CONTESTO"},
        {"key": "con_3",
         "label": "È stata condotta una valutazione degli effetti che il sistema potrebbe produrre sui diritti e le opportunità delle persone che ne sono influenzate?",
         "help": None,
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
    "dettagli_audit": [],
    "punti_testo": 0,
    "_session_restored": False,
    "_session_timestamp": "",
    "_last_upload_hash": None,
    "_restored_dominio": "",
    "_restored_dimensioni": [],
    "_onboarding_done": False,
    "_migrazione_v1": False,
}
for k, v in _defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# Pre-inizializzazione di tutti i key degli item audit a "NV".
# Deve avvenire qui — prima di qualsiasi widget, sidebar inclusa —
# perché Streamlit inizializza i radio button alla prima opzione ("SI")
# se il key non è ancora presente in session_state al momento del render.
# La sidebar esegue prima dei tab, quindi calcola_copertura() leggerebbe
# valori "SI" se questa inizializzazione avvenisse più tardi.
# La condizione `not in STATO_OPTIONS` gestisce anche valori anomali
# da versioni precedenti del file di sessione.
for _gruppo, _items in AUDIT_ITEMS.items():
    for _item in _items:
        if st.session_state.get(_item["key"]) not in STATO_OPTIONS:
            st.session_state[_item["key"]] = "NV"

# ═══════════════════════════════════════════════════════════
# RENDERING ITEM AUDIT
# Tre stati: SI / NO / NV
# Il campo note appare solo quando lo stato è NO.
# Il valore della nota è preservato in session_state anche
# quando il campo non è visibile.
# ═══════════════════════════════════════════════════════════
def render_audit_item(item, weight_override=None):
    # Guardia secondaria: gestisce casi residui in cui il key fosse
    # arrivato con un valore non ammesso nonostante la pre-inizializzazione.
    if st.session_state.get(item["key"]) not in STATO_OPTIONS:
        st.session_state[item["key"]] = "NV"

    stato_corrente = st.session_state.get(item["key"], "NV")

    col_q, col_note = st.columns([1.6, 1])

    with col_q:
        st.radio(
            label=item["label"],
            options=STATO_OPTIONS,
            format_func=lambda x: STATO_LABELS[x],
            key=item["key"],
            horizontal=True,
        )
        # Testo di aiuto sempre visibile, in corsivo grigio
        if item.get("help"):
            st.markdown(
                f"<div style='font-size:12px; color:{C_MEDIUM}; "
                f"font-style:italic; margin-top:2px; margin-bottom:4px; "
                f"line-height:1.5;'>{item['help']}</div>",
                unsafe_allow_html=True
            )

    with col_note:
        if stato_corrente == "NO":
            st.text_input(
                "Evidenza o azione prevista",
                key=f"note_{item['key']}",
                placeholder="Descrivi il problema o l'azione correttiva...",
                label_visibility="collapsed",
            )

    st.markdown("<hr class='item-divider'>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════
# CALCOLO PUNTEGGIO
# Solo gli item con stato "NO" contribuiscono al rischio.
# ═══════════════════════════════════════════════════════════
def calcola_punteggio(pesi_dinamici):
    punteggio = 0.0
    dimensioni_rilevate = set()
    livelli_rilevati = set()
    dettagli = []

    for gruppo, items in AUDIT_ITEMS.items():
        for item in items:
            if st.session_state.get(item["key"], "NV") == "NO":
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
# COPERTURA AUDIT
# Misura quanti item sono stati effettivamente valutati
# (stato SI o NO) rispetto al totale.
# Gli item NV non contribuiscono alla copertura.
# ═══════════════════════════════════════════════════════════
def calcola_copertura():
    totale = sum(len(items) for items in AUDIT_ITEMS.values())
    verificati = sum(
        1 for items in AUDIT_ITEMS.values()
        for item in items
        if st.session_state.get(item["key"], "NV") in ("SI", "NO")
    )
    pct = int((verificati / totale) * 100) if totale > 0 else 0
    return verificati, totale, pct

# ═══════════════════════════════════════════════════════════
# PERSISTENZA SESSIONE
# ═══════════════════════════════════════════════════════════
def serialize_session(info):
    dati_audit = {}
    for gruppo, items in AUDIT_ITEMS.items():
        for item in items:
            dati_audit[item["key"]] = st.session_state.get(item["key"], "NV")
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
        "versione": "1.1",
        "timestamp": datetime.now().isoformat(),
        "info": info,
        "audit": dati_audit,
    }

def restore_session(payload):
    try:
        migrazione_effettuata = False
        for key, value in payload.get("audit", {}).items():
            # Migrazione dalla versione 1.0 (booleani) alla 1.1 (stringhe SI/NO/NV).
            # True → "NO" (mancanza rilevata = problema rilevato, framing invertito).
            # False → "NV": nel vecchio sistema False poteva significare sia "verificato
            # e in ordine" sia "non ancora verificato". La conversione conservativa in
            # "NV" è più onesta che assumere falsamente la verifica — l'utente rivaluterà.
            if isinstance(value, bool):
                st.session_state[key] = "NO" if value else "NV"
                migrazione_effettuata = True
            else:
                st.session_state[key] = value
        st.session_state["_session_restored"]  = True
        st.session_state["_session_timestamp"] = payload.get("timestamp", "—")
        st.session_state["_migrazione_v1"]     = migrazione_effettuata
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
        "DOMINIO APPLICATIVO", list(DOMINI.keys()), index=dominio_index
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
    # Avanzamento basato sulla copertura
    n_ver, n_tot_cov, pct_cov = calcola_copertura()
    st.markdown("**COPERTURA AUDIT**")
    st.progress(pct_cov / 100)
    if pct_cov == 100:
        colore_prog, stato_prog = "#28a745", "✅ Tutti gli item verificati"
    elif pct_cov >= 50:
        colore_prog, stato_prog = "#856404", f"In corso — {n_ver}/{n_tot_cov} item"
    else:
        colore_prog, stato_prog = "#a5a5a5", f"Avviato — {n_ver}/{n_tot_cov} item"
    st.markdown(
        f"<p style='font-size:12px;color:{colore_prog};margin-top:4px;'>{stato_prog}</p>",
        unsafe_allow_html=True
    )

    st.divider()
    st.markdown("**SESSIONE DI AUDIT**")
    if st.session_state["_session_restored"]:
        ts = st.session_state["_session_timestamp"]
        st.success(f"Sessione ripristinata\n{ts[:16].replace('T', ' ')}")
        if st.session_state.get("_migrazione_v1"):
            st.warning(
                "⚠️ File da versione precedente. Gli item non problematici "
                "sono stati impostati a 'Non verificato' — rivalutali per "
                "una copertura accurata."
            )

    info_correnti = {
        "dominio": dominio_scelto,
        "dimensioni_dichiarate": dimensioni_dichiarate,
    }
    session_json = json.dumps(
        serialize_session(info_correnti), ensure_ascii=False, indent=2
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
                payload_data = json.loads(uploaded.getvalue())
                ok, errore = restore_session(payload_data)
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
    # Pulsante per riaprire la guida introduttiva in qualsiasi momento
    if st.button("❓ Guida introduttiva", use_container_width=True):
        st.session_state["_onboarding_done"] = False
        # Il click sul pulsante causa già un rerun automatico.
        # st.rerun() esplicito dentro with st.sidebar può essere
        # instabile in alcune versioni di Streamlit — non necessario.

    st.divider()
    st.markdown("**NOTA METODOLOGICA**")
    st.caption(
        "Strumento basato sul modello Four Levels (+1). "
        "Risponde 'No' solo quando il problema è stato rilevato e verificato. "
        "La copertura misura la completezza dell'audit, indipendentemente dal rischio."
    )

# ═══════════════════════════════════════════════════════════
# ONBOARDING — mostrato al primo accesso e su richiesta
# ═══════════════════════════════════════════════════════════
if not st.session_state["_onboarding_done"]:

    # Logo progetto — sostituire il percorso con il PNG del logo reale
    st.image("Logo_Images.png", width=180)
    st.markdown(f"""
        <div style="max-width:800px; margin:0 auto; padding-top:20px;">
        <div style="background:linear-gradient(140deg,#1B2D45 0%,#2A4060 100%);
                    border-radius:16px; padding:40px 44px 36px; color:white;
                    margin-bottom:28px;">
            <div style="font-size:11px; font-weight:700; letter-spacing:2px;
                        color:rgba(255,255,255,0.5); text-transform:uppercase;
                        margin-bottom:10px;">
                Progetto PRIN PNRR · IMAGES
            </div>
            <div style="font-size:36px; font-weight:800; margin-bottom:10px;
                        color:white; letter-spacing:-0.5px;">
                IMAGES NAVIGATOR
            </div>
            <div style="font-size:16px; opacity:0.85; line-height:1.6; max-width:580px;">
                Uno strumento di supporto per chi sviluppa sistemi di intelligenza
                artificiale e vuole valutare — e migliorare — la loro inclusività
                rispetto a genere ed etnia.
            </div>
        </div>
        </div>
    """, unsafe_allow_html=True)

    col_ob1, col_ob2 = st.columns(2, gap="medium")

    with col_ob1:
        st.markdown(f"""
            <div style="background:white; border-radius:12px; padding:24px 26px;
                        border-left:5px solid {C_PRIMARY}; margin-bottom:16px;">
                <div style="font-size:11px; font-weight:700; letter-spacing:1.5px;
                            color:{C_MEDIUM}; text-transform:uppercase; margin-bottom:10px;">
                    Il progetto
                </div>
                <p style="color:{C_DARK}; font-size:14px; line-height:1.65; margin:0;">
                    IMAGES Navigator nasce nell'ambito del progetto
                    <strong>IMAGES</strong> (<em>Inclusive Machine Learning using
                    Art and Culture for tackling Gender and Ethnicity Stereotypes</em>),
                    finanziato dal PRIN PNRR e coordinato da Sapienza Università di Roma
                    e ISTC-CNR.<br><br>
                    Lo strumento operazionalizza il modello teorico
                    <strong>Four Levels (+1)</strong> (Panarese, Grasso e Solinas, 2025),
                    che interpreta il bias algoritmico come esito di un processo
                    sociotecnico distribuito su cinque dimensioni: dati, team, modello,
                    utenti e contesto.
                </p>
            </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
            <div style="background:white; border-radius:12px; padding:24px 26px;
                        border-left:5px solid {C_MEDIUM}; margin-bottom:16px;">
                <div style="font-size:11px; font-weight:700; letter-spacing:1.5px;
                            color:{C_MEDIUM}; text-transform:uppercase; margin-bottom:10px;">
                    A chi è rivolto
                </div>
                <p style="color:{C_DARK}; font-size:14px; line-height:1.65; margin:0;">
                    A chiunque sia coinvolto nello sviluppo o nella valutazione di
                    sistemi IA: sviluppatori, designer, ricercatori, product manager,
                    policy maker, auditor. Non richiede competenze avanzate di
                    machine learning.
                </p>
            </div>
        """, unsafe_allow_html=True)

    with col_ob2:
        st.markdown(f"""
            <div style="background:white; border-radius:12px; padding:24px 26px;
                        border-left:5px solid {C_PRIMARY}; margin-bottom:16px;">
                <div style="font-size:11px; font-weight:700; letter-spacing:1.5px;
                            color:{C_MEDIUM}; text-transform:uppercase; margin-bottom:10px;">
                    Come funziona
                </div>
                <p style="color:{C_DARK}; font-size:14px; line-height:1.65; margin:0;">
                    Lo strumento pone domande di verifica su cinque livelli della
                    pipeline (Dati, Team, Modello, Utenti, Contesto) più due moduli
                    per testi e immagini. Per ogni domanda hai tre opzioni:
                </p>
                <div style="margin-top:14px;">
                    <div style="display:flex; align-items:flex-start; gap:10px;
                                margin-bottom:10px;">
                        <span style="background:#d4edda; color:#155724; padding:3px 12px;
                                     border-radius:5px; font-size:12px; font-weight:700;
                                     flex-shrink:0; white-space:nowrap;">Sì</span>
                        <span style="color:{C_DARK}; font-size:13px; line-height:1.5;">
                            Ho verificato questo aspetto e non ho rilevato problemi</span>
                    </div>
                    <div style="display:flex; align-items:flex-start; gap:10px;
                                margin-bottom:10px;">
                        <span style="background:#f8d7da; color:#721c24; padding:3px 12px;
                                     border-radius:5px; font-size:12px; font-weight:700;
                                     flex-shrink:0; white-space:nowrap;">No</span>
                        <span style="color:{C_DARK}; font-size:13px; line-height:1.5;">
                            Ho verificato questo aspetto e ho rilevato una criticità</span>
                    </div>
                    <div style="display:flex; align-items:flex-start; gap:10px;">
                        <span style="background:#f3f4f6; color:#6b7280; padding:3px 12px;
                                     border-radius:5px; font-size:12px; font-weight:700;
                                     flex-shrink:0; white-space:nowrap;">N.A.</span>
                        <span style="color:{C_DARK}; font-size:13px; line-height:1.5;">
                            Non ho ancora esaminato questo aspetto, oppure non è
                            pertinente al mio sistema</span>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
            <div style="background:white; border-radius:12px; padding:24px 26px;
                        border-left:5px solid {C_MEDIUM}; margin-bottom:16px;">
                <div style="font-size:11px; font-weight:700; letter-spacing:1.5px;
                            color:{C_MEDIUM}; text-transform:uppercase; margin-bottom:10px;">
                    Cosa produce
                </div>
                <p style="color:{C_DARK}; font-size:14px; line-height:1.65; margin:0;">
                    I risultati vengono presentati attraverso due misure complementari:
                    il <strong>conteggio dei problemi rilevati</strong> (metodo nativo
                    del Toolkit IMAGES) e il <strong>punteggio ponderato</strong> con
                    moltiplicatore intersezionale, che tiene conto del dominio applicativo
                    e della diffusione del bias attraverso i livelli del sistema.<br><br>
                    La <strong>copertura dell'audit</strong> indica quante domande sono
                    state valutate: un rischio basso su un audit incompleto è meno
                    affidabile di uno su un audit completo.
                </p>
            </div>
        """, unsafe_allow_html=True)

    # Nota d'uso generale
    st.markdown(f"""
        <div style="background:#fff8e1; border:1px solid #ffe082; border-radius:10px;
                    padding:16px 22px; margin:8px 0 12px;">
            <span style="font-size:13px; color:#5d4037; line-height:1.65;">
                <strong>Nota d'uso.</strong> Questo strumento è progettato per
                supportare processi di miglioramento, non per emettere giudizi.
                I risultati dipendono dalla completezza e dall'onestà delle risposte
                fornite. Nessun punteggio costituisce una certificazione di conformità
                né un obbligo legale. Lo strumento è parte di una ricerca accademica
                in corso: i parametri saranno oggetto di validazione empirica progressiva.
            </span>
        </div>
    """, unsafe_allow_html=True)

    # Disclaimer moduli Testi e Immagini
    st.markdown(f"""
        <div style="background:#f0f4ff; border:1px solid #c7d2fe; border-radius:10px;
                    padding:16px 22px; margin:0 0 12px;">
            <span style="font-size:13px; color:#3730a3; line-height:1.65;">
                <strong>Testi e Immagini.</strong> I moduli Testi e Immagini non
                analizzano automaticamente i contenuti: richiedono che tu abbia già
                esaminato il materiale prodotto o utilizzato dal sistema e che tu
                risponda sulla base della tua osservazione diretta.
            </span>
        </div>
    """, unsafe_allow_html=True)

    # Disclaimer contestuale
    st.markdown(f"""
        <div style="background:#f0fdf4; border:1px solid #86efac; border-radius:10px;
                    padding:16px 22px; margin:0 0 24px;">
            <span style="font-size:13px; color:#166534; line-height:1.65;">
                <strong>Interpretazione contestuale.</strong> Alcuni indicatori —
                in particolare nel modulo Immagini — possono essere funzionali al
                dominio applicativo del sistema che stai valutando. La presenza di
                nudità in un sistema di supporto diagnostico medico, ad esempio,
                non è indicativa di oggettificazione. La responsabilità
                dell'interpretazione contestuale di ciascun segnale rimane con
                il valutatore.
            </span>
        </div>
    """, unsafe_allow_html=True)

    col_start, col_empty = st.columns([1, 2])
    with col_start:
        if st.button("Inizia l'audit →", type="primary", use_container_width=True):
            st.session_state["_onboarding_done"] = True
            st.rerun()

    st.stop()

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
st.markdown(f"<h1 style='color:{C_PRIMARY};'>IMAGES NAVIGATOR</h1>",
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
        st.caption("Rispondi Sì se l'aspetto è stato verificato e gestito, No se è stato verificato e risulta problematico, N.A. se non è ancora stato esaminato o non è applicabile.")
        for item in AUDIT_ITEMS["PREP"]:
            render_audit_item(item)

    with tabs[1]:
        st.subheader("DATI")
        st.caption(f"Peso degli indicatori per questo dominio: {w_dati}")
        for item in AUDIT_ITEMS["DATI"]:
            render_audit_item(item, weight_override=w_dati)

    with tabs[2]:
        st.subheader("TEAM")
        st.caption(f"Peso degli indicatori per questo dominio: {w_team}")
        for item in AUDIT_ITEMS["TEAM"]:
            render_audit_item(item, weight_override=w_team)

    with tabs[3]:
        st.subheader("MODELLO")
        st.caption(f"Peso degli indicatori per questo dominio: {w_mod}")
        for item in AUDIT_ITEMS["MODELLO"]:
            render_audit_item(item, weight_override=w_mod)

    with tabs[4]:
        st.subheader("UTENTI")
        st.caption(f"Peso degli indicatori per questo dominio: {w_ut}")
        for item in AUDIT_ITEMS["UTENTI"]:
            render_audit_item(item, weight_override=w_ut)

    with tabs[5]:
        st.subheader("CONTESTO (+1)")
        st.caption(
            "Questo livello valuta il quadro normativo, culturale e istituzionale "
            "in cui il sistema opera. Nel modello Four Levels (+1) il contesto non è "
            "sfondo ma parte attiva del rischio — anche un sistema ben progettato può "
            "produrre danni in un ambiente privo di governance adeguata. "
            "I pesi elevati di questo livello riflettono questa centralità teorica."
        )
        for item in AUDIT_ITEMS["CONTESTO"]:
            render_audit_item(item)

    with tabs[6]:
        st.subheader("ANALISI DEI TESTI")
        st.caption("La presenza di anche un solo elemento determina un rischio bias.")
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**Stereotipi di genere**")
            t1  = st.checkbox("Uso di 'uomo/uomini' come sinonimo universale di umanità",             key="t_g1")
            t2  = st.checkbox("Participio declinato al maschile in presenza di maggioranza femminile", key="t_g2")
            st.markdown("<div style='font-size:12px;color:#a5a5a5;font-style:italic;margin:-8px 0 8px 24px;line-height:1.4;'>Es. \"Gli studenti iscritti al corso sono stati ammessi alla sessione\" scritto al maschile anche quando la maggioranza è femminile.</div>", unsafe_allow_html=True)
            t3  = st.checkbox("Uso asimmetrico di appellativi (es. 'Signora' vs titolo professionale)", key="t_g3")
            t4  = st.checkbox("Titoli professionali declinati al maschile o con suffisso 'donna'",      key="t_g4")
            t5  = st.checkbox("Uso di aggettivi legati a fragilità emotiva o diminutivi",               key="t_g5")
            st.markdown("<div style='font-size:12px;color:#a5a5a5;font-style:italic;margin:-8px 0 8px 24px;line-height:1.4;'>Es. aggettivi come \"delicata\", \"emotiva\", \"irrazionale\", \"isterica\" riferiti a donne; diminutivi come \"dottoressa\" usato in modo sminuente rispetto a \"dottore\".</div>", unsafe_allow_html=True)
            t6  = st.checkbox("Identificazione relazionale della donna (es. 'la moglie di')",           key="t_g6")
            t7  = st.checkbox("Uso di termini d'odio, misogini o metafore animali denigratorie",        key="t_g7")
            st.markdown("<div style='font-size:12px;color:#a5a5a5;font-style:italic;margin:-8px 0 8px 24px;line-height:1.4;'>Es. termini come \"strega\", \"oca\"; espressioni che associano donne ad animali in chiave denigratoria; linguaggio che normalizza violenza o sottomissione.</div>", unsafe_allow_html=True)

        with c2:
            st.markdown("**Stereotipi etnici**")
            t8  = st.checkbox("Uso di stereotipi comparativi basati sull'etnia",          key="t_e1")
            st.markdown("<div style='font-size:12px;color:#a5a5a5;font-style:italic;margin:-8px 0 8px 24px;line-height:1.4;'>Es. \"fumare come un turco\", \"essere preciso come uno svizzero\" — costrutti che attribuiscono qualità o difetti a un'intera etnia.</div>", unsafe_allow_html=True)
            t9  = st.checkbox("Antonomasia stereotipata basata sull'etnia",                key="t_e2")
            st.markdown("<div style='font-size:12px;color:#a5a5a5;font-style:italic;margin:-8px 0 8px 24px;line-height:1.4;'>Es. usare il nome di un gruppo etnico come sinonimo di un comportamento o difetto, come se l'appartenenza al gruppo spiegasse o giustificasse la caratteristica attribuita.</div>", unsafe_allow_html=True)
            t10 = st.checkbox("Uso di generalizzazioni o termini razzisti/obsoleti",       key="t_e3")
            st.markdown("<div style='font-size:12px;color:#a5a5a5;font-style:italic;margin:-8px 0 8px 24px;line-height:1.4;'>Es. termini storicamente usati in senso dispregiativo verso specifici gruppi etnici, o affermazioni generalizzanti come \"tutti gli immigrati sono...\"</div>", unsafe_allow_html=True)
            t11 = st.checkbox("Deumanizzazione tramite tratti o metafore animali",         key="t_e4")
            st.markdown("<div style='font-size:12px;color:#a5a5a5;font-style:italic;margin:-8px 0 8px 24px;line-height:1.4;'>Es. paragoni o metafore che associano gruppi etnici a caratteristiche animali negative come brutalità, sporcizia o mancanza di civiltà.</div>", unsafe_allow_html=True)
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
            st.markdown(
                f"**INDICE RISCHIO ETNICO: {score_e} / 4.0 ({label_e})**  \n"
                f"<span style='font-size:12px; color:#a5a5a5;'>"
                f"Soglie: ≤1 Basso · 2 Medio · ≥3 Alto</span>",
                unsafe_allow_html=True
            )

        st.session_state.max_score_img = max(score_f, score_mf, score_e)
        st.session_state.img_labels    = (label_f, label_mf, label_e)

# ═══════════════════════════════════════════════════════════
# CALCOLO — indipendente dal tab attivo
# ═══════════════════════════════════════════════════════════
punteggio_base, dim_rilevate, liv_rilevati, dettagli_audit = calcola_punteggio(pesi_dinamici)

dimensioni_attive = set(dimensioni_dichiarate) | dim_rilevate
n_dim     = len(dimensioni_attive)
n_livelli = len(liv_rilevati)

moltiplicatore   = get_intersectional_multiplier(n_dim, n_livelli, dominio_scelto)
punteggio_finale = round(punteggio_base * moltiplicatore, 2)
soglia           = DOMINI[dominio_scelto]["threshold"]

n_critici           = sum(
    1 for items in AUDIT_ITEMS.values()
    for item in items
    if st.session_state.get(item["key"], "NV") == "NO"
)
n_verificati        = sum(
    1 for items in AUDIT_ITEMS.values()
    for item in items
    if st.session_state.get(item["key"], "NV") in ("SI", "NO")
)
critici_per_livello = conta_critici_per_livello()
ver_cov, tot_cov, pct_cov_sc = calcola_copertura()

# ═══════════════════════════════════════════════════════════
# COLONNA RISULTATI — SCORECARD
# ═══════════════════════════════════════════════════════════
with col_risultati:

    audit_avviato = n_verificati > 0 or st.session_state.get("punti_testo", 0) > 0

    if not audit_avviato:
        st.markdown(f"""
            <div style='background:white; border:1px dashed {C_MEDIUM};
                        border-radius:16px; padding:40px 24px;
                        text-align:center; margin-top:15px;'>
                <div style='font-size:32px; margin-bottom:12px;'>🛡️</div>
                <p style='color:{C_MEDIUM}; font-size:14px; margin:0;
                          text-transform:uppercase; letter-spacing:1px;'>
                    Inizia a rispondere alle domande<br>per visualizzare i risultati
                </p>
            </div>
        """, unsafe_allow_html=True)

    else:
        # ── Copertura — mostrata sempre, sopra le misure di rischio ──
        n_non_ver = tot_cov - ver_cov
        if pct_cov_sc == 100:
            cov_bg, cov_fg = "#d4edda", "#155724"
            cov_msg = "✅ Tutti gli item verificati — valutazione completa"
        elif pct_cov_sc >= 50:
            cov_bg, cov_fg = "#fff3cd", "#856404"
            cov_msg = f"⚠️ {n_non_ver} item non ancora verificati — il rischio potrebbe essere sottostimato"
        else:
            cov_bg, cov_fg = "#f8f9fa", "#6c757d"
            cov_msg = f"ℹ️ {n_non_ver} item non ancora verificati — continua l'audit per una valutazione affidabile"

        st.markdown(f"""
            <div style="background:{cov_bg}; border-radius:12px;
                        padding:14px 18px; margin-bottom:12px;">
                <div style="font-size:10px; font-weight:700; text-transform:uppercase;
                            letter-spacing:1.5px; color:{cov_fg}; margin-bottom:4px;">
                    COPERTURA AUDIT
                </div>
                <div style="font-size:20px; font-weight:700; color:{cov_fg};">
                    {pct_cov_sc}% — {ver_cov}/{tot_cov} item
                </div>
                <div style="font-size:12px; color:{cov_fg}; margin-top:4px; line-height:1.4;">
                    {cov_msg}
                </div>
            </div>
        """, unsafe_allow_html=True)

        # ── Calcola i due esiti ──
        lbl_cnt, bg_cnt, fg_cnt = esito_conteggio(n_critici)
        lbl_pts, bg_pts, fg_pts = esito_punteggio(punteggio_finale, soglia)

        # ── MISURA 1: Conteggio IMAGES — primaria ──
        st.markdown(f"""
            <div class="result-card" style="border-top: 6px solid {C_PRIMARY};">
                <div class="measure-label">① METODO IMAGES — CONTEGGIO PROBLEMI RILEVATI</div>
                <div class="measure-value" style="background:{bg_cnt}; color:{fg_cnt};">
                    {lbl_cnt}
                </div>
            </div>
        """, unsafe_allow_html=True)

        with st.expander("Dettaglio per livello"):
            for gruppo, n in critici_per_livello.items():
                _, bg, fg = esito_conteggio(n)
                n_ver_gr = sum(
                    1 for item in AUDIT_ITEMS[gruppo]
                    if st.session_state.get(item["key"], "NV") in ("SI", "NO")
                )
                n_tot_gr = len(AUDIT_ITEMS[gruppo])
                st.markdown(f"""
                    <div style="display:flex; justify-content:space-between; align-items:center;
                                padding:6px 0; border-bottom:1px solid #eee; font-size:13px;">
                        <span style="color:{C_DARK}; font-weight:600;">
                            {gruppo}
                            <span style="font-weight:400; color:{C_MEDIUM};
                                         font-size:11px;"> ({n_ver_gr}/{n_tot_gr} verificati)</span>
                        </span>
                        <span style="background:{bg}; color:{fg}; padding:2px 10px;
                                     border-radius:6px; font-weight:700; font-size:12px;">
                            {n} problemi
                        </span>
                    </div>
                """, unsafe_allow_html=True)

        # ── MISURA 2: Punteggio pesato ──
        st.markdown(f"""
            <div class="result-card" style="border-top: 6px solid {C_MEDIUM};">
                <div class="measure-label">② PUNTEGGIO PONDERATO (× MOLTIPLICATORE INTERSEZIONALE)</div>
                <div class="measure-value" style="background:{bg_pts}; color:{fg_pts};">
                    {lbl_pts}
                </div>
            </div>
        """, unsafe_allow_html=True)

        if moltiplicatore > 1.0:
            dim_labels = ", ".join(
                d.replace("_", " ").title() for d in sorted(dimensioni_attive)
            )
            liv_labels = ", ".join(l.title() for l in sorted(liv_rilevati))
            st.markdown(f"""
                <div style="background:#fdf0f5; border:1px solid {C_PRIMARY};
                            border-radius:8px; padding:10px 14px;
                            margin-top:-6px; margin-bottom:10px;
                            font-size:12px; color:{C_DARK};">
                    <strong style="color:{C_PRIMARY};">
                        ⚠️ Effetto intersezionale attivo ×{moltiplicatore}
                    </strong><br>
                    Dimensioni: {dim_labels or '—'} &nbsp;|&nbsp; Livelli implicati: {liv_labels or '—'}
                </div>
            """, unsafe_allow_html=True)

        # ── Stato output Testi e Immagini ──
        testo_status = (
            "🔴 Rischio rilevato"
            if st.session_state.get("punti_testo", 0) > 0
            else "🟢 Nessun rischio"
        )
        img_labels = st.session_state.get("img_labels", ("BASSO", "BASSO", "BASSO"))
        if "ALTO" in img_labels:
            img_status = "🔴 Rischio alto"
        elif "MEDIO" in img_labels:
            img_status = "🟡 Rischio medio"
        else:
            img_status = "🟢 Rischio basso"

        st.markdown(f"""
            <div class="result-card">
                <div class="measure-label">STATO DEGLI OUTPUT</div>
                <p style="margin:6px 0; color:{C_DARK}; font-size:14px;">
                    <strong>Testi:</strong> {testo_status}
                </p>
                <p style="margin:6px 0; color:{C_DARK}; font-size:14px;">
                    <strong>Immagini:</strong> {img_status}
                </p>
            </div>
        """, unsafe_allow_html=True)

        st.write("")

        # ── Report scaricabile ──
        report_data  = f"AUDIT IMAGES NAVIGATOR — {dominio_scelto}\n"
        report_data += f"DATA: {datetime.now().strftime('%d/%m/%Y %H:%M')}\n"
        report_data += "=" * 50 + "\n"
        report_data += f"COPERTURA AUDIT: {pct_cov_sc}% ({ver_cov}/{tot_cov} item verificati)\n"
        report_data += "=" * 50 + "\n"
        report_data += "METODO IMAGES (CONTEGGIO PROBLEMI RILEVATI):\n"
        report_data += f"  Totale: {n_critici} — {lbl_cnt}\n"
        report_data += "  Dettaglio per livello:\n"
        for gruppo, n in critici_per_livello.items():
            n_ver_r = sum(1 for item in AUDIT_ITEMS[gruppo]
                         if st.session_state.get(item["key"], "NV") in ("SI", "NO"))
            report_data += f"    {gruppo}: {n} problemi ({n_ver_r}/{len(AUDIT_ITEMS[gruppo])} verificati)\n"
        report_data += "-" * 50 + "\n"
        report_data += "PUNTEGGIO PESATO:\n"
        report_data += f"  Base: {punteggio_base:.2f} | Moltiplicatore: ×{moltiplicatore}\n"
        report_data += f"  Finale: {punteggio_finale:.2f} (soglia dominio: {soglia})\n"
        report_data += f"  Esito: {lbl_pts}\n"
        if moltiplicatore > 1.0:
            report_data += f"  Dimensioni: {', '.join(sorted(dimensioni_attive))}\n"
            report_data += f"  Livelli implicati: {', '.join(sorted(liv_rilevati))}\n"
        report_data += "-" * 50 + "\n"
        report_data += f"TESTI: {testo_status}\n"
        report_data += (
            f"IMMAGINI: {img_status} "
            f"(F: {img_labels[0]}, M/F: {img_labels[1]}, ETNIA: {img_labels[2]})\n"
        )
        report_data += "=" * 50 + "\n"
        report_data += "DETTAGLIO PROBLEMI RILEVATI E NOTE:\n"
        report_data += (
            "\n".join(dettagli_audit)
            if dettagli_audit
            else "Nessun problema rilevato o nessuna nota registrata."
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
