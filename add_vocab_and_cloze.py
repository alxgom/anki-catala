"""
add_vocab_and_cloze.py
-----------------------
Adds:
1. "Más / menos" to cpnl bàsic 2 [dev]
2. 6 Cloze cards for "sistema del campanar" (telling time) to a new 'Frases' or existing deck.
Let's put the Cloze cards in a new deck called "Frases [dev]" to keep things clean, as per brainstorming.
"""

import sys
sys.stdout.reconfigure(encoding='utf-8')
from anki_client import invoke

def log(msg): print(msg)

# 1. Add "Más / menos" to Basic 2
def add_mas_menos():
    note = {
        'deckName': 'cpnl bàsic 2 [dev]',
        'modelName': 'Basic (optional reversed card)',
        'fields': {
            'Front': 'Más / menos',
            'Back': 'Més / menys',
            'Add Reverse': 'y'
        },
        'tags': ['quantitats', 'adverbis']
    }
    try:
        invoke('addNote', note=note)
        log("✅ Added 'Más / menos' to cpnl bàsic 2 [dev]")
    except Exception as e:
        log(f"⚠️ Could not add 'Más / menos' (maybe already exists): {e}")

# 2. Add Cloze cards for time
def add_time_cloze():
    deck = "Frases [dev]"
    # Ensure deck exists
    try:
        invoke('createDeck', deck=deck)
    except:
        pass

    cards = [
        # 09:15
        "<b>09:15</b><br>Sistema tradicional: Són les nou i quart<br>Campanar: És {{c1::un quart de deu}}",
        # 09:30
        "<b>09:30</b><br>Sistema tradicional: Són les nou i mitja<br>Campanar: Són {{c1::dos quarts de deu}}",
        # 09:45
        "<b>09:45</b><br>Sistema tradicional: Són les deu menys quart<br>Campanar: Són {{c1::tres quarts de deu}}",
        # 16:55
        "<b>16:55</b><br>Campanar: Falten {{c1::cinc minuts per a les cinc}}",
        # 10:27
        "<b>10:27</b><br>Campanar: Faltent {{c1::tres minuts per a dos quarts d'onze}} (o vint-i-set minuts passats de les deu)",
        # 12:00
        "<b>12:00</b><br>Campanar: Són les {{c1::dotze en punt}}"
    ]
    
    added = 0
    for text in cards:
        note = {
            'deckName': deck,
            'modelName': 'Cloze',
            'fields': {
                'Text': text,
                'Back Extra': 'El sistema del campanar es basa en dir quants quarts han passat de l\'hora <b>següent</b>.'
            },
            'tags': ['temps', 'campanar']
        }
        try:
            invoke('addNote', note=note)
            added += 1
        except Exception as e:
            log(f"Error adding cloze: {e}")
            
    log(f"✅ Added {added} time cloze cards to {deck}")

if __name__ == "__main__":
    log("=== Adding New Cards ===")
    add_mas_menos()
    add_time_cloze()
    log("Done!")
