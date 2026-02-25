from anki_client import find_notes, get_notes_info, invoke

ids = find_notes('deck:"cpnl basic 1 [dev]"')
notes = get_notes_info(ids)

for n in notes:
    front = n["fields"]["Front"]["value"]
    if "nosotros" in front and ("mí" in front or "Em" in front or "ti" in front):
        new_back = (
            "<b>Pronoms febles (OI)</b> — complement indirecte<br><br>"
            "em &nbsp;(me) &nbsp;&nbsp;→ &nbsp;<i>Em dóna el pa</i> (Me da el pan)<br>"
            "et &nbsp;&nbsp;(te) &nbsp;&nbsp;&nbsp;→ &nbsp;<i>Et truco demà</i> (Te llamo mañana)<br>"
            "li &nbsp;&nbsp;(le) &nbsp;&nbsp;&nbsp;→ &nbsp;<i>Li explico la història</i> (Le explico la historia)<br>"
            "ens (nos) &nbsp;→ &nbsp;<i>Ens escriu cada dia</i> (Nos escribe cada día)<br>"
            "us &nbsp;&nbsp;(os) &nbsp;&nbsp;→ &nbsp;<i>Us porto un regal</i> (Os traigo un regalo)<br>"
            "els &nbsp;(les) &nbsp;→ &nbsp;<i>Els dono les claus</i> (Les doy las llaves)<br><br>"
            "<b>Davant vocal → contracció:</b><br>"
            "em → m' &nbsp;&nbsp;<i>M'agrada</i> (me gusta)<br>"
            "et → t' &nbsp;&nbsp;&nbsp;&nbsp;<i>T'estimo</i> (te quiero)"
        )
        invoke("updateNoteFields", note={"id": n["noteId"], "fields": {
            "Front": "A mí / a ti / a ell / a nosaltres...",
            "Back": new_back
        }})
        invoke("addTags", notes=[n["noteId"]], tags="pronoms")
        print(f"Fixed: {front[:60]}")
        break
