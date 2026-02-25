"""
clone_deck.py
-------------
Clones all notes from a source deck into a new target deck via AnkiConnect.
Requires Anki to be running with AnkiConnect installed.
"""

from anki_client import invoke, find_notes, get_notes_info, add_notes

SOURCE_DECK = "cpnl basic 1"
TARGET_DECK = "cpnl basic 1 [dev]"


def create_deck(deck_name: str):
    """Create a deck if it doesn't already exist."""
    return invoke("createDeck", deck=deck_name)


def clone_deck(source: str, target: str):
    print(f"📋 Cloning '{source}' → '{target}'...")

    # 1. Create the target deck
    create_deck(target)
    print(f"✅ Target deck '{target}' created (or already exists).")

    # 2. Find all notes in source deck
    note_ids = find_notes(f'deck:"{source}"')
    print(f"🔍 Found {len(note_ids)} note(s) in '{source}'.")

    if not note_ids:
        print("⚠️  No notes found. Nothing to clone.")
        return

    # 3. Get full note info
    notes_info = get_notes_info(note_ids)

    # 4. Build new note payloads for the target deck
    new_notes = []
    skipped = 0
    for note in notes_info:
        if not note:
            skipped += 1
            continue
        fields = {name: info["value"] for name, info in note["fields"].items()}
        new_notes.append({
            "deckName": target,
            "modelName": note["modelName"],
            "fields": fields,
            "tags": note["tags"],
        })

    if skipped:
        print(f"⚠️  Skipped {skipped} empty/invalid note(s).")

    # 5. Add notes in batch
    results = add_notes(new_notes, allow_duplicates=True)

    success = sum(1 for r in results if r is not None)
    duplicates = sum(1 for r in results if r is None)

    print(f"\n✅ Done!")
    print(f"   Added:      {success} note(s)")
    print(f"   Duplicates: {duplicates} note(s) skipped (already exist)")
    print(f"\n👉 Open Anki to see your new deck: '{target}'")


if __name__ == "__main__":
    clone_deck(SOURCE_DECK, TARGET_DECK)
