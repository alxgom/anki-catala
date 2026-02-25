"""
add_content.py
--------------
Adds / updates content across decks using "upsert" logic:
  - If a card with the same Front already exists in the deck → update it
  - If not → create it

Covers:
  1. Run pending update_verb_deck steps (conj tags, voler fix)
  2. New verbs → Verbs Essencials
  3. New vocab → cpnl basic 1 [dev]
  4. New content → cpnl bàsic 2 [dev]  (cloned first if needed)

Run with Anki open.
"""

from anki_client import find_notes, get_notes_info, invoke, add_note

BASIC1 = "cpnl basic 1 [dev]"
BASIC2_SRC = "cpnl bàsic 2"
BASIC2 = "cpnl bàsic 2 [dev]"
VERBS  = "Verbs Essencials"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load_deck_index(deck: str) -> dict:
    """Returns {stripped_front: note} for every note in the deck."""
    note_ids = find_notes(f'deck:"{deck}"')
    notes = get_notes_info(note_ids)
    return {n["fields"]["Front"]["value"].strip(): n for n in notes if n}


def upsert(index: dict, deck: str, front: str, back: str, tags: list, model="Basic"):
    """Insert or update a card. Updates index in-place."""
    existing = index.get(front.strip())
    if existing:
        invoke("updateNoteFields", note={"id": existing["noteId"], "fields": {"Front": front, "Back": back}})
        # Refresh tags
        old_tags = " ".join(existing["tags"])
        if old_tags:
            invoke("removeTags", notes=[existing["noteId"]], tags=old_tags)
        invoke("addTags", notes=[existing["noteId"]], tags=" ".join(tags))
        print(f"  ✏️  Updated : {front}")
    else:
        note_id = add_note(deck, model, {"Front": front, "Back": back}, tags, allow_duplicate=True)
        print(f"  ✅ Added   : {front}")
        # Fake-update the index so we don't double-insert if called again
        index[front.strip()] = {"noteId": note_id, "fields": {"Front": {"value": front}, "Back": {"value": back}}, "tags": tags}


def conj(infinitive, forms):
    jo, tu, ell, nos, vos, ells = forms
    return (
        f"<b>{infinitive}</b><br><br>"
        f"jo &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;→ {jo}<br>"
        f"tu &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;→ {tu}<br>"
        f"ell/a &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;→ {ell}<br>"
        f"nosaltres → {nos}<br>"
        f"vosaltres &nbsp;→ {vos}<br>"
        f"ells/es &nbsp;&nbsp;&nbsp;→ {ells}"
    )

def clone_if_needed(src, dst):
    decks = invoke("deckNames")
    if dst not in decks:
        print(f"  Cloning '{src}' → '{dst}'...")
        invoke("createDeck", deck=dst)
        ids = find_notes(f'deck:"{src}"')
        notes = get_notes_info(ids)
        new_notes = [
            {"deckName": dst, "modelName": n["modelName"],
             "fields": {k: v["value"] for k,v in n["fields"].items()},
             "tags": n["tags"], "options": {"allowDuplicate": True}}
            for n in notes if n
        ]
        invoke("addNotes", notes=new_notes)
        print(f"  Cloned {len(new_notes)} notes.")
    else:
        print(f"  '{dst}' already exists, skipping clone.")


# ---------------------------------------------------------------------------
# 1. Pending verb deck fixes (voler label + conj tags)
# ---------------------------------------------------------------------------
VERB_META = {
    "Ser":                   ("Ser",    ["present","verbes","verbes::essencials","conj::irregular"]),
    "Estar":                 ("Estar",  ["present","verbes","verbes::essencials","conj::irregular","conj::-ar"]),
    "Tenir":                 ("Tenir",  ["present","verbes","verbes::essencials","conj::irregular","conj::-er"]),
    "Fer":                   ("Fer",    ["present","verbes","verbes::essencials","conj::irregular","conj::-er"]),
    "Ir / Anar":             ("Anar",   ["present","verbes","verbes::essencials","conj::irregular","conj::-ar"]),
    "Querer / Poder querer": ("Querer", ["present","verbes","verbes::essencials","conj::irregular","conj::-er"]),
    "Poder":                 ("Poder",  ["present","verbes","verbes::essencials","conj::irregular","conj::-er"]),
    "Saber":                 ("Saber",  ["present","verbes","verbes::essencials","conj::irregular","conj::-er"]),
    "Venir":                 ("Venir",  ["present","verbes","verbes::essencials","conj::irregular","conj::-ir"]),
    "Vivir":                 ("Vivir",  ["present","verbes","verbes::essencials","conj::irregular","conj::-ure"]),
}
VERB_BACKS = {
    "Ser":    conj("ser",    ["soc","ets","és","som","sou","són"]),
    "Estar":  conj("estar",  ["estic","estàs","està","estem","esteu","estan"]),
    "Tenir":  conj("tenir",  ["tinc","tens","té","tenim","teniu","tenen"]),
    "Fer":    conj("fer",    ["faig","fas","fa","fem","feu","fan"]),
    "Anar":   conj("anar",   ["vaig","vas","va","anem","aneu","van"]),
    "Querer": conj("voler",  ["vull","vols","vol","volem","voleu","volen"]),
    "Poder":  conj("poder",  ["puc","pots","pot","podem","podeu","poden"]),
    "Saber":  conj("saber",  ["sé","saps","sap","sabem","sabeu","saben"]),
    "Venir":  conj("venir",  ["vinc","véns","vé","venim","veniu","vénen"]),
    "Vivir":  conj("viure",  ["visc","vius","viu","vivim","viviu","viuen"]),
}

