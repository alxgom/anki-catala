"""
upgrade_cards.py
----------------
Applies 4 quick-win upgrades to all Anki decks:

1. Add pronunciation + verb CSS to the Basic card template
2. Restyle all verb cards with proper HTML tables
3. Standardize tags to hierarchical format
4. Switch vocab cards to "Basic (optional reversed card)"

Run with Anki open. Don't close the black window (~2-3 min).
"""

import sys
sys.stdout.reconfigure(encoding='utf-8')

from anki_client import find_notes, get_notes_info, invoke
from card_helpers import verb_table

LOG = []
def log(msg): LOG.append(msg); print(msg)


# =========================================================================
# 1. ADD CSS TO CARD TEMPLATES
# =========================================================================
CUSTOM_CSS = """
/* Pronunciation markers */
.vn { color: #e67e22; text-decoration: underline; font-weight: bold; }
.sl { color: #999; text-decoration: line-through; }

/* Verb conjugation table */
.verb-card { text-align: center; }
.verb-inf { font-size: 1.4em; font-weight: bold; margin-bottom: 2px; }
.verb-tense { font-size: 0.85em; color: #888; margin-bottom: 10px; }
.verb-table { margin: 0 auto; border-collapse: collapse; font-size: 1.05em; }
.verb-table td { padding: 3px 12px; }
.verb-table .pronoun { text-align: right; color: #888; font-size: 0.9em; }
.verb-table .form { text-align: left; font-weight: bold; }
"""

def upgrade_css():
    log("\n-- 1. Upgrade CSS --")
    for model in ["Basic", "Basic (optional reversed card)", "Basic (and reversed card)", "Cloze"]:
        try:
            current = invoke("modelStyling", modelName=model)
            css = current.get("css", "")
            if ".vn" in css:
                log(f"  [{model}] CSS already applied, skipping")
                continue
            new_css = css.rstrip() + "\n" + CUSTOM_CSS
            invoke("updateModelStyling", model={"name": model, "css": new_css})
            log(f"  [{model}] CSS updated")
        except Exception as e:
            log(f"  [{model}] Error: {e}")


# =========================================================================
# 2. RESTYLE VERB CARDS
# =========================================================================
VERB_DATA = {
    "Ser":      ("ser",      ["soc","ets","és","som","sou","són"]),
    "Estar":    ("estar",    ["estic","estàs","està","estem","esteu","estan"]),
    "Tenir":    ("tenir",    ["tinc","tens","té","tenim","teniu","tenen"]),
    "Fer":      ("fer",      ["faig","fas","fa","fem","feu","fan"]),
    "Anar":     ("anar",     ["vaig","vas","va","anem","aneu","van"]),
    "Querer":   ("voler",    ["vull","vols","vol","volem","voleu","volen"]),
    "Poder":    ("poder",    ["puc","pots","pot","podem","podeu","poden"]),
    "Saber":    ("saber",    ["sé","saps","sap","sabem","sabeu","saben"]),
    "Venir":    ("venir",    ["vinc","véns","ve","venim","veniu","vénen"]),
    "Vivir":    ("viure",    ["visc","vius","viu","vivim","viviu","viuen"]),
    "Creer":    ("creure",   ["crec","creus","creu","creiem","creieu","creuen"]),
    "Elegir":   ("escollir", ["escullo","escolles","escull","escollim","escolliu","escullen"]),
    "Escribir": ("escriure", ["escric","escrius","escriu","escrivim","escriviu","escriuen"]),
    "Decir":    ("dir",      ["dic","dius","diu","diem","dieu","diuen"]),
    "Llevar":   ("dur",      ["duc","dus","du","duem","dueu","duen"]),
    "Correr":   ("córrer",   ["corro","corres","corre","correm","correu","corren"]),
    "Beber":    ("beure",    ["bec","beus","beu","bevem","beveu","beuen"]),
    "Leer":     ("llegir",   ["llegeixo","llegeixes","llegeix","llegim","llegiu","llegeixen"]),
    "Dormir":   ("dormir",   ["dormo","dorms","dorm","dormim","dormiu","dormen"]),
}

