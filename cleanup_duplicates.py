"""
cleanup_duplicates.py
---------------------
Comprehensive cleanup of cpnl basic 1 [dev]:

1. Remove exact duplicate cards (same Front text appearing twice)
   - Keep the FIRST (fixed) copy, delete the second (unfixed clone)
2. Delete old individual day/month/season cards that were consolidated
3. Delete old unfixed pronoun and possessives cards
4. Fix remaining errors (La Nuit, Sensa, Devant, Derrere, etc.)
5. Fix incomplete cards (Quedarse, Bailar, Entrar)
6. Add tags to untagged cards
"""

import sys
sys.stdout.reconfigure(encoding='utf-8')
from anki_client import find_notes, get_notes_info, invoke


DECK = "cpnl basic 1 [dev]"


def update_fields(nid, fields):
    invoke("updateNoteFields", note={"id": nid, "fields": fields})

def delete_notes(nids):
    if nids:
        invoke("deleteNotes", notes=nids)

def add_tags(nids, tags_str):
    if nids:
        invoke("addTags", notes=nids, tags=tags_str)


# ---------------------------------------------------------------------------
# Step 1: Remove exact duplicate cards (keep earliest noteId)
# ---------------------------------------------------------------------------
def remove_duplicates():
    print("\n── 1. Remove duplicate cards ──")
    ids = find_notes(f'deck:"{DECK}"')
    notes = get_notes_info(ids)

    seen = {}  # front_stripped -> first note
    to_delete = []

    for n in notes:
        if not n:
            continue
        front = n["fields"]["Front"]["value"].strip()
        if front in seen:
            to_delete.append(n["noteId"])
        else:
            seen[front] = n

    if to_delete:
        delete_notes(to_delete)
        print(f"  🗑️  Deleted {len(to_delete)} duplicate cards")
    else:
        print("  ℹ️  No duplicates found")


# ---------------------------------------------------------------------------
# Step 2: Delete old individual cards that are now consolidated
# ---------------------------------------------------------------------------
OLD_INDIVIDUAL_FRONTS = [
    # Days (individually)
    "Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado", "Domingo",
    # Months (individually)
    "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
    "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre",
    # Seasons (individually)
    "Verano", "Invierno", "El otoño", "Primavera",
    # Old unfixed pronoun card (replaced by better one)
    "A mí/a ti/ a el/ a nosotros/ a vostre/ a ells",
    # Old possessives card (replaced by expanded one)
    "Mío, tuyo,suyo",
]

def delete_old_individuals():
    print("\n── 2. Delete old unconsolidated cards ──")
    ids = find_notes(f'deck:"{DECK}"')
    notes = get_notes_info(ids)

    to_delete = []
    for n in notes:
        if not n:
            continue
        front = n["fields"]["Front"]["value"].strip()
        if front in OLD_INDIVIDUAL_FRONTS:
            to_delete.append(n["noteId"])
            print(f"  🗑️  [{front}]")

    if to_delete:
        delete_notes(to_delete)
        print(f"  → Deleted {len(to_delete)} old individual cards")
    else:
        print("  ℹ️  No old individual cards found")