def fix_verb_deck():
    print(f"\n── 1. Fix Verbs Essencials labels & tags ──")
    idx = load_deck_index(VERBS)
    for old_front, (new_front, tags) in VERB_META.items():
        note = idx.get(old_front) or idx.get(new_front)
        if not note:
            print(f"  ⚠️  Not found: {old_front}")
            continue
        back = VERB_BACKS.get(new_front, note["fields"]["Back"]["value"])
        invoke("updateNoteFields", note={"id": note["noteId"], "fields": {"Front": new_front, "Back": back}})
        old_tags_str = " ".join(note["tags"])
        if old_tags_str: invoke("removeTags", notes=[note["noteId"]], tags=old_tags_str)
        invoke("addTags", notes=[note["noteId"]], tags=" ".join(tags))
        print(f"  ✏️  {old_front} → {new_front}")


# ---------------------------------------------------------------------------
# 2. New verbs → Verbs Essencials
# ---------------------------------------------------------------------------
NEW_VERBS = [
    ("Creer",   conj("creure",  ["crec","creus","creu","creiem","creieu","creuen"]),
     ["present","verbes","verbes::essencials","conj::irregular","conj::-ure"]),
    ("Elegir",  conj("escollir",["escullo","escolles","escull","escolim","escoliu","escullen"]),
     ["present","verbes","verbes::essencials","conj::irregular","conj::-ir"]),
    ("Escribir",conj("escriure",["escric","escrius","escriu","escrivim","escriviu","escriuen"]),
     ["present","verbes","verbes::essencials","conj::irregular","conj::-ure"]),
    ("Decir",   conj("dir",     ["dic","dius","diu","diem","dieu","diuen"]),
     ["present","verbes","verbes::essencials","conj::irregular"]),
    ("Llevar",  conj("dur",     ["duc","dus","du","duem","dueu","duen"]),
     ["present","verbes","verbes::essencials","conj::irregular","conj::-er"]),
    ("Correr",  conj("correr",  ["corro","corres","corre","correm","correu","corren"]),
     ["present","verbes","verbes::essencials","conj::-er"]),
    ("Beber",   conj("beure",   ["bec","beus","beu","bevem","beveu","beuen"]),
     ["present","verbes","verbes::essencials","conj::irregular","conj::-ure"]),
    ("Leer",    conj("llegir",  ["llegeixo","llegeixes","llegeix","llegim","llegiu","llegeixen"]),
     ["present","verbes","verbes::essencials","conj::irregular","conj::-ir"]),
    ("Dormir",  conj("dormir",  ["dormo","dorms","dorm","dormim","dormiu","dormen"]),
     ["present","verbes","verbes::essencials","conj::-ir"]),
]

def add_new_verbs():
    print(f"\n── 2. New verbs → {VERBS} ──")
    idx = load_deck_index(VERBS)
    for front, back, tags in NEW_VERBS:
        upsert(idx, VERBS, front, back, tags)


