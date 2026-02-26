"""Quick batch fix script — writes log to file to avoid encoding issues."""
import sys, json
sys.stdout.reconfigure(encoding='utf-8')
from anki_client import find_notes, get_notes_info, invoke

DECK = "cpnl basic 1 [dev]"
LOG = []

def log(msg):
    LOG.append(msg)

def update(nid, fields):
    invoke("updateNoteFields", note={"id": nid, "fields": fields})

def tag(nids, t):
    invoke("addTags", notes=nids, tags=t)

FIXES = {
    "La noche":   {"Back": "La nit"},
    "Despues":    {"Back": "Després"},
    "Sin":        {"Back": "Sense"},
    "Delante":    {"Back": "Davant"},
    "Detras":     {"Back": "Darrere"},
    "Padre/madre": {"Back": "Pare/mare"},
    "Tío/tia":    {"Back": "Oncle/tieta"},
    "Entrar":     {"Back": "Entrar"},
    "Bailar":     {"Back": "Ballar"},
    "Quedarse":   {"Back": "Quedar-se<br><br>Em quedo<br>Et quedes<br>Es queda<br>Ens quedem<br>Us quedeu<br>Es queden"},
    "Recibidor":  {"Back": "El rebedor"},
    "Cocina":     {"Back": "La cuina"},
    "Puerta":     {"Back": "La porta"},
    "Ropa":       {"Back": "La roba"},
    "Presupuesto": {"Back": "El pressupost"},
    "Profesion":  {"Back": "La professió"},
    "Fiesta":     {"Back": "La festa"},
    "Luna":       {"Back": "La lluna"},
    "Escoba":     {"Back": "L'escombra"},
    "Fiebre":     {"Back": "La febre"},
    "Libro":      {"Back": "El llibre"},
    "Esquina":    {"Back": "La cantonada"},
    "Ruido":      {"Back": "El soroll"},
    "Silencio":   {"Back": "El silenci"},
    "Alquiler":   {"Back": "El lloguer"},
    "Siesta":     {"Back": "La migdiada"},
    "Baja":       {"Back": "Baixa / baix (adj. m/f)"},
    "Negocio":    {"Back": "La botiga"},
    "Ensalada":   {"Back": "L'amanida"},
    "Pez":        {"Back": "El peix"},
    "Perro":      {"Back": "El gos / la gossa"},
    "Apellido":   {"Back": "El cognom"},
    "Edad":       {"Back": "L'edat (fem.)"},
    "Hoy":        {"Back": "Avui"},
}

TAG_MAP = {
    "Salir": "verbes", "Entrar": "verbes", "Bailar": "verbes",
    "Mismo": "adjectius", "Verdaderas": "adjectius", "Falsas": "adjectius",
    "Siesta": "temps", "Luna": "natura", "Bruja": "vocabulari",
    "Escoba": "casa", "Fiesta": "expressions", "Ruido": "casa",
    "Silencio": "vocabulari", "Fiebre": "cos", "Libro": "objectes",
    "Baja": "adjectius", "Esquina": "llocs", "Hasta": "expressions",
    "Presupuesto": "economia", "Apellido": "vocabulari",
    "Edad": "vocabulari", "Profesion": "profesiones",
}

ids = find_notes(f'deck:"{DECK}"')
notes = get_notes_info(ids)

fixed = 0
tagged = 0

for n in notes:
    if not n: continue
    front = n["fields"]["Front"]["value"].strip()
    if front in FIXES:
        update(n["noteId"], FIXES[front])
        log(f"Fixed: [{front}]")
        fixed += 1
    if not n["tags"] and front in TAG_MAP:
        tag([n["noteId"]], TAG_MAP[front])
        log(f"Tagged: [{front}] -> {TAG_MAP[front]}")
        tagged += 1

# Fix estovalles
for n in notes:
    if not n: continue
    if "Tijeras" in n["fields"]["Front"]["value"]:
        update(n["noteId"], {"Front": "Mantel / estovalles", "Back": "Les estovalles<br><i>(sempre en plural)</i>"})
        log("Fixed estovalles card")
        fixed += 1
        break

# Delete old unfixed pronoun/possessives cards
OLD_FRONTS = ["A mí/a ti/ a el/ a nosotros/ a vostre/ a ells", "Mío, tuyo,suyo"]
to_del = [n["noteId"] for n in notes if n and n["fields"]["Front"]["value"].strip() in OLD_FRONTS]
if to_del:
    invoke("deleteNotes", notes=to_del)
    log(f"Deleted {len(to_del)} old pronoun/possessives cards")

final = find_notes(f'deck:"{DECK}"')
log(f"\nDone! Fixed {fixed}, tagged {tagged}. Deck now has {len(final)} cards.")

with open("cleanup_log.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(LOG))

print(f"Done. Fixed={fixed} Tagged={tagged} Total={len(final)}")
