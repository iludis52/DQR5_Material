"""
LangGraph-Implementierungen der FLACI-Automaten
================================================

DEA-Automaten (1–3): Kein Ausgabealphabet, nur Domänenzustand.
Moore-Automat (4):   Ausgabe hängt nur vom Zustand ab → MOORE_OUTPUTS dict.
Mealy-Automaten (5–6): Ausgabe hängt von Zustand UND Eingabe ab → MEALY_TRANSITIONS table.

Simulationshinweis: input_sequence und position sind Infrastruktur,
um den Automaten mit einer Eingabeliste zu füttern. In der Produktion
kämen Eingaben von Sensoren, APIs oder Nutzereingaben.
"""

from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, END
import operator


# ============================================================================
# 1. DREHKREUZ (DEA)
# ============================================================================

class DrehkreuzState(TypedDict):
    current_state: str
    input_sequence: list[str]
    position: int
    gesperrt: bool


def drehkreuz_zu(state: DrehkreuzState) -> dict:
    pos = state["position"]
    eingabe = state["input_sequence"][pos]

    result = {"position": pos + 1}

    if eingabe == "bezahlen":
        result["current_state"] = "Offen"
        result["gesperrt"] = False

    return result


def drehkreuz_offen(state: DrehkreuzState) -> dict:
    pos = state["position"]
    eingabe = state["input_sequence"][pos]

    result = {"position": pos + 1}

    if eingabe == "durchgehen":
        result["current_state"] = "Zu"
        result["gesperrt"] = True

    return result


def drehkreuz_router(state: DrehkreuzState) -> str:
    if state["position"] >= len(state["input_sequence"]):
        return END
    return state["current_state"]


def build_drehkreuz():
    graph = StateGraph(DrehkreuzState)
    graph.add_node("Zu", drehkreuz_zu)
    graph.add_node("Offen", drehkreuz_offen)
    graph.set_entry_point("Zu")
    graph.add_conditional_edges("Zu", drehkreuz_router, {"Zu": "Zu", "Offen": "Offen", END: END})
    graph.add_conditional_edges("Offen", drehkreuz_router, {"Zu": "Zu", "Offen": "Offen", END: END})
    return graph.compile()


# ============================================================================
# 2. MIKROWELLE (DEA)
# ============================================================================

class MikrowelleState(TypedDict):
    current_state: str
    input_sequence: list[str]
    position: int
    tuer_offen: bool
    heizung_aktiv: bool
    fertig: bool


def mikrowelle_offen(state: MikrowelleState) -> dict:
    pos = state["position"]
    eingabe = state["input_sequence"][pos]

    result = {"position": pos + 1}

    if eingabe == "schliessen":
        result["current_state"] = "Zu"
        result["tuer_offen"] = False

    return result


def mikrowelle_zu(state: MikrowelleState) -> dict:
    pos = state["position"]
    eingabe = state["input_sequence"][pos]

    result = {"position": pos + 1}

    if eingabe == "öffnen":
        result["current_state"] = "Offen"
        result["tuer_offen"] = True
    elif eingabe == "starten":
        result["current_state"] = "Läuft"
        result["heizung_aktiv"] = True

    return result


def mikrowelle_laeuft(state: MikrowelleState) -> dict:
    pos = state["position"]
    eingabe = state["input_sequence"][pos]

    result = {"position": pos + 1}

    if eingabe == "warten":
        result["current_state"] = "OK"
        result["heizung_aktiv"] = False
        result["fertig"] = True
    elif eingabe == "öffnen":
        result["current_state"] = "Offen"
        result["heizung_aktiv"] = False
        result["tuer_offen"] = True

    return result


def mikrowelle_ok(state: MikrowelleState) -> dict:
    pos = state["position"]
    eingabe = state["input_sequence"][pos]

    result = {"position": pos + 1}

    if eingabe == "öffnen":
        result["current_state"] = "Offen"
        result["tuer_offen"] = True
        result["fertig"] = False

    return result


