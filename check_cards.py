import sys
sys.stdout.reconfigure(encoding='utf-8')
from anki_client import find_notes, get_notes_info

with open("basic2_check.txt", "w", encoding="utf-8") as f:
    f.write("=== cpnl bàsic 2 [dev] ===\n")
    ids = find_notes('deck:"cpnl bàsic 2 [dev]"')
    notes = get_notes_info(ids)
    for n in notes:
        f.write(f"{n['fields']['Front']['value']} --> {n['fields']['Back']['value']} | Tags: {n.get('tags', [])}\n")

    f.write("\n=== cpnl basic 1 [dev] - fruits secs ===\n")
    ids = find_notes('deck:"cpnl basic 1 [dev]" "Frutos secos"')
    notes = get_notes_info(ids)
    for n in notes:
        f.write(f"{n['fields']['Front']['value']} --> {n['fields']['Back']['value']} | Tags: {n.get('tags', [])}\n")
