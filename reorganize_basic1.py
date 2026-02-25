"""
reorganize_basic1.py
--------------------
Modifies EXISTING cards in cpnl basic 1 [dev]:

  1. Consolidate days of week → one card with abbreviations (delete individuals)
  2. Consolidate months → one card (delete individuals)
  3. Consolidate seasons → one card (delete individuals)
  4. Fix 'De vegades' card → add 'cop' with examples
  5. Add 'rap' to verdures list card
  6. Expand possessives (meva/teva/seva) card
  7. Add examples to indirect object pronouns (em/et/li) card
  8. Fix 'buit/buida' card

All operations are idempotent — safe to run multiple times.
"""

from anki_client import find_notes, get_notes_info, invoke, add_note

DECK = "cpnl basic 1 [dev]"


def load_index(deck):
    ids = find_notes(f'deck:"{deck}"')
    notes = get_notes_info(ids)
    return {n["fields"]["Front"]["value"].strip(): n for n in notes if n}


def update_fields(note_id, fields):
    invoke("updateNoteFields", note={"id": note_id, "fields": fields})


def delete_notes(note_ids):
    invoke("deleteNotes", notes=note_ids)


def add_tags(note_ids, tags_str):
    invoke("addTags", notes=note_ids, tags=tags_str)


def upsert(idx, deck, front, back, tags, model="Basic"):
    existing = idx.get(front.strip())
    if existing:
        update_fields(existing["noteId"], {"Front": front, "Back": back})
        old = " ".join(existing["tags"])
        if old: invoke("removeTags", notes=[existing["noteId"]], tags=old)
        invoke("addTags", notes=[existing["noteId"]], tags=" ".join(tags))
        print(f"  ✏️  Updated : {front}")
    else:
        add_note(deck, model, {"Front": front, "Back": back}, tags, allow_duplicate=True)
        print(f"  ✅ Added   : {front}")


# ---------------------------------------------------------------------------
# 1. Consolidate days of the week
# ---------------------------------------------------------------------------
DAY_FRONTS = ["Lunes","Martes","Miercoles","Jueves","Viernes","Sabado","Domingo"]
DAYS_COMBINED_FRONT = "Los días de la semana"
DAYS_COMBINED_BACK = (
    "<b>Dies de la setmana</b><br><br>"
    "Dilluns &nbsp;&nbsp;· Dl ·&nbsp; (lunes)<br>"
    "Dimarts &nbsp;&nbsp;· Dt ·&nbsp; (martes)<br>"
    "Dimecres · Dc ·&nbsp; (miércoles)<br>"
    "Dijous &nbsp;&nbsp;&nbsp;· Dj ·&nbsp; (jueves)<br>"
    "Divendres · Dv ·&nbsp; (viernes)<br>"
    "Dissabte &nbsp;· Ds ·&nbsp; (sábado)<br>"
    "Diumenge &nbsp;· Dg ·&nbsp; (domingo)"
)

def consolidate_days(idx):
    print("\n── 1. Consolidate days of week ──")
    to_delete = [idx[f]["noteId"] for f in DAY_FRONTS if f in idx]
    if to_delete:
        delete_notes(to_delete)
        print(f"  🗑️  Deleted {len(to_delete)} individual day cards")
    upsert(idx, DECK, DAYS_COMBINED_FRONT, DAYS_COMBINED_BACK, ["temps"])


# ---------------------------------------------------------------------------
# 2. Consolidate months
# ---------------------------------------------------------------------------
MONTH_FRONTS = ["Enero","Febrero","Marzo","Abril","Mayo","Junio",
                "Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"]
MONTHS_COMBINED_FRONT = "Los meses del año"
MONTHS_COMBINED_BACK = (
    "<b>Els mesos de l'any</b><br><br>"
    "Gener &nbsp;&nbsp;&nbsp;· Febrer · Març<br>"
    "Abril &nbsp;&nbsp;&nbsp;&nbsp;· Maig &nbsp;&nbsp;· Juny<br>"
    "Juliol &nbsp;&nbsp;&nbsp;· Agost &nbsp;· Setembre<br>"
    "Octubre · Novembre · Desembre"
)

