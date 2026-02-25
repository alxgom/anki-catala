"""
enrich_forms.py
---------------
Enriches color and adjective cards in the dev deck with all gendered forms:
  masculine / feminine / masculine plural / feminine plural

Format used in Back field:
  vermell / vermella / vermells / vermelles

Only applies to cards in the dev deck. Run after fix_deck.py.
"""

from anki_client import find_notes, get_notes_info, invoke

DEV_DECK = "cpnl basic 1 [dev]"

# ---------------------------------------------------------------------------
# Enrichment map: key = Front (stripped), value = full Back with all forms
# Format guide: masc / fem / masc.pl / fem.pl
# Notes:
#   - Invariable words (gris, rosa, taronja): masc = fem, add just plural
#   - Nouns with natural gender: show el/la forms
# ---------------------------------------------------------------------------

ENRICHED_BACKS = {
    # --- Colors (individual cards) ---
    "Rojo":      "Vermell / vermella / vermells / vermelles",
    "Verde":     "Verd / verda / verds / verdes",
    "Amarillo":  "Groc / groga / grocs / grogues",
    "Azul":      "Blau / blava / blaus / blaves",
    "Negro":     "Negre / negra / negres / negres",  # negres for both plurals
    "Blanco":    "Blanc / blanca / blancs / blanques",
    "Naranja":   "Taronja (invariable) / taronges (pl.)",
    "Rosa":      "Rosa (invariable) / roses (pl.)",
    "Gris":      "Gris / grisa / grisos / grises",
    "Morado":    "Morat / morada / morats / morades",

    # --- Adjectives (individual cards) ---
    "Corto":     "Curt / curta / curts / curtes",
    "Largo":     "Llarg / llarga / llargs / llargues",
    "Caliente":  "Calent / calenta / calents / calentes",
    "Frio":      "Fred / freda / freds / fredes",
    "Caluroso":  "Càlid / càlida / càlids / càlides",
    "Fresco":    "Fresc / fresca / frescos / fresques",
    "Dulce":     "Dolç / dolça / dolços / dolces",
    "Salado":    "Salat / salada / salats / salades",
    "Seco":      "Sec / seca / secs / seques",
    "Duro":      "Dur / dura / durs / dures",
    "Caro":      "Car / cara / cars / cares",
    "Dificil":   "Difícil / difícil / difícils / difícils",  # invariable masc/fem
    "Lleno/pleno": "Ple / plena / plens / plenes",
    "Vacio":     "Buit / buida / buits / buides",
    "Mismo":     "Mateix / mateixa / mateixos / mateixes",
    "Verdaderas": "Veritable / veritable / veritables / veritables",
    "Falsas":    "Fals / falsa / falsos / falses",

    # --- Numbers with gendered form ---
    "Segundo":   "Segon / segona / segons / segones",

    # --- Relaciones (gendered nouns) ---
    "Amigo":     "Amic / amiga / amics / amigues",
    "Vecinos":   "Veí / veïna / veïns / veïnes",
    "Medico":    "Metge / metgessa (doctor/a)",
    "Cocinero":  "Cuiner / cuinera / cuiners / cuineres",
}


def update_note_fields(note_id: int, fields: dict):
    invoke("updateNoteFields", note={"id": note_id, "fields": fields})


def enrich_forms():
    print(f"\n✨ Enriching forms in '{DEV_DECK}'...\n")

    note_ids = find_notes(f'deck:"{DEV_DECK}"')
    notes = get_notes_info(note_ids)

    enriched = 0
    for note in notes:
        if not note:
            continue

        front = note["fields"]["Front"]["value"].strip()

        if front in ENRICHED_BACKS:
            new_back = ENRICHED_BACKS[front]
            current_back = note["fields"]["Back"]["value"].strip()

            if current_back != new_back:
                update_note_fields(note["noteId"], {"Back": new_back})
                print(f"  ✨ [{front}]")
                print(f"     was: {current_back}")
                print(f"     now: {new_back}\n")
                enriched += 1

    print(f"✅ Enriched {enriched} card(s).")


if __name__ == "__main__":
    enrich_forms()