def mikrowelle_router(state: MikrowelleState) -> str:
    if state["position"] >= len(state["input_sequence"]):
        return END
    return state["current_state"]


def build_mikrowelle():
    graph = StateGraph(MikrowelleState)
    graph.add_node("Offen", mikrowelle_offen)
    graph.add_node("Zu", mikrowelle_zu)
    graph.add_node("Läuft", mikrowelle_laeuft)
    graph.add_node("OK", mikrowelle_ok)
    graph.set_entry_point("Offen")
    for node in ["Offen", "Zu", "Läuft", "OK"]:
        graph.add_conditional_edges(node, mikrowelle_router,
            {"Offen": "Offen", "Zu": "Zu", "Läuft": "Läuft", "OK": "OK", END: END})
    return graph.compile()


# ============================================================================
# 3. ONLINESHOP (DEA)
# ============================================================================

class OnlineshopState(TypedDict):
    current_state: str
    input_sequence: list[str]
    position: int
    zahlung_gebucht: bool
    fehler: str | None


def shop_node(state: OnlineshopState) -> dict:
    pos = state["position"]
    eingabe = state["input_sequence"][pos]

    result = {"position": pos + 1}

    if eingabe == "checkout":
        result["current_state"] = "Kasse"
    elif eingabe == "error":
        result["current_state"] = "Trap"
        result["fehler"] = "Verbindungsfehler"

    return result


def kasse_node(state: OnlineshopState) -> dict:
    pos = state["position"]
    eingabe = state["input_sequence"][pos]

    result = {"position": pos + 1}

    if eingabe == "pay":
        result["current_state"] = "Deal"
        result["zahlung_gebucht"] = True
    elif eingabe == "error":
        result["current_state"] = "Trap"
        result["fehler"] = "Zahlungsfehler"
    elif eingabe == "back":
        result["current_state"] = "Shop"

    return result


def onlineshop_router(state: OnlineshopState) -> str:
    if state["current_state"] in ("Deal", "Trap"):
        return END
    if state["position"] >= len(state["input_sequence"]):
        return END
    return state["current_state"]

def onlineshop_router(state: OnlineshopState) -> str:
    if state["current_state"] in ("Deal", "Trap"):
        return END
    if state["position"] >= len(state["input_sequence"]):
        return END
    return state["current_state"]


def build_onlineshop():
    graph = StateGraph(OnlineshopState)
    graph.add_node("Shop", shop_node)
    graph.add_node("Kasse", kasse_node)
    graph.set_entry_point("Shop")

    graph.add_conditional_edges(
        "Shop", onlineshop_router,{"Shop": "Shop", "Kasse": "Kasse", END: END}
    )

    graph.add_conditional_edges(
        "Kasse", onlineshop_router,{"Shop": "Shop", "Kasse": "Kasse", END: END}
    )
    return graph.compile()


# ============================================================================
# 4. GETRÄNKEAUTOMAT (MOORE)
# ============================================================================
# Moore-Eigenschaft: Die Ausgabe hängt NUR vom Zustand ab.
# Das MOORE_OUTPUTS-Dict macht diese Eigenschaft strukturell sichtbar:
#   Zustand → Ausgabe (unabhängig von der Eingabe)
#
# Implementierungshinweis: Da LangGraph den Zielknoten nicht garantiert
# ausführt, setzen wir die Ausgabe als Transition-Action. Das MOORE_OUTPUTS-
# Dict stellt sicher, dass wir trotzdem immer die zum Zielzustand gehörige
# Ausgabe verwenden — die Moore-Eigenschaft bleibt erhalten.

class GetraenkeMooreState(TypedDict):
    current_state: str
    input_sequence: list[str]
    position: int
    guthaben_cent: int
    display: str
    outputs: Annotated[list[str], operator.add]


# Moore-Ausgabefunktion: Zustand → Ausgabe
MOORE_OUTPUTS = {
    "hat0€": '"2€"',
    "hat1€": '"1€"',
    "OK":    "Limo",
    "back":  "-1€",
}