def consolidate_months(idx):
    print("\n── 2. Consolidate months ──")
    to_delete = [idx[f]["noteId"] for f in MONTH_FRONTS if f in idx]
    if to_delete:
        delete_notes(to_delete)
        print(f"  🗑️  Deleted {len(to_delete)} individual month cards")
    upsert(idx, DECK, MONTHS_COMBINED_FRONT, MONTHS_COMBINED_BACK, ["temps"])


# ---------------------------------------------------------------------------
# 3. Consolidate seasons
# ---------------------------------------------------------------------------
SEASON_FRONTS = ["Verano","Invierno","El otoño","Primavera"]
SEASONS_COMBINED_FRONT = "Las estaciones del año"
SEASONS_COMBINED_BACK = (
    "<b>Les estacions de l'any</b><br><br>"
    "🌱 La primavera (primavera)<br>"
    "☀️ L'estiu (verano)<br>"
    "🍂 La tardor (otoño)<br>"
    "❄️ L'hivern (invierno)"
)

def consolidate_seasons(idx):
    print("\n── 3. Consolidate seasons ──")
    to_delete = [idx[f]["noteId"] for f in SEASON_FRONTS if f in idx]
    if to_delete:
        delete_notes(to_delete)
        print(f"  🗑️  Deleted {len(to_delete)} individual season cards")
    upsert(idx, DECK, SEASONS_COMBINED_FRONT, SEASONS_COMBINED_BACK, ["temps"])


# ---------------------------------------------------------------------------
# 4. Fix vegades / cop card
# ---------------------------------------------------------------------------
def fix_vegades(idx):
    print("\n── 4. Fix vegades / cop card ──")
    front = "Aveces"
    back = (
        "<b>De vegades / a vegades</b> = a veces<br><br>"
        "<b>Un cop / una vegada</b> = una vez<br>"
        "<b>Dos cops / dues vegades</b> = dos veces<br><br>"
        "<i>De vegades surto a córrer</i> (A veces salgo a correr)<br>"
        "<i>Ho he fet un cop</i> (Lo he hecho una vez)<br>"
        "<i>Sovint hi vaig, però de vegades no puc</i>"
    )
    upsert(idx, DECK, front, back, ["temps","expressions"])


# ---------------------------------------------------------------------------
# 5. Add rap to verdures card
# ---------------------------------------------------------------------------
def fix_verdures(idx):
    print("\n── 5. Add rap to verdures ──")
    # Find the verdures list card by its front content
    note = None
    for front, n in idx.items():
        if "Verduras" in front or "verduras" in front.lower():
            note = n
            break

    if not note:
        print("  ⚠️  Verdures card not found")
        return

    current_back = note["fields"]["Back"]["value"]
    if "Rap" in current_back or "rap" in current_back:
        print("  ℹ️  Rap already present, skipping")
        return

    new_back = current_back.rstrip() + "<br>El rap (rape)"
    update_fields(note["noteId"], {"Back": new_back})
    print(f"  ✏️  Added rap to verdures card")


