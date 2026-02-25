"""
dump_deck.py - Dump all notes from a deck to JSON for analysis
"""
import json
from anki_client import find_notes, get_notes_info

DECK = "cpnl basic 1"

note_ids = find_notes('deck:"cpnl basic 1"')
notes = get_notes_info(note_ids)

with open('deck_dump.json', 'w', encoding='utf-8') as f:
    json.dump(notes, f, ensure_ascii=False, indent=2)

print(f"Dumped {len(notes)} notes to deck_dump.json")
