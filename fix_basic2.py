"""
fix_basic2.py
-------------
Fixes missing genders/articles and incomplete cards in cpnl bàsic 2 [dev].
"""

import sys
sys.stdout.reconfigure(encoding='utf-8')

from anki_client import find_notes, get_notes_info, invoke

DECK = "cpnl bàsic 2 [dev]"


def load_index(deck):
    ids = find_notes(f'deck:"{deck}"')
    notes = get_notes_info(ids)
    return {n["fields"]["Front"]["value"].strip(): n for n in notes if n}


def update_fields(note_id, fields):
    invoke("updateNoteFields", note={"id": note_id, "fields": fields})


def add_tags(note_ids, tags_str):
    invoke("addTags", notes=note_ids, tags=tags_str)


# Fixes: { front_match_substring: (new_front, new_back, tags_to_add) }
# We match by substring since the old fronts have <br> in them
FIXES = {
    "Frutos secos": {
        "front": "Frutos secos",
        "back": (
            "<b>Els fruits secs</b><br><br>"
            "La nou (nuez)<br>"
            "L'avellana (avellana)<br>"
            "L'ametlla (almendra)<br>"
            "El pistatxo (pistacho)<br>"
            "El cacauet (cacahuete)"
        ),
        "tags": ["alimentació", "fruits_secs"],
    },
    "Mozo/cliente": {
        "front": "Camarero / cliente",
        "back": "El cambrer / la cambrera (camarero/a)<br>El client / la clienta (cliente/a)",
        "tags": ["profesiones", "restauració"],
    },
    "Hambre/sed": {
        "front": "Hambre / sed",
        "back": "La fam (hambre, fem.)<br>La set (sed, fem.)",
        "tags": ["alimentació"],
    },
}


def main():
    print(f"🔧 Fixing '{DECK}'...\n")
    idx = load_index(DECK)

    for match_key, fix in FIXES.items():
        # Find the card (fronts may contain <br> tags)
        note = None
        for front, n in idx.items():
            if match_key in front:
                note = n
                break

        if not note:
            print(f"  ⚠️  Not found: {match_key}")
            continue

        old_front = note["fields"]["Front"]["value"]
        update_fields(note["noteId"], {
            "Front": fix["front"],
            "Back": fix["back"],
        })
        add_tags([note["noteId"]], " ".join(fix["tags"]))
        print(f"  ✏️  Fixed: [{old_front[:50]}] → [{fix['front']}]")

    print(f"\n✅ Done!")


if __name__ == "__main__":
    main()