# ---------------------------------------------------------------------------
# 6. Expand possessives card
# ---------------------------------------------------------------------------
def fix_possessives(idx):
    print("\n── 6. Expand possessives (meva/teva/seva) ──")
    front = "Mío, tuyo,suyo "  # Note: check exact front including possible spaces
    # Try variants
    note = idx.get("Mío, tuyo,suyo") or idx.get("Mío, tuyo,suyo ") or idx.get("Mío, tuyo, suyo")
    if not note:
        # Search more broadly
        for k, n in idx.items():
            if "tuyo" in k.lower():
                note = n
                break

    if not note:
        print("  ⚠️  Possessives card not found")
        return

    new_front = "Posesivos / possessius"
    new_back = (
        "<b>Possessius</b> — masc. / fem. / masc.pl / fem.pl<br><br>"
        "meu &nbsp;&nbsp;/ meva &nbsp;&nbsp;/ meus &nbsp;&nbsp;/ meves &nbsp;&nbsp;(mi/mis)<br>"
        "teu &nbsp;&nbsp;/ teva &nbsp;&nbsp;/ teus &nbsp;&nbsp;/ teves &nbsp;&nbsp;(tu/tus)<br>"
        "seu &nbsp;&nbsp;/ seva &nbsp;&nbsp;/ seus &nbsp;&nbsp;/ seves &nbsp;&nbsp;(su/sus - ell/a)<br>"
        "nostre / nostra / nostres / nostres (nuestro/a)<br>"
        "vostre / vostra / vostres / vostres (vuestro/a)<br>"
        "seu &nbsp;&nbsp;/ seva &nbsp;&nbsp;/ seus &nbsp;&nbsp;/ seves &nbsp;&nbsp;(su/sus - ells/es)"
    )
    update_fields(note["noteId"], {"Front": new_front, "Back": new_back})
    invoke("addTags", notes=[note["noteId"]], tags="pronoms")
    print(f"  ✏️  Expanded possessives card")


# ---------------------------------------------------------------------------
# 7. Add examples to em/et/li card
# ---------------------------------------------------------------------------
def fix_pronouns(idx):
    print("\n── 7. Add examples to em/et/li card ──")
    note = None
    for k, n in idx.items():
        if "Em" in k and ("nosotros" in k or "mí" in k or "A mí" in k):
            note = n
            break

    if not note:
        print("  ⚠️  em/et/li card not found")
        return

    new_back = (
        "<b>Pronoms febles (OI)</b> — indirect object<br><br>"
        "em &nbsp;(me) &nbsp;&nbsp;→ &nbsp;<i>Em dóna el pa</i> (Me da el pan)<br>"
        "et &nbsp;&nbsp;(te) &nbsp;&nbsp;&nbsp;→ &nbsp;<i>Et truco demà</i> (Te llamo mañana)<br>"
        "li &nbsp;&nbsp;(le) &nbsp;&nbsp;&nbsp;→ &nbsp;<i>Li explico la història</i> (Le explico la historia)<br>"
        "ens (nos) &nbsp;→ &nbsp;<i>Ens escriu cada dia</i> (Nos escribe cada día)<br>"
        "us &nbsp;&nbsp;(os) &nbsp;&nbsp;→ &nbsp;<i>Us porto un regal</i> (Os traigo un regalo)<br>"
        "els &nbsp;(les) &nbsp;→ &nbsp;<i>Els dono les claus</i> (Les doy las llaves)<br><br>"
        "<b>Davant vocal: em→m', et→t', li→li</b><br>"
        "<i>M'agrada (me gusta) · T'estimo (te quiero)</i>"
    )
    update_fields(note["noteId"], {"Back": new_back})
    invoke("addTags", notes=[note["noteId"]], tags="pronoms")
    print(f"  ✏️  Updated em/et/li card with examples")


# ---------------------------------------------------------------------------
# 8. Fix buit/buida (already enriched as Vacio → Buit/buida/buits/buides)
#    Add the feminine form as standalone if not present
# ---------------------------------------------------------------------------
def fix_buit(idx):
    print("\n── 8. Check buit/buida ──")
    note = idx.get("Vacio") or idx.get("Vacío")
    if note:
        current = note["fields"]["Back"]["value"]
        if "buida" not in current.lower():
            update_fields(note["noteId"], {"Back": "Buit / buida / buits / buides"})
            print(f"  ✏️  Added buida to buit card")
        else:
            print(f"  ℹ️  Already has buida: {current}")
    else:
        print("  ⚠️  Buit card not found")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print(f"🔧 Reorganizing '{DECK}'...\n")
    idx = load_index(DECK)
    print(f"Loaded {len(idx)} notes.\n")

    consolidate_days(idx)
    consolidate_months(idx)
    consolidate_seasons(idx)
    fix_vegades(idx)
    fix_verdures(idx)
    fix_possessives(idx)
    fix_pronouns(idx)
    fix_buit(idx)

    print("\n✅ Reorganization complete!")