def moore_hat0(state: GetraenkeMooreState) -> dict:
    pos = state["position"]
    eingabe = state["input_sequence"][pos]

    result = {"position": pos + 1}

    if eingabe == "1€ einwerfen":
        ziel = "hat1€"
        result["current_state"] = ziel
        result["guthaben_cent"] = 100
        result["display"] = MOORE_OUTPUTS[ziel]         # Ausgabe bestimmt durch Zielzustand
        result["outputs"] = [MOORE_OUTPUTS[ziel]]

    return result


def moore_hat1(state: GetraenkeMooreState) -> dict:
    pos = state["position"]
    eingabe = state["input_sequence"][pos]

    result = {"position": pos + 1}

    if eingabe == "1€ einwerfen":
        ziel = "OK"
    elif eingabe == "abbrechen":
        ziel = "back"
    else:
        return result

    result["current_state"] = ziel
    result["guthaben_cent"] = 200 if ziel == "OK" else 0
    result["display"] = MOORE_OUTPUTS[ziel]
    result["outputs"] = [MOORE_OUTPUTS[ziel]]

    return result


def moore_ok(state: GetraenkeMooreState) -> dict:
    pos = state["position"]
    eingabe = state["input_sequence"][pos]

    result = {"position": pos + 1}

    if eingabe == "warten":
        ziel = "hat0€"
        result["current_state"] = ziel
        result["guthaben_cent"] = 0
        result["display"] = MOORE_OUTPUTS[ziel]
        result["outputs"] = [MOORE_OUTPUTS[ziel]]

    return result


def moore_back(state: GetraenkeMooreState) -> dict:
    pos = state["position"]
    eingabe = state["input_sequence"][pos]

    result = {"position": pos + 1}

    if eingabe == "warten":
        ziel = "hat0€"
        result["current_state"] = ziel
        result["guthaben_cent"] = 0
        result["display"] = MOORE_OUTPUTS[ziel]
        result["outputs"] = [MOORE_OUTPUTS[ziel]]

    return result


def moore_router(state: GetraenkeMooreState) -> str:
    if state["position"] >= len(state["input_sequence"]):
        return END
    return state["current_state"]


def build_getraenkeautomat_moore():
    graph = StateGraph(GetraenkeMooreState)
    graph.add_node("hat0€", moore_hat0)
    graph.add_node("hat1€", moore_hat1)
    graph.add_node("OK", moore_ok)
    graph.add_node("back", moore_back)
    graph.set_entry_point("hat0€")
    for node in ["hat0€", "hat1€", "OK", "back"]:
        graph.add_conditional_edges(node, moore_router,
            {"hat0€": "hat0€", "hat1€": "hat1€", "OK": "OK", "back": "back", END: END})
    return graph.compile()


# ============================================================================
# 5. MEALY-GETRÄNKEAUTOMAT
# ============================================================================
# Mealy-Eigenschaft: Die Ausgabe hängt von Zustand UND Eingabe ab.
# Die MEALY_TRANSITIONS-Tabelle macht diese Eigenschaft strukturell sichtbar:
#   (Zustand, Eingabe) → (Zielzustand, Ausgabe)

class GetraenkeMealyState(TypedDict):
    current_state: str
    input_sequence: list[str]
    position: int
    guthaben_cent: int
    outputs: Annotated[list[str], operator.add]


# Mealy-Übergangstabelle: (Zustand, Eingabe) → (Zielzustand, Ausgabe)
MEALY_TRANSITIONS = {
    ("hat0€", "1€ einwerfen"): ("hat1€", "'piep'",  100),
    ("hat0€", "abbrechen"):    ("hat0€", "'piep'",    0),
    ("hat1€", "1€ einwerfen"): ("hat0€", "Limo",      0),
    ("hat1€", "abbrechen"):    ("hat0€", "-1€",       0),
}


