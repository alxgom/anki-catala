"""
update_verb_deck.py
-------------------
1. Fixes voler front: "Querer / Poder querer" → "Querer"
2. Adds tense tag: present
3. Adds conjugation group tags per verb:
   conj::-ar | conj::-er | conj::-ir | conj::-ure | conj::irregular

Then cleans up old verb cards in 'cpnl basic 1 [dev]':
- Replaces messy Back fields with the polished conjugation format
"""

from anki_client import find_notes, get_notes_info, invoke

VERB_DECK = "Verbs Essencials"
DEV_DECK  = "cpnl basic 1 [dev]"

# Per-verb metadata: front → (correct_front, conj_tags)
VERB_META = {
    "Ser":                    ("Ser",    ["present", "conj::irregular"]),
    "Estar":                  ("Estar",  ["present", "conj::irregular", "conj::-ar"]),
    "Tenir":                  ("Tenir",  ["present", "conj::irregular", "conj::-er"]),
    "Fer":                    ("Fer",    ["present", "conj::irregular", "conj::-er"]),
    "Ir / Anar":              ("Anar",   ["present", "conj::irregular", "conj::-ar"]),
    "Querer / Poder querer":  ("Querer", ["present", "conj::irregular", "conj::-er"]),
    "Poder":                  ("Poder",  ["present", "conj::irregular", "conj::-er"]),
    "Saber":                  ("Saber",  ["present", "conj::irregular", "conj::-er"]),
    "Venir":                  ("Venir",  ["present", "conj::irregular", "conj::-ir"]),
    "Vivir":                  ("Vivir",  ["present", "conj::irregular", "conj::-ure"]),
}

# Polished Back fields for the old messy cards in cpnl basic 1 [dev]
# Key = Front as it appears in that deck (Spanish)
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

OLD_VERB_FIXES = {
    "Ser":         conj("ser",    ["soc","ets","és","som","sou","són"]),
    "Estar":       conj("estar",  ["estic","estàs","està","estem","esteu","estan"]),
    "Tenir":       conj("tenir",  ["tinc","tens","té","tenim","teniu","tenen"]),
    "Hacer":       conj("fer",    ["faig","fas","fa","fem","feu","fan"]),
    "Ir":          conj("anar",   ["vaig","vas","va","anem","aneu","van"]),
    "Querer":      conj("voler",  ["vull","vols","vol","volem","voleu","volen"]),
    "Poder":       conj("poder",  ["puc","pots","pot","podem","podeu","poden"]),
    "Saber":       conj("saber",  ["sé","saps","sap","sabem","sabeu","saben"]),
    "Venir":       conj("venir",  ["vinc","véns","vé","venim","veniu","vénen"]),
    "Vivir":       conj("viure",  ["visc","vius","viu","vivim","viviu","viuen"]),
    "Ver ":        conj("veure",  ["veig","veus","veu","veiem","veieu","veuen"]),
    "Ver":         conj("veure",  ["veig","veus","veu","veiem","veieu","veuen"]),
    "Llamarse":    conj("dir-se", ["em dic","et dius","es diu","ens diem","us dieu","es diuen"]),
    "Tener":       conj("tenir",  ["tinc","tens","té","tenim","teniu","tenen"]),
    "Vivir":       conj("viure",  ["visc","vius","viu","vivim","viviu","viuen"]),
}


def update_note_fields(note_id, fields):
    invoke("updateNoteFields", note={"id": note_id, "fields": fields})

def add_tags(note_ids, tags_str):
    invoke("addTags", notes=note_ids, tags=tags_str)

def remove_tags(note_ids, tags_str):
    invoke("removeTags", notes=note_ids, tags=tags_str)


# ---------------------------------------------------------------------------
# Step 1: Update Verbs Essencials deck
# ---------------------------------------------------------------------------
def update_verb_deck():
    print(f"\n🔧 Step 1: Updating '{VERB_DECK}' tags & labels...\n")

    note_ids = find_notes(f'deck:"{VERB_DECK}"')
    notes = get_notes_info(note_ids)

    for note in notes:
        if not note:
            continue
        front = note["fields"]["Front"]["value"].strip()
        if front not in VERB_META:
            print(f"  ⚠️  Unknown card: [{front}] — skipping")
            continue

        correct_front, new_tags = VERB_META[front]
        fields_to_update = {}

        # Fix front label if needed
        if front != correct_front:
            fields_to_update["Front"] = correct_front
            print(f"  ✏️  Front: '{front}' → '{correct_front}'")

        if fields_to_update:
            update_note_fields(note["noteId"], fields_to_update)

        # Remove old generic tags, add specific ones
        remove_tags([note["noteId"]], "verbes verbes::essencials")
        add_tags([note["noteId"]], " ".join(new_tags) + " verbes verbes::essencials")
        print(f"  🏷️  [{correct_front}] → tags: {new_tags}")

    print("\n✅ Verb deck updated.\n")


# ---------------------------------------------------------------------------
# Step 2: Clean old verb cards in cpnl basic 1 [dev]
# ---------------------------------------------------------------------------
def clean_old_verbs():
    print(f"🧹 Step 2: Cleaning old verb cards in '{DEV_DECK}'...\n")

    note_ids = find_notes(f'deck:"{DEV_DECK}" tag:verbes')
    notes = get_notes_info(note_ids)

    cleaned = 0
    for note in notes:
        if not note:
            continue
        front = note["fields"]["Front"]["value"].strip()
        if front in OLD_VERB_FIXES:
            new_back = OLD_VERB_FIXES[front]
            update_note_fields(note["noteId"], {"Back": new_back})
            # Add present tense tag
            add_tags([note["noteId"]], "present")
            print(f"  ✅ Cleaned: [{front}]")
            cleaned += 1

    print(f"\n✅ Cleaned {cleaned} old verb card(s).\n")


if __name__ == "__main__":
    update_verb_deck()
    clean_old_verbs()
    print("🎉 All done!")