def restyle_verbs():
    log("\n-- 2. Restyle verb cards --")
    idx_verbs = {n["fields"]["Front"]["value"].strip(): n
                 for n in get_notes_info(find_notes('deck:"Verbs Essencials"')) if n}

    for front, (cat_inf, forms) in VERB_DATA.items():
        note = idx_verbs.get(front)
        if not note:
            log(f"  [{front}] not found, skipping")
            continue
        new_back = verb_table(cat_inf, forms)
        invoke("updateNoteFields", note={"id": note["noteId"], "fields": {"Back": new_back}})
        log(f"  [{front}] restyled")


# =========================================================================
# 3. TAG CLEANUP (hierarchical standardization)
# =========================================================================
TAG_RENAMES = {
    # food subcategories
    "comidas": "alimentació::comidas",
    "fruits secs": "alimentació::fruits_secs",
    "fruits": "alimentació::fruits_secs",
    "secs": None,  # remove stray "secs" tag
    # clothing
    "complements": "roba::complements",
    # body
    "cos": "cos",
    # professions
    "restauració": "profesiones::restauració",
    # time
    "expressions": "expressions",
    # furniture
    "mobles": "casa::mobles",
    # economy
    "economia": "economia",
    # animals
    "animales": "animals",
    # misc
    "vocabulari": "vocabulari",
    "objectes": "vocabulari::objectes",
    "natura": "vocabulari::natura",
}

def cleanup_tags():
    log("\n-- 3. Tag cleanup --")
    all_decks = ["cpnl basic 1 [dev]", "cpnl bàsic 2 [dev]", "Verbs Essencials"]
    renamed = 0

    for deck in all_decks:
        ids = find_notes(f'deck:"{deck}"')
        notes = get_notes_info(ids)
        for n in notes:
            if not n:
                continue
            old_tags = n.get("tags", [])
            new_tags = []
            changed = False
            for t in old_tags:
                if t in TAG_RENAMES:
                    new_t = TAG_RENAMES[t]
                    if new_t is None:
                        changed = True  # just remove it
                        continue
                    if new_t != t:
                        changed = True
                    new_tags.append(new_t)
                else:
                    new_tags.append(t)

            if changed:
                # Remove all old tags, add new ones
                old_str = " ".join(old_tags)
                if old_str:
                    invoke("removeTags", notes=[n["noteId"]], tags=old_str)
                if new_tags:
                    invoke("addTags", notes=[n["noteId"]], tags=" ".join(new_tags))
                renamed += 1

    log(f"  Renamed tags on {renamed} cards")


# =========================================================================
# 4. SWITCH TO OPTIONAL REVERSE CARDS
# =========================================================================
def enable_reverse():
    log("\n-- 4. Enable optional reverse cards --")
    TARGET_MODEL = "Basic (optional reversed card)"

    # Get field info for target model
    target_fields = invoke("modelFieldNames", modelName=TARGET_MODEL)
    log(f"  Target model fields: {target_fields}")

    for deck in ["cpnl basic 1 [dev]", "cpnl bàsic 2 [dev]"]:
        ids = find_notes(f'deck:"{deck}"')
        notes = get_notes_info(ids)
        switched = 0
        for n in notes:
            if not n:
                continue
            if n["modelName"] == "Basic":
                try:
                    invoke("changeModel", notes={
                        "notes": [{"id": n["noteId"],
                                   "modelName": TARGET_MODEL,
                                   "fields": {"Front": n["fields"]["Front"]["value"],
                                              "Back": n["fields"]["Back"]["value"],
                                              "Add Reverse": ""},
                                   "tags": " ".join(n.get("tags", []))}]
                    })
                    switched += 1
                except Exception as e:
                    log(f"  Error on [{n['fields']['Front']['value'][:30]}]: {e}")
        log(f"  [{deck}] Switched {switched} cards to optional reverse")


# =========================================================================
# MAIN
# =========================================================================
if __name__ == "__main__":
    log("=== Upgrading Anki cards ===")

    upgrade_css()
    restyle_verbs()
    cleanup_tags()
    enable_reverse()

    with open("upgrade_log.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(LOG))

    log(f"\n=== Done! Log saved to upgrade_log.txt ===")
