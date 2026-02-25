"""
create_verb_deck.py
-------------------
Creates a polished dedicated deck for the 10 most essential Catalan verbs.

Deck name: "Verbs Essencials"
Card format:
  Front: Spanish infinitive
  Back:  Catalan infinitive + full present tense conjugation

Conjugation format (using HTML <br> and <b> for clarity):
  <b>Catalan infinitive</b><br>
  <br>
  jo     →  faig<br>
  tu     →  fas<br>
  ell/a  →  fa<br>
  nosaltres → fem<br>
  vosaltres → feu<br>
  ells/es   → fan
"""

from anki_client import invoke, add_note

DECK = "Verbs Essencials"
MODEL = "Basic"
TAGS = ["verbes", "verbes::essencials"]


def conj(infinitive, forms):
    """Build a clean Back field with infinitive + present tense table."""
    jo, tu, ell, nos, vos, ells = forms
    return (
        f"<b>{infinitive}</b><br><br>"
        f"jo &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;→ {jo}<br>"
        f"tu &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;→ {tu}<br>"
        f"ell/a &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;→ {ell}<br>"
        f"nosaltres → {nos}<br>"
        f"vosaltres &nbsp;→ {vos}<br>"
        f"ells/es &nbsp;&nbsp;&nbsp;→ {ells}"
    )


# ---------------------------------------------------------------------------
# Verb data: (Spanish front, Catalan infinitive, [jo, tu, ell, nos, vos, ells])
# ---------------------------------------------------------------------------
VERBS = [
    (
        "Ser",
        "ser",
        ["soc", "ets", "és", "som", "sou", "són"],
    ),
    (
        "Estar",
        "estar",
        ["estic", "estàs", "està", "estem", "esteu", "estan"],
    ),
    (
        "Tenir",
        "tenir",
        ["tinc", "tens", "té", "tenim", "teniu", "tenen"],
    ),
    (
        "Fer",
        "fer",
        ["faig", "fas", "fa", "fem", "feu", "fan"],
    ),
    (
        "Ir / Anar",
        "anar",
        ["vaig", "vas", "va", "anem", "aneu", "van"],
    ),
    (
        "Querer / Poder querer",
        "voler",
        ["vull", "vols", "vol", "volem", "voleu", "volen"],
    ),
    (
        "Poder",
        "poder",
        ["puc", "pots", "pot", "podem", "podeu", "poden"],
    ),
    (
        "Saber",
        "saber",
        ["sé", "saps", "sap", "sabem", "sabeu", "saben"],
    ),
    (
        "Venir",
        "venir",
        ["vinc", "véns", "vé", "venim", "veniu", "vénen"],
    ),
    (
        "Vivir",
        "viure",
        ["visc", "vius", "viu", "vivim", "viviu", "viuen"],
    ),
]


def main():
    print(f"\n🃏 Creating deck: '{DECK}'")
    invoke("createDeck", deck=DECK)
    print("✅ Deck created.\n")

    for spanish, catalan, forms in VERBS:
        back = conj(catalan, forms)
        note_id = add_note(
            deck_name=DECK,
            model_name=MODEL,
            fields={"Front": spanish, "Back": back},
            tags=TAGS,
            allow_duplicate=True,
        )
        if note_id:
            print(f"  ✅ Added: {spanish} → {catalan}")
        else:
            print(f"  ⚠️  Skipped (duplicate?): {spanish}")

    print(f"\n🎉 Done! Check Anki for the '{DECK}' deck.")


if __name__ == "__main__":
    main()
