"""Switch Basic cards to 'Basic (optional reversed card)' note type."""
import sys
sys.stdout.reconfigure(encoding='utf-8')
from anki_client import find_notes, get_notes_info, invoke

TARGET = "Basic (optional reversed card)"

for deck in ["cpnl basic 1 [dev]", "cpnl bàsic 2 [dev]"]:
    ids = find_notes(f'deck:"{deck}"')
    notes = get_notes_info(ids)
    switched = 0
    for n in notes:
        if not n: continue
        if n["modelName"] == "Basic":
            try:
                invoke("updateNoteModel", note={
                    "id": n["noteId"],
                    "modelName": TARGET,
                    "fields": {
                        "Front": n["fields"]["Front"]["value"],
                        "Back": n["fields"]["Back"]["value"],
                        "Add Reverse": ""
                    }
                })
                switched += 1
            except Exception as e:
                front = n["fields"]["Front"]["value"][:30]
                print(f"  Error [{front}]: {e}")
    print(f"[{deck}] Switched {switched} cards")

print("Done!")