# ---------------------------------------------------------------------------
# Step 3: Fix remaining translation/typo errors
# ---------------------------------------------------------------------------
REMAINING_FIXES = {
    "La noche":   {"Back": "La nit"},
    "Despues":    {"Back": "Després"},
    "Sin":        {"Back": "Sense"},           # Sensa → Sense
    "Delante":    {"Back": "Davant"},          # Devant → Davant
    "Detras":     {"Back": "Darrere"},         # Derrere → Darrere
    "Padre/madre": {"Back": "Pare/mare"},      # Pere → Pare
    "Tío/tia":    {"Back": "Oncle/tieta"},     # oncla-tiata → tieta
    "Entrar":     {"Back": "Entrar"},          # Same in Catalan, just needs a tag
    "Bailar":     {"Back": "Ballar"},          # Remove trailing <br>
    "Quedarse":   {"Back": "Quedar-se<br><br>Em quedo<br>Et quedes<br>Es queda<br>Ens quedem<br>Us quedeu<br>Es queden"},
    "Recibidor":  {"Back": "El rebedor"},      # Missing article
    "Cocina":     {"Back": "La cuina"},        # Missing article
    "Puerta":     {"Back": "La porta"},        # Missing article
    "Ropa":       {"Back": "La roba"},         # Missing article
    "Presupuesto": {"Back": "El pressupost"},  # Presupost → pressupost, missing article
    "Profesion":  {"Back": "La professió"},    # Missing article
    "Fiesta":     {"Back": "La festa"},        # Missing article
    "Luna":       {"Back": "La lluna"},        # Missing article
    "Escoba":     {"Back": "L'escombra"},      # Missing article
    "Fiebre":     {"Back": "La febre"},        # Missing article
    "Libro":      {"Back": "El llibre"},       # Missing article
    "Esquina":    {"Back": "La cantonada"},    # Missing article
    "Ruido":      {"Back": "El soroll"},       # Missing article
    "Silencio":   {"Back": "El silenci"},      # Missing article
    "Alquiler":   {"Back": "El lloguer"},      # Lloger → lloguer, missing article
    "Siesta":     {"Back": "La migdiada"},     # Missing article
    "Baja":       {"Back": "Baixa / baix (adj. m/f)"},
    "Negocio":    {"Back": "La botiga"},       # Missing article
    "Ensalada":   {"Back": "L'amanida"},       # Missing article
    "Pez":        {"Back": "El peix"},         # Missing article
    "Perro":      {"Back": "El gos / la gossa"},
    "Apellido":   {"Back": "El cognom"},       # Missing article
    "Edad":       {"Back": "L'edat (fem.)"},   # Missing article
    "Hoy":        {"Back": "Avui"},            # Avuí → Avui
}

def fix_remaining():
    print("\n── 3. Fix remaining errors ──")
    ids = find_notes(f'deck:"{DECK}"')
    notes = get_notes_info(ids)

    fixed = 0
    for n in notes:
        if not n:
            continue
        front = n["fields"]["Front"]["value"].strip()
        if front in REMAINING_FIXES:
            update_fields(n["noteId"], REMAINING_FIXES[front])
            print(f"  ✏️  Fixed: [{front}]")
            fixed += 1

    print(f"  → Fixed {fixed} cards")


# ---------------------------------------------------------------------------
# Step 4: Add missing tags to untagged cards
# ---------------------------------------------------------------------------
TAG_MAP = {
    "Salir":      "verbes",
    "Entrar":     "verbes",
    "Bailar":     "verbes",
    "Mismo":      "adjectius",
    "Verdaderas": "adjectius",
    "Falsas":     "adjectius",
    "Siesta":     "temps",
    "Luna":       "natura",
    "Bruja":      "vocabulari",
    "Escoba":     "casa",
    "Fiesta":     "expressions",
    "Ruido":      "casa",
    "Silencio":   "vocabulari",
    "Fiebre":     "cos",
    "Libro":      "objectes",
    "Baja":       "adjectius",
    "Esquina":    "llocs",
    "Hasta":      "expressions",
    "Presupuesto": "economia",
    "Apellido":   "vocabulari",
    "Edad":       "vocabulari",
    "Profesion":  "profesiones",
}

def add_missing_tags():
    print("\n── 4. Add missing tags ──")
    ids = find_notes(f'deck:"{DECK}"')
    notes = get_notes_info(ids)

    tagged = 0
    for n in notes:
        if not n:
            continue
        front = n["fields"]["Front"]["value"].strip()
        if not n["tags"] and front in TAG_MAP:
            add_tags([n["noteId"]], TAG_MAP[front])
            print(f"  🏷️  [{front}] → {TAG_MAP[front]}")
            tagged += 1

    print(f"  → Tagged {tagged} cards")


# ---------------------------------------------------------------------------
# Step 5: Fix the estovalles card (wrong Front text)
# ---------------------------------------------------------------------------
def fix_estovalles():
    print("\n── 5. Fix estovalles card ──")
    ids = find_notes(f'deck:"{DECK}"')
    notes = get_notes_info(ids)
    for n in notes:
        if not n:
            continue
        front = n["fields"]["Front"]["value"].strip()
        if "Tijeras" in front:
            update_fields(n["noteId"], {
                "Front": "Mantel / estovalles",
                "Back": "Les estovalles<br><i>(sempre en plural)</i>"
            })
            print("  ✏️  Fixed estovalles card Front")
            return
    print("  ⚠️  estovalles card not found")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print(f"🔧 Comprehensive cleanup of '{DECK}'...\n")

    remove_duplicates()
    delete_old_individuals()
    fix_remaining()
    add_missing_tags()
    fix_estovalles()

    # Final count
    final = find_notes(f'deck:"{DECK}"')
    print(f"\n✅ Done! '{DECK}' now has {len(final)} cards.")
