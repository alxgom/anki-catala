"""
inspect_deck.py
---------------
Pull and display all notes from a deck for analysis.
"""
import json
from anki_client import find_notes, get_notes_info, get_model_field_names, get_model_names

DECK = "cpnl basic 1"

def inspect(deck=DECK, limit=None):
    print(f"\n=== Inspecting deck: '{deck}' ===\n")

    # Get note types used
    print("📐 Available note types (models):")
    for m in get_model_names():
        fields = get_model_field_names(m)
        print(f"   • {m}: {fields}")

    # Get all note IDs
    note_ids = find_notes(f'deck:"{deck}"')
    print(f"\n📦 Total notes: {len(note_ids)}")

    # Fetch note info
    sample = note_ids[:limit] if limit else note_ids
    notes = get_notes_info(sample)

    # Group by model
    by_model = {}
    for note in notes:
        if not note:
            continue
        model = note["modelName"]
        by_model.setdefault(model, []).append(note)

    print(f"\n📊 Notes by model type:")
    for model, notes_list in by_model.items():
        print(f"   • {model}: {len(notes_list)} note(s)")

    # Print sample cards per model
    print("\n--- SAMPLE CARDS ---")
    for model, notes_list in by_model.items():
        print(f"\n[{model}]")
        for note in notes_list[:10]:  # show first 10 per type
            fields = {k: v["value"] for k, v in note["fields"].items()}
            print(f"  tags: {note['tags']}")
            for fname, fval in fields.items():
                print(f"    {fname}: {repr(fval[:120]) if fval else '(empty)'}")
            print()

if __name__ == "__main__":
    inspect()
