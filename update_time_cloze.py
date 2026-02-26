"""
update_time_cloze.py
-----------------------
Updates the 6 time cloze cards in Frases [dev]
to remove explanatory text.
"""

import sys
sys.stdout.reconfigure(encoding='utf-8')
from anki_client import find_notes, get_notes_info, invoke

def log(msg): print(msg)

def simplify_cloze():
    ids = find_notes('deck:"Frases [dev]" tag:campanar')
    notes = get_notes_info(ids)
    
    updated = 0
    for n in notes:
        text = n['fields']['Text']['value']
        # Extract the time from <b>...</b>
        import re
        time_match = re.search(r'<b>(.*?)</b>', text)
        if not time_match:
            continue
        time_str = time_match.group(1)
        
        # Determine the new text based on the time
        new_text = ""
        if time_str == "09:15":
            new_text = f"<b>{time_str}</b><br><br>És {{{{c1::un quart de deu}}}}"
        elif time_str == "09:30":
            new_text = f"<b>{time_str}</b><br><br>Són {{{{c1::dos quarts de deu}}}}"
        elif time_str == "09:45":
            new_text = f"<b>{time_str}</b><br><br>Són {{{{c1::tres quarts de deu}}}}"
        elif time_str == "16:55":
            new_text = f"<b>{time_str}</b><br><br>Falten {{{{c1::cinc minuts per a les cinc}}}}"
        elif time_str == "10:27":
            new_text = f"<b>{time_str}</b><br><br>Falten {{{{c1::tres minuts per a dos quarts d'onze}}}}"
        elif time_str == "12:00":
            new_text = f"<b>{time_str}</b><br><br>Són les {{{{c1::dotze en punt}}}}"
            
        if new_text:
            try:
                invoke('updateNoteFields', note={
                    'id': n['noteId'],
                    'fields': {
                        'Text': new_text,
                        'Back Extra': '' # also clear the back extra per user request "no need to explain"
                    }
                })
                updated += 1
                log(f"Updated {time_str}")
            except Exception as e:
                log(f"Error updating {time_str}: {e}")

    log(f"✅ Simplified {updated} time cloze cards")

if __name__ == "__main__":
    log("=== Simplifying Cloze Cards ===")
    simplify_cloze()
    log("Done!")
