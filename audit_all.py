"""
audit_all.py - Dump all cards from all 3 decks into a single file for review.
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')
import json
from anki_client import find_notes, get_notes_info

DECKS = [
    "cpnl basic 1 [dev]",
    "cpnl bàsic 2 [dev]",
    "Verbs Essencials",
]

with open("audit_all.txt", "w", encoding="utf-8") as f:
    for deck in DECKS:
        ids = find_notes(f'deck:"{deck}"')
        notes = get_notes_info(ids)
        f.write(f"\n{'='*60}\n")
        f.write(f"  {deck}  ({len(notes)} cards)\n")
        f.write(f"{'='*60}\n\n")
        for i, n in enumerate(notes, 1):
            front = n["fields"]["Front"]["value"].strip()
            back = n["fields"]["Back"]["value"].strip()
            tags = n.get("tags", [])
            f.write(f"[{i}] Front: {front}\n")
            f.write(f"    Back:  {back}\n")
            f.write(f"    Tags:  {tags}\n\n")

print("Audit written to audit_all.txt")