# ---------------------------------------------------------------------------
# 3. New vocabulary → cpnl basic 1 [dev]
# ---------------------------------------------------------------------------
NEW_BASIC1 = [
    # Nouns / misc
    ("Tijeras de tijera",     "Les estovalles (mantel)<br>⚠️ plural: les estovalles",
     ["casa"]),
    ("Por favor",             "Si us plau<br><i>(col·loquial: sisplau)</i>",
     ["expressions"]),
    ("Silla",                 "La cadira / les cadires",
     ["casa","mobles"]),
    ("Toalla / servilleta",   "La tovalla (toalla)<br>El tovalló (servilleta)",
     ["casa"]),

    # Foods
    ("Albóndigas",            "Les mandonguilles",                ["alimentació","comidas"]),
    ("Dorada (pescado)",      "L'orada",                          ["alimentació"]),
    ("Miel",                  "La mel",                           ["alimentació"]),

    # Nuts
    ("Frutos secos",
     "<b>Els fruits secs</b><br><br>La nou (nuez)<br>L'avellana (avellana)<br>L'ametlla (almendra)<br>El pistatxo (pistacho)<br>El cacauet (cacahuete)",
     ["alimentació","fruits secs"]),

    # Body parts (chunk card)
    ("Partes del cuerpo",
     "<b>El cos</b><br><br>"
     "El cap (cabeza)<br>L'orella (oreja)<br>El coll (cuello)<br>"
     "Les mans (manos)<br>Els peus (pies)<br>Les cames (piernas)<br>"
     "La panxa (barriga)<br>L'esquena (espalda)<br>El nas (nariz)<br>"
     "La boca (boca)<br>Els ulls (ojos)",
     ["cos"]),

    # Complements / accessories (chunk card)
    ("Complementos / accesorios",
     "<b>Complements</b><br><br>"
     "El collaret (collar)<br>L'anell (anillo)<br>El braçalet (pulsera)<br>"
     "Les arracades (pendientes)<br>Les orelleres (orejeras)<br>"
     "El gorro / la gorra (gorro/gorra)<br>La bufanda (bufanda)<br>"
     "Els guants (guantes)<br>El casc (casco/helmet)<br>"
     "Les botes (botas)<br>Els mitjons (calcetines)<br>"
     "Les sandàlies (sandalias)<br>Les xancletes (chanclas)",
     ["roba","complements"]),

    # Ordinals
    ("Números ordinales",
     "<b>Ordinals</b> — masc. / fem.<br><br>"
     "1r primer / 1a primera<br>"
     "2n segon / 2a segona<br>"
     "3r tercer / 3a tercera<br>"
     "4t quart / 4a quarta<br>"
     "5è cinquè / 5a cinquena<br>"
     "6è sisè / 6a sisena<br>"
     "7è setè / 7a setena<br>"
     "8è vuitè / 8a vuitena<br>"
     "9è novè / 9a novena<br>"
     "10è desè / 10a desena",
     ["numeros"]),
]

def add_basic1_vocab():
    print(f"\n── 3. New vocab → {BASIC1} ──")
    idx = load_deck_index(BASIC1)
    for front, back, tags in NEW_BASIC1:
        upsert(idx, BASIC1, front, back, tags)


# ---------------------------------------------------------------------------
# 4. New content → cpnl bàsic 2 [dev]
# ---------------------------------------------------------------------------
NEW_BASIC2 = [
    # Pronoun 'en' with apostrophe examples
    ("El pronom 'en'",
     "<b>En / n'</b> — substitueix un complement amb 'de' o quantitat<br><br>"
     "<b>Davant vocal → n' (apostrofat)</b><br><br>"
     "• Tinc tres llibres → <b>En</b> tinc tres<br>"
     "• Vols pa? → Sí, <b>en</b> vull<br>"
     "• Parla del treball → <b>En</b> parla molt<br>"
     "• Hi ha molts errors → <b>N'</b>hi ha molts<br>"
     "• He comprat ous → <b>N'</b>he comprat sis",
     ["pronoms","pronoms::en"]),

    # Food-related jobs (chunk card)
    ("Trabajos en hostelería",
     "<b>Feines de restauració</b><br><br>"
     "El cambrer / la cambrera (camarero/a)<br>"
     "El caixer / la caixera (cajero/a)<br>"
     "L'ajudant de cuina (ayudante de cocina)<br>"
     "L'encarregat·da de sala (encargado/a de sala)<br>"
     "El personal de neteja (personal de limpieza)<br>"
     "L'escombriaire (basurero/a)",
     ["profesiones","restauració"]),

    # New individual words
    ("Cuenta / cuentas",      "El compte / els comptes",          ["economia"]),
    ("Parece / parece que",
     "Sembla / sembla que...<br><br><i>Sembla que plourà</i> (Parece que lloverá)",
     ["expressions"]),
    ("Entonces / en aquel momento",
     "Aleshores<br><br><i>Aleshores, va decidir marxar</i><br>(Entonces, decidió marcharse)",
     ["expressions","temps"]),
    ("Cualquier / cualquiera",
     "Qualsevol<br><br><i>Qualsevol dia és bo per aprendre</i><br>(Cualquier día es bueno para aprender)",
     ["expressions"]),
    ("Pues / entonces",
     "Doncs<br><br><i>Doncs, ens quedem aquí</i><br>(Pues, nos quedamos aquí)",
     ["expressions"]),
    ("Nunca / jamás",         "Mai<br><br><i>Mai he estat a Londres</i> (Nunca he estado en Londres)",
     ["expressions","temps"]),
    ("Garaje",                "El garatge",                       ["casa","llocs"]),
]

def add_basic2_content():
    print(f"\n── 4. New content → {BASIC2} ──")
    clone_if_needed(BASIC2_SRC, BASIC2)
    idx = load_deck_index(BASIC2)
    for front, back, tags in NEW_BASIC2:
        upsert(idx, BASIC2, front, back, tags)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    fix_verb_deck()
    add_new_verbs()
    add_basic1_vocab()
    add_basic2_content()
    print("\n🎉 All content added/updated!")
