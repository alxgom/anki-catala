# Anki Català — Project Documentation

## What Is This?

A collection of Python scripts to build, manage, and improve Anki flashcard decks for learning Catalan (specifically aligned with CPNL coursework).

The scripts communicate with **Anki desktop** via the **AnkiConnect** add-on to create, update, and delete cards programmatically.

---

## Prerequisites

### 1. Anki Desktop

- Download from [apps.ankiweb.net](https://apps.ankiweb.net/)
- **Must be open and running** before you execute any script

### 2. AnkiConnect Add-on

- Inside Anki: `Tools → Add-ons → Get Add-ons`
- Enter code: **`2055492159`**
- Restart Anki after installing
- The add-on runs a local API server at `http://localhost:8765`

### 3. Python 3.10+

- No external packages needed — all scripts use only the standard library

---

## ⚠️ Important Rules

1. **Always open Anki desktop first** before running any script
2. **Never run scripts against the original decks** — always use `[dev]` copies
3. **Don't close the black PowerShell window** — scripts make hundreds of sequential API calls (~0.5s each) and may take 2-4 minutes. The window looks stuck but it's working
4. Scripts are **idempotent** — safe to run multiple times (upsert logic: update if exists, create if not)

---

## Current Decks

| Deck                 | Cards | Description                                         |
| -------------------- | ----- | --------------------------------------------------- |
| `cpnl basic 1`       | 186   | Original deck (do not modify directly)              |
| `cpnl basic 1 [dev]` | 177   | Working copy — cleaned, enriched, tagged            |
| `cpnl bàsic 2`       | 3     | Original deck                                       |
| `cpnl bàsic 2 [dev]` | 12    | Working copy with new content                       |
| `Verbs Essencials`   | 19    | Dedicated verb deck with present-tense conjugations |

---

## Scripts Reference

### Core Client

| Script           | Description                                                                                                                                         |
| ---------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| `anki_client.py` | AnkiConnect HTTP client. All other scripts import from here. Functions: `invoke()`, `find_notes()`, `get_notes_info()`, `add_note()`, `add_notes()` |

### Deck Setup

| Script                | Description                                           | Run When                             |
| --------------------- | ----------------------------------------------------- | ------------------------------------ |
| `clone_deck.py`       | Clone a deck to a `[dev]` copy                        | Once per deck, before making changes |
| `create_verb_deck.py` | Create the `Verbs Essencials` deck with 10 core verbs | Once (already run)                   |

### Inspection & Audit

| Script            | Description                                              | Run When                |
| ----------------- | -------------------------------------------------------- | ----------------------- |
| `inspect_deck.py` | Print note types, fields, and sample cards from a deck   | Exploring a new deck    |
| `dump_deck.py`    | Export all notes from `cpnl basic 1` to `deck_dump.json` | Snapshot before changes |
| `dump_basic2.py`  | Export all notes from `cpnl bàsic 2` to JSON             | Snapshot                |
| `audit_all.py`    | Dump all cards from all 3 decks into `audit_all.txt`     | Full review             |
| `check_cards.py`  | Quick check of specific cards (Basic 2 + fruits secs)    | Spot checks             |

### Fixes & Cleanup

| Script                  | Description                                                                       | Run When              |
| ----------------------- | --------------------------------------------------------------------------------- | --------------------- |
| `fix_deck.py`           | Fix critical errors, typos, tags, whitespace in Basic 1 dev                       | First cleanup pass    |
| `enrich_forms.py`       | Add masc/fem/plural forms to adjective and color cards                            | After fix_deck        |
| `fix_basic2.py`         | Fix missing genders and incomplete cards in Basic 2 dev                           | After cloning Basic 2 |
| `quick_fix.py`          | Batch fix remaining typos, add missing articles, tag cards, delete old duplicates | Final cleanup         |
| `cleanup_duplicates.py` | Comprehensive cleanup (alternative to quick_fix, more verbose)                    | Alternative cleanup   |
| `reorganize_basic1.py`  | Consolidate days/months/seasons, expand possessives, fix pronouns                 | After fix_deck        |

### Content Addition

| Script                | Description                                                                   | Run When               |
| --------------------- | ----------------------------------------------------------------------------- | ---------------------- |
| `add_content.py`      | Add new verbs, vocab, and Basic 2 content across all decks. Uses upsert logic | Adding new content     |
| `update_verb_deck.py` | Fix verb deck labels/tags and clean old verb cards in Basic 1                 | After create_verb_deck |

### Utility (temporary)

| Script                 | Description                                              |
| ---------------------- | -------------------------------------------------------- |
| `_find_pronouncard.py` | Debug script to locate and fix the em/et/li pronoun card |

---

## Typical Workflow

### Adding new vocabulary

```
1. Open Anki desktop
2. Edit add_content.py → add entries to NEW_BASIC1 or NEW_BASIC2
3. Run: python add_content.py
4. Check cards in Anki → Browse → select deck
5. Commit: git add -A; git commit -m "Add new vocab"; git push
```

### Fixing existing cards

```
1. Open Anki desktop
2. Run: python audit_all.py (generates audit_all.txt)
3. Review audit_all.txt for issues
4. Edit quick_fix.py with corrections
5. Run: python quick_fix.py
6. Verify in Anki, commit
```

### Creating a dev copy of a new deck

```
1. Open Anki desktop
2. Edit clone_deck.py → change source/target deck names
3. Run: python clone_deck.py
4. The [dev] copy is now safe to modify
```

---

## File Structure

```
c:\DEV\anki_catalan\
├── anki_client.py          # Core API client (import this)
├── brainstorming.md        # Future development ideas & roadmap
├── DOCS.md                 # This file
│
├── clone_deck.py           # Clone decks
├── create_verb_deck.py     # Build verb deck
├── add_content.py          # Add new cards (upsert)
│
├── fix_deck.py             # Fix errors & typos
├── enrich_forms.py         # Add gendered forms
├── fix_basic2.py           # Fix Basic 2 cards
├── quick_fix.py            # Final batch fixes
├── reorganize_basic1.py    # Consolidate cards
├── update_verb_deck.py     # Fix verb deck
├── cleanup_duplicates.py   # Remove duplicates
│
├── inspect_deck.py         # Inspect deck structure
├── dump_deck.py            # Export deck to JSON
├── dump_basic2.py          # Export Basic 2
├── audit_all.py            # Full audit dump
├── check_cards.py          # Quick card check
│
├── deck_dump.json          # Snapshot of original Basic 1
├── audit_all.txt           # Latest full audit
├── cleanup_log.txt         # Last cleanup run log
│
├── AnkiConnect.py          # AnkiConnect add-on source (forked)
├── README.md               # Original AnkiConnect README
└── tests/                  # AnkiConnect tests
```

---

## Tags Taxonomy

| Tag                                                            | Category                       |
| -------------------------------------------------------------- | ------------------------------ |
| `casa`, `mobles`                                               | Home, furniture                |
| `llocs`                                                        | Places                         |
| `temps`                                                        | Time, calendar                 |
| `verbes`, `verbes::irregular`, `verbes::essencials`            | Verbs                          |
| `present`, `conj::-ar`, `conj::-er`, `conj::-ir`, `conj::-ure` | Verb tense & conjugation group |
| `relaciones`                                                   | Family, relationships          |
| `roba`, `complements`                                          | Clothing, accessories          |
| `posiciones`                                                   | Positions, directions          |
| `adjectius`                                                    | Adjectives                     |
| `colors`                                                       | Colors                         |
| `profesiones`, `restauració`                                   | Professions                    |
| `alimentació`, `fruits_secs`                                   | Food                           |
| `numeros`                                                      | Numbers                        |
| `cos`                                                          | Body                           |
| `transport`                                                    | Transport                      |
| `preguntas`                                                    | Questions                      |
| `pronoms`, `pronoms::en`                                       | Pronouns                       |
| `expressions`                                                  | Expressions, connectors        |
| `economia`                                                     | Economy                        |
| `animales`                                                     | Animals                        |
| `vocabulari`, `objectes`, `natura`                             | General vocabulary             |
