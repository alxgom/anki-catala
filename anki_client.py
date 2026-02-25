"""
anki_client.py
--------------
A simple Python client for the AnkiConnect local API (http://localhost:8765).
Requires Anki desktop to be running with the AnkiConnect add-on installed.

AnkiConnect add-on code: 2055492159
"""

import json
import urllib.request
import urllib.error


ANKI_CONNECT_URL = "http://localhost:8765"


def invoke(action: str, **params):
    """
    Send a request to the AnkiConnect API.

    Args:
        action: The AnkiConnect action name (e.g. 'deckNames', 'findNotes')
        **params: Parameters for the action

    Returns:
        The result from AnkiConnect, or raises an exception on error.
    """
    payload = json.dumps({
        "action": action,
        "version": 6,
        "params": params
    }).encode("utf-8")

    request = urllib.request.Request(ANKI_CONNECT_URL, payload)
    try:
        response = urllib.request.urlopen(request, timeout=5)
    except urllib.error.URLError as e:
        raise ConnectionError(
            "Could not connect to AnkiConnect. "
            "Make sure Anki is running and the AnkiConnect add-on (code: 2055492159) is installed.\n"
            f"Original error: {e}"
        )

    result = json.loads(response.read().decode("utf-8"))

    if result.get("error") is not None:
        raise Exception(f"AnkiConnect error: {result['error']}")

    return result["result"]


# ---------------------------------------------------------------------------
# Deck helpers
# ---------------------------------------------------------------------------

def get_deck_names() -> list[str]:
    """Return a list of all deck names."""
    return invoke("deckNames")


def get_deck_names_and_ids() -> dict:
    """Return a dict of {deck_name: deck_id}."""
    return invoke("deckNamesAndIds")


# ---------------------------------------------------------------------------
# Note / Card helpers
# ---------------------------------------------------------------------------

def find_notes(query: str) -> list[int]:
    """
    Find notes by Anki search query.
    Example queries: 'deck:Catalan', 'tag:verb', '*'
    """
    return invoke("findNotes", query=query)


def get_notes_info(note_ids: list[int]) -> list[dict]:
    """Return full info for a list of note IDs."""
    return invoke("notesInfo", notes=note_ids)


def add_note(deck_name: str, model_name: str, fields: dict, tags: list[str] = None) -> int:
    """
    Add a single note to a deck.

    Args:
        deck_name:  Name of the target deck (e.g. 'Catalan::Basic2')
        model_name: Note type (e.g. 'Basic', 'Basic (and reversed card)')
        fields:     Dict of field name → value (e.g. {'Front': 'gat', 'Back': 'cat'})
        tags:       Optional list of tags

    Returns:
        The new note's ID.
    """
    note = {
        "deckName": deck_name,
        "modelName": model_name,
        "fields": fields,
        "tags": tags or [],
        "options": {
            "allowDuplicate": False
        }
    }
    return invoke("addNote", note=note)


def add_notes(notes: list[dict], allow_duplicates: bool = False) -> list[int]:
    """
    Add multiple notes at once.
    Each item in `notes` should be a dict with keys:
      deckName, modelName, fields, tags
    """
    formatted = [
        {
            "deckName": n["deckName"],
            "modelName": n["modelName"],
            "fields": n["fields"],
            "tags": n.get("tags", []),
            "options": {"allowDuplicate": allow_duplicates}
        }
        for n in notes
    ]
    return invoke("addNotes", notes=formatted)


def get_model_names() -> list[str]:
    """Return a list of all note type (model) names."""
    return invoke("modelNames")


def get_model_field_names(model_name: str) -> list[str]:
    """Return the field names for a given note type."""
    return invoke("modelFieldNames", modelName=model_name)


# ---------------------------------------------------------------------------
# Connection test
# ---------------------------------------------------------------------------

def test_connection():
    """Quick sanity-check: print version and available decks."""
    print("🔌 Testing AnkiConnect connection...")
    try:
        version = invoke("version")
        print(f"✅ Connected! AnkiConnect API version: {version}")

        decks = get_deck_names()
        print(f"\n📚 Found {len(decks)} deck(s):")
        for deck in sorted(decks):
            print(f"   • {deck}")

        models = get_model_names()
        print(f"\n🗂️  Found {len(models)} note type(s):")
        for model in sorted(models):
            print(f"   • {model}")

    except ConnectionError as e:
        print(f"❌ {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")


if __name__ == "__main__":
    test_connection()
