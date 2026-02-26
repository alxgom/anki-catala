"""
card_helpers.py
---------------
HTML helper functions for card content generation.
Provides pronunciation marking (vocal neutra, silent letters)
and verb conjugation table formatting.
"""


def vn(word: str, positions: list[int]) -> str:
    """
    Mark neutral vowels (vocal neutra) in a word.
    Wraps characters at given positions with <span class="vn">.

    Usage:
        vn("petit", [0])   → 'p<span class="vn">e</span>tit'
        vn("botiga", [0,5]) → '<span class="vn">b</span>otig<span class="vn">a</span>'
    """
    chars = list(word)
    result = []
    for i, ch in enumerate(chars):
        if i in positions:
            result.append(f'<span class="vn">{ch}</span>')
        else:
            result.append(ch)
    return "".join(result)


def sl(word: str, positions: list[int]) -> str:
    """
    Mark silent letters (lletra muda) in a word.
    Wraps characters at given positions with <span class="sl">.

    Usage:
        sl("temps", [3])  → 'tem<span class="sl">p</span>s'
    """
    chars = list(word)
    result = []
    for i, ch in enumerate(chars):
        if i in positions:
            result.append(f'<span class="sl">{ch}</span>')
        else:
            result.append(ch)
    return "".join(result)


def verb_table(infinitive: str, forms: list[str], tense: str = "Present") -> str:
    """
    Generate a styled HTML table for a verb conjugation.

    Args:
        infinitive: Catalan infinitive (e.g. "fer")
        forms: List of 6 conjugated forms [jo, tu, ell, nos, vos, ells]
        tense: Tense label (default "Present")

    Usage:
        verb_table("fer", ["faig","fas","fa","fem","feu","fan"])
    """
    jo, tu, ell, nos, vos, ells = forms
    return (
        f'<div class="verb-card">'
        f'<div class="verb-inf">{infinitive}</div>'
        f'<div class="verb-tense">{tense}</div>'
        f'<table class="verb-table">'
        f'<tr><td class="pronoun">jo</td><td class="form">{jo}</td></tr>'
        f'<tr><td class="pronoun">tu</td><td class="form">{tu}</td></tr>'
        f'<tr><td class="pronoun">ell/a</td><td class="form">{ell}</td></tr>'
        f'<tr><td class="pronoun">nosaltres</td><td class="form">{nos}</td></tr>'
        f'<tr><td class="pronoun">vosaltres</td><td class="form">{vos}</td></tr>'
        f'<tr><td class="pronoun">ells/es</td><td class="form">{ells}</td></tr>'
        f'</table>'
        f'</div>'
    )
