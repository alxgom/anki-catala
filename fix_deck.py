"""
fix_deck.py
-----------
Fixes all identified errors in the dev deck: 'cpnl basic 1 [dev]'
  1. Critical translation errors (wrong language, inverted cards, untranslated)
  2. Typos / spelling errors
  3. Tag inconsistencies
  4. Trailing/leading whitespace

Run ONLY against the [dev] deck, never the original.
"""

import json
from anki_client import find_notes, get_notes_info, invoke

DEV_DECK = "cpnl basic 1 [dev]"

# ---------------------------------------------------------------------------
# Fix map: key = exact current Front value (stripped), value = corrected fields
# Format: { "front_value": {"Back": "corrected_back"} }
# Use "Front" key too if the front itself needs fixing (inverted card)
# ---------------------------------------------------------------------------

FIELD_FIXES = {
    # --- Critical errors: wrong language / not translated ---
    "La mesa":      {"Back": "La taula"},
    "Julio":        {"Back": "Juliol"},
    "La noche":     {"Back": "La nit"},
    "Silencio ":    {"Back": "Silenci"},   # note: has trailing space on front
    "Silencio":     {"Back": "Silenci"},
    "Probar":       {"Back": "Provar"},
    "Dificil":      {"Back": "Difícil"},
    "Demandar":     {"Back": "Demanar"},
    "Dar":          {"Back": "Donar"},

    # Inverted card: Front is Catalan, Back is Spanish — swap them
    "Bruixa":       {"Front": "Bruja", "Back": "Bruixa"},

    # --- Typos / spelling errors ---
    "Enero":        {"Back": "Gener"},
    "Febrero":      {"Back": "Febrer"},
    "Noviembre":    {"Back": "Novembre"},
    "Seguido":      {"Back": "Sovint"},
    "Semana":       {"Back": "Setmana"},
    "Rojo":         {"Back": "Vermell"},
    "Hijo/hija":    {"Back": "Fill/filla"},
    "Hermano/hermana": {"Back": "Germà/germana"},
    "Libro":        {"Back": "Llibre"},
    "Apellido":     {"Back": "Cognom"},   # Cognome → Cognom
    "Amar":         {"Back": "Estimar"},  # "Amar" existed as Catalan too but Estimar is correct
}

# ---------------------------------------------------------------------------
# Tag fixes: rename tags across the whole deck
# { "old_tag": "new_tag" } — use None to remove a tag
# ---------------------------------------------------------------------------

TAG_RENAMES = {
    "la::casa":   "casa",
    "robas":      "roba",
    "comidas":    "alimentació",
    "adjetuis":   "adjectius",
}

# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def update_note_fields(note_id: int, fields: dict):
    """Update one or more fields of a note by ID."""
    invoke("updateNoteFields", note={"id": note_id, "fields": fields})


def add_tags_to_notes(note_ids: list, tags: str):
    invoke("addTags", notes=note_ids, tags=tags)


def remove_tags_from_notes(note_ids: list, tags: str):
    invoke("removeTags", notes=note_ids, tags=tags)


def strip_html(text: str) -> str:
    """Very basic HTML strip for comparison purposes only."""
    import re
    return re.sub(r"<[^>]+>", "", text).strip()


# ---------------------------------------------------------------------------
# Phase 1: Fix field values
# ---------------------------------------------------------------------------

def fix_fields(notes: list) -> int:
    fixes_applied = 0
    for note in notes:
        if not note:
            continue

        front_raw = note["fields"]["Front"]["value"]
        front_text = front_raw.strip()  # stripped for matching

        if front_text in FIELD_FIXES:
            corrections = FIELD_FIXES[front_text]
            fields_to_update = {}

            for field_name, new_value in corrections.items():
                current = note["fields"][field_name]["value"].strip()
                if current != new_value:
                    fields_to_update[field_name] = new_value

            if fields_to_update:
                update_note_fields(note["noteId"], fields_to_update)
                print(f"  ✏️  Fixed [{front_text}]: {fields_to_update}")
                fixes_applied += 1

    return fixes_applied


# ---------------------------------------------------------------------------
# Phase 2: Fix tags
# ---------------------------------------------------------------------------

def fix_tags(notes: list) -> int:
    fixes_applied = 0
    for note in notes:
        if not note:
            continue

        current_tags = note["tags"]
        needs_update = False

        for old_tag, new_tag in TAG_RENAMES.items():
            if old_tag in current_tags:
                remove_tags_from_notes([note["noteId"]], old_tag)
                if new_tag:
                    add_tags_to_notes([note["noteId"]], new_tag)
                    print(f"  🏷️  [{note['fields']['Front']['value'].strip()}]: '{old_tag}' → '{new_tag}'")
                else:
                    print(f"  🏷️  [{note['fields']['Front']['value'].strip()}]: removed '{old_tag}'")
                needs_update = True

        if needs_update:
            fixes_applied += 1

    return fixes_applied


# ---------------------------------------------------------------------------
# Phase 3: Strip whitespace from all fields
# ---------------------------------------------------------------------------

def fix_whitespace(notes: list) -> int:
    fixes_applied = 0
    for note in notes:
        if not note:
            continue

        fields_to_update = {}
        for field_name, field_info in note["fields"].items():
            val = field_info["value"]
            stripped = val.strip()
            if stripped != val:
                fields_to_update[field_name] = stripped

        if fields_to_update:
            update_note_fields(note["noteId"], fields_to_update)
            front = note["fields"]["Front"]["value"].strip()
            print(f"  🧹 Stripped whitespace [{front}]: {list(fields_to_update.keys())}")
            fixes_applied += 1

    return fixes_applied


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print(f"\n🔧 Running fixes on deck: '{DEV_DECK}'\n")

    note_ids = find_notes(f'deck:"{DEV_DECK}"')
    print(f"Found {len(note_ids)} notes.\n")

    notes = get_notes_info(note_ids)

    print("─── Phase 1: Fix translation errors & typos ───")
    n1 = fix_fields(notes)
    print(f"→ {n1} note(s) fixed.\n")

    print("─── Phase 2: Fix tags ───")
    n2 = fix_tags(notes)
    print(f"→ {n2} note(s) re-tagged.\n")

    print("─── Phase 3: Strip whitespace ───")
    n3 = fix_whitespace(notes)
    print(f"→ {n3} note(s) cleaned.\n")

    print(f"✅ Done! Total changes: {n1 + n2 + n3} note(s) updated.")
    print(f"\n👉 Open Anki and check '{DEV_DECK}' to verify.")


if __name__ == "__main__":
    main()