def mealy_hat0(state: GetraenkeMealyState) -> dict:
    pos = state["position"]
    eingabe = state["input_sequence"][pos]
    ziel, ausgabe, guthaben = MEALY_TRANSITIONS[("hat0€", eingabe)]

    return {
        "current_state": ziel,
        "guthaben_cent": guthaben,
        "outputs": [ausgabe],
        "position": pos + 1,
    }


def mealy_hat1(state: GetraenkeMealyState) -> dict:
    pos = state["position"]
    eingabe = state["input_sequence"][pos]
    ziel, ausgabe, guthaben = MEALY_TRANSITIONS[("hat1€", eingabe)]

    return {
        "current_state": ziel,
        "guthaben_cent": guthaben,
        "outputs": [ausgabe],
        "position": pos + 1,
    }


def mealy_router(state: GetraenkeMealyState) -> str:
    if state["position"] >= len(state["input_sequence"]):
        return END
    return state["current_state"]


def build_getraenkeautomat_mealy():
    graph = StateGraph(GetraenkeMealyState)
    graph.add_node("hat0€", mealy_hat0)
    graph.add_node("hat1€", mealy_hat1)
    graph.set_entry_point("hat0€")
    for node in ["hat0€", "hat1€"]:
        graph.add_conditional_edges(node, mealy_router,
            {"hat0€": "hat0€", "hat1€": "hat1€", END: END})
    return graph.compile()


# ============================================================================
# 6. MUSTERERKENNUNG 101 (MEALY)
# ============================================================================
# Mealy: (Zustand, Eingabe) → (Zielzustand, Ausgabe)

class MustererkennungState(TypedDict):
    current_state: str
    input_sequence: list[str]
    position: int
    treffer_count: int
    outputs: Annotated[list[str], operator.add]


# Mealy-Übergangstabelle: (Zustand, Eingabe) → (Zielzustand, Ausgabe)
MUSTER_TRANSITIONS = {
    ("q0", "0"): ("q0", "nix"),
    ("q0", "1"): ("q1", "nix"),
    ("q1", "1"): ("q1", "nix"),
    ("q1", "0"): ("q2", "nix"),
    ("q2", "1"): ("q1", "treffer"),
    ("q2", "0"): ("q0", "nix"),
}


def muster_node(state: MustererkennungState) -> dict:
    pos = state["position"]
    eingabe = state["input_sequence"][pos]
    ziel, ausgabe = MUSTER_TRANSITIONS[(state["current_state"], eingabe)]

    result = {
        "current_state": ziel,
        "outputs": [ausgabe],
        "position": pos + 1,
    }

    if ausgabe == "treffer":
        result["treffer_count"] = state["treffer_count"] + 1

    return result


def muster_router(state: MustererkennungState) -> str:
    if state["position"] >= len(state["input_sequence"]):
        return END
    return state["current_state"]


def build_mustererkennung():
    graph = StateGraph(MustererkennungState)
    graph.add_node("q0", muster_node)
    graph.add_node("q1", muster_node)
    graph.add_node("q2", muster_node)
    graph.set_entry_point("q0")
    for node in ["q0", "q1", "q2"]:
        graph.add_conditional_edges(node, muster_router,
            {"q0": "q0", "q1": "q1", "q2": "q2", END: END})
    return graph.compile()


# ============================================================================
# DEMO
# ============================================================================

