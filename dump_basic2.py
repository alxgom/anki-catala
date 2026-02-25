"""
dump_basic2.py - Dump all notes from cpnl bàsic 2 to JSON
"""
import json
from anki_client import find_notes, get_notes_info

note_ids = find_notes('deck:"cpnl bàsic 2"')
notes = get_notes_info(note_ids)

with open('basic2_dump.json', 'w', encoding='utf-8') as f:
    json.dump(notes, f, ensure_ascii=False, indent=2)

print(f"Dumped {len(notes)} notes from cpnl bàsic 2")