if __name__ == "__main__":

    print("1. DREHKREUZ (DEA)")
    print("-" * 40)
    r = build_drehkreuz().invoke({
        "current_state": "Zu", "position": 0, "gesperrt": True,
        "input_sequence": ["bezahlen", "durchgehen", "bezahlen", "bezahlen", "durchgehen"],
    })
    print(f"   Zustand: {r['current_state']}, gesperrt: {r['gesperrt']}")

    print("\n2. MIKROWELLE (DEA)")
    print("-" * 40)
    r = build_mikrowelle().invoke({
        "current_state": "Offen", "position": 0,
        "tuer_offen": True, "heizung_aktiv": False, "fertig": False,
        "input_sequence": ["schliessen", "starten", "warten"],
    })
    print(f"   Zustand: {r['current_state']}, fertig: {r['fertig']}")

    print("\n3a. ONLINESHOP (DEA) — Erfolg")
    print("-" * 40)
    r = build_onlineshop().invoke({
        "current_state": "Shop", "position": 0,
        "zahlung_gebucht": False, "fehler": None,
        "input_sequence": ["checkout", "pay"],
    })
    print(f"   Zustand: {r['current_state']}, bezahlt: {r['zahlung_gebucht']}")

    print("\n3b. ONLINESHOP (DEA) — Fehler")
    print("-" * 40)
    r = build_onlineshop().invoke({
        "current_state": "Shop", "position": 0,
        "zahlung_gebucht": False, "fehler": None,
        "input_sequence": ["checkout", "error"],
    })
    print(f"   Zustand: {r['current_state']}, fehler: {r['fehler']}")

    print("\n4. GETRÄNKEAUTOMAT (MOORE)")
    print("-" * 40)
    r = build_getraenkeautomat_moore().invoke({
        "current_state": "hat0€", "position": 0,
        "guthaben_cent": 0, "display": MOORE_OUTPUTS["hat0€"],
        "outputs": [MOORE_OUTPUTS["hat0€"]],
        "input_sequence": ["1€ einwerfen", "1€ einwerfen", "warten"],
    })
    print(f"   Zustand: {r['current_state']}, display: {r['display']}")
    print(f"   Outputs: {r['outputs']}")

    print("\n5. GETRÄNKEAUTOMAT (MEALY)")
    print("-" * 40)
    r = build_getraenkeautomat_mealy().invoke({
        "current_state": "hat0€", "position": 0,
        "guthaben_cent": 0, "outputs": [],
        "input_sequence": ["1€ einwerfen", "1€ einwerfen"],
    })
    print(f"   Zustand: {r['current_state']}, guthaben: {r['guthaben_cent']}ct")
    print(f"   Outputs: {r['outputs']}")

    print("\n6. MUSTERERKENNUNG 101 (MEALY)")
    print("-" * 40)
    r = build_mustererkennung().invoke({
        "current_state": "q0", "position": 0,
        "treffer_count": 0, "outputs": [],
        "input_sequence": list("1011010"),
    })
    print(f"   Eingabe: {''.join(r['input_sequence'])}")
    print(f"   Outputs: {r['outputs']}")
    print(f"   Treffer: {r['treffer_count']}")
    
    
    
######################################

from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class State(TypedDict):
    nachricht: str

def empfangen(state: State) -> dict:
    return {"nachricht": state["nachricht"]}

def verarbeiten(state: State) -> dict:
    return {"nachricht": state["nachricht"].upper()}

def ausgeben(state: State) -> dict:
    return {"nachricht": f"Ergebnis: {state['nachricht']}"}

# --- Graph aufbauen ---
graph = StateGraph(State)

graph.add_node("empfangen", empfangen)       # Knoten
graph.add_node("verarbeiten", verarbeiten)
graph.add_node("ausgeben", ausgeben)

graph.add_edge(START, "empfangen")            # START → erster Knoten
graph.add_edge("empfangen", "verarbeiten")    # Kante
graph.add_edge("verarbeiten", "ausgeben")     # Kante
graph.add_edge("ausgeben", END)               # letzter Knoten → END

app = graph.compile()


########################################

def klassifizieren(state: State) -> dict:
    if "suche" in state["nachricht"].lower():
        return {"route": "recherche"}
    return {"route": "direkt"}

def routing(state: State) -> Literal["recherchieren", "antworten"]:
    """Die Routing-Funktion — die Übergangsfunktion δ."""
    if state["route"] == "recherche":
        return "recherchieren"
    return "antworten"

# --- Graph aufbauen ---
graph = StateGraph(State)
graph.add_node("klassifizieren", klassifizieren)
graph.add_node("recherchieren", recherchieren)
graph.add_node("antworten", antworten)
graph.add_node("ausgeben", ausgeben)

graph.add_edge(START, "klassifizieren")

# Bedingter Übergang
graph.add_conditional_edges(
    "klassifizieren",              # Ausgangsknoten
    routing,                       # Routing-Funktion
    {                              # Mapping
        "recherchieren": "recherchieren",
        "antworten": "antworten"
    }
)

graph.add_edge("recherchieren", "ausgeben")
graph.add_edge("antworten", "ausgeben")
graph.add_edge("ausgeben", END)

#############################################

#State-Schema: Der Bauplan des Rucksacks
from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages

class AgentState(TypedDict):
    """Der Rucksack — alles, was durch den Graphen wandert."""
    nachrichten: Annotated[list, add_messages]   # wird angehängt
    route: str                                    # Routing-Entscheidung
    ergebnis: str                                 # Zwischenergebnis
    fehler_zaehler: int                           # Zähler

#Knotenfunktion: Lesen und Schreiben
def recherchieren(state: AgentState) -> dict:
    """Liest aus dem Rucksack, schreibt zurück."""
    frage = state["nachrichten"][-1]       # Lesen
    ergebnis = suche_im_web(frage)         # Arbeit verrichten
    return {                               # Partielles Update
        "ergebnis": ergebnis,
        "route": "fertig"
    }
    
#Reducer-Muster
# Ohne Reducer: neuer Wert überschreibt alten
ergebnis: str               # "alt" → "neu" (überschrieben)

# Mit Reducer: neuer Wert wird angehängt
nachrichten: Annotated[list, add_messages]  # [msg1] → [msg1, msg2]

############################################

# LangGraph: Agent mit Retry-Zyklus
def pruefen(state: AgentState) -> dict:
    """Prüft das Ergebnis: fertig oder nochmal?"""
    if state["ergebnis_ok"]:
        return {"route": "fertig"}
    if state["fehler_zaehler"] >= 3:
        return {"route": "fertig"}        # Abbruchbedingung!
    return {
        "route": "nochmal",
        "fehler_zaehler": state["fehler_zaehler"] + 1
    }

def nach_pruefung(state) -> Literal["planen", "antworten"]:
    if state["route"] == "nochmal":
        return "planen"       # ← Zyklus: zurück zum Anfang
    return "antworten"        # ← Ausstieg aus dem Zyklus

# --- Graph aufbauen ---
graph = StateGraph(AgentState)
graph.add_node("planen", planen)
graph.add_node("tool_aufrufen", tool_aufrufen)
graph.add_node("pruefen", pruefen)
graph.add_node("antworten", antworten)

graph.add_edge(START, "planen")
graph.add_edge("planen", "tool_aufrufen")
graph.add_edge("tool_aufrufen", "pruefen")

graph.add_conditional_edges(
    "pruefen", nach_pruefung,
    {"planen": "planen", "antworten": "antworten"}
)
graph.add_edge("antworten", END)


#Abbruchbedingungen
# Mechanismus 1: Eigener Zähler im State
if state["fehler_zaehler"] >= 3:
    return {"route": "fertig"}

# Mechanismus 2: LangGraphs Rekursionslimit
app.invoke(state, {"recursion_limit": 10})


##############################################

class State(TypedDict):
    frage: str
    antwort: str
    qualitaet: str

graph = StateGraph(State)
graph.add_node("analysieren", analysieren)
graph.add_node("generieren", generieren)
graph.add_node("bewerten", bewerten)
graph.add_node("verbessern", verbessern)
graph.add_node("ausgeben", ausgeben)

graph.add_edge(START, "analysieren")
graph.add_edge("analysieren", "generieren")
graph.add_edge("generieren", "bewerten")
graph.add_conditional_edges(
    "bewerten", qualitaets_routing,
    {"verbessern": "verbessern", "ausgeben": "ausgeben"}
)
graph.add_edge("verbessern", "generieren")  # ← Zyklus!
graph.add_edge("ausgeben", END)


