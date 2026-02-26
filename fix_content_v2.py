"""
fix_content_v2.py
------------------
Comprehensive content fix:
1. Strip ALL Spanish text from Back fields (parenthetical translations)
2. Fix hosteleria card: add Spanish job list to Front
3. Add missing articles to remaining cards
4. Re-apply tags (they got wiped by tag cleanup bug)
5. Fix pronoun card to be Catalan-only
6. Clean up chunk cards (body, accessories, days, seasons, expressions)

Rule: Front = 100% Spanish, Back = 100% Catalan
"""

import sys, re
sys.stdout.reconfigure(encoding='utf-8')
from anki_client import find_notes, get_notes_info, invoke
from card_helpers import verb_table

LOG = []
def log(msg): LOG.append(msg)

def update(nid, fields):
    invoke("updateNoteFields", note={"id": nid, "fields": fields})

def tag(nids, t):
    invoke("addTags", notes=nids, tags=t)


# =========================================================================
# TAG MAP - complete re-tagging since all tags got wiped
# =========================================================================
TAG_MAP = {
    "La cama": "casa", "La chimenea": "casa", "El balcon": "casa",
    "El dormitorio": "casa", "La ventana": "casa", "La mesa": "casa",
    "El comedor": "casa", "El living": "casa", "El baño": "casa",
    "Cocina": "casa", "Garage": "casa", "Puerta": "casa",
    "Recibidor": "casa", "El lavadero": "casa", "El pasillo": "casa",
    "Alacena": "casa", "Alquiler": "casa", "Luz": "casa",
    "Mantel / estovalles": "casa", "Silla": "casa mobles",
    "Toalla / servilleta": "casa",

    "Plaza": "llocs", "Casa": "llocs", "Calle": "llocs",
    "Avenida": "llocs", "Barrio": "llocs", "Parque": "llocs",
    "Negocio": "llocs", "Teatro": "llocs", "Esquina": "llocs",

    "Semana": "temps", "Día": "temps", "La tarde": "temps",
    "La noche": "temps", "La mañana": "temps", "El mediodia": "temps",
    "La madrugada": "temps", "Ahora": "temps", "Hoy": "temps",
    "Luego": "temps", "Mañana": "temps", "Ayer": "temps",
    "Despues": "temps", "Año": "temps", "Siempre": "temps",
    "Seguido": "temps", "Siesta": "temps",
    "Los días de la semana": "temps",
    "Los meses del año": "temps",
    "Las estaciones del año": "temps",

    "Padre/madre": "relaciones", "Hermano/hermana": "relaciones",
    "Tío/tia": "relaciones", "Chico/chica": "relaciones",
    "Hijo/hija": "relaciones", "Primo/prima": "relaciones",
    "Sobrino/sobrina": "relaciones", "Vecinos": "relaciones",
    "Amigo": "relaciones",

    "Ropa": "roba", "Complementos / accesorios": "roba complements",

    "Escribir": "verbes", "Leer": "verbes", "Ver": "verbes",
    "Tener": "verbes", "Amar": "verbes", "Vivir": "verbes",
    "Salir": "verbes", "Entrar": "verbes", "Dar": "verbes",
    "Llamarse": "verbes", "Ser": "verbes verbes::irregular",
    "Hacer": "verbes", "Recomendar": "verbes", "Estar": "verbes",
    "Haber": "verbes", "Demandar": "verbes", "Ponerse": "verbes verbes::irregular",
    "Ir": "verbes verbes::irregular", "Agarrar": "verbes",
    "Saber": "verbes", "Girar": "verbes", "Poder": "verbes",
    "Probar": "verbes", "Parar": "verbes", "Querer": "verbes",
    "Beber": "verbes", "Quedarse": "verbes", "Bailar": "verbes",
    "Regular -ar": "verbes",

    "Rojo": "colors", "Verde": "colors", "Amarillo": "colors",
    "Azul": "colors",

    "Medico": "profesiones", "Plomero": "profesiones",
    "Cocinero": "profesiones", "El trabajo": "profesiones",
    "Profesion": "profesiones",

    "Delante": "posicions", "Detras": "posicions",
    "Derecha": "posicions", "Izquierda": "posicions",
    "Entrando": "posicions", "Saliendo": "posicions",
    "A dentro": "posicions", "Afuera": "posicions",
    "Al fondo": "posicions", "Lejos": "posicions",
    "Cerca": "posicions",

    "Caliente": "adjectius", "Frio": "adjectius",
    "Caluroso": "adjectius", "Fresco": "adjectius",
    "Dulce": "adjectius", "Salado": "adjectius",
    "Seco": "adjectius", "Duro": "adjectius",
    "Largo": "adjectius", "Corto": "adjectius",
    "Caro": "adjectius", "Dificil": "adjectius",
    "Lleno/pleno": "adjectius", "Vacio": "adjectius",
    "Mismo": "adjectius", "Verdaderas": "adjectius",
    "Falsas": "adjectius", "Baja": "adjectius",

    "Ensalada": "alimentacio", "Pez": "alimentacio",
    "Albóndigas": "alimentacio", "Dorada (pescado)": "alimentacio",
    "Miel": "alimentacio", "Frutos secos": "alimentacio",
    "Desayuno": "alimentacio", "Almuerzo": "alimentacio",
    "Merienda": "alimentacio", "Cena": "alimentacio",

    "Dieciséis": "numeros", "Segundo": "numeros",
    "Números ordinales": "numeros",

    "Cuerpo": "cos", "Cabello": "cos", "Piel": "cos",
    "Partes del cuerpo": "cos",

    "Perro": "animals",

    "A mí / a ti / a ell / a nosaltres...": "pronoms",
    "Posesivos / possessius": "pronoms",

    "Aveces": "expressions temps",
    "Sin": "expressions",
    "Hasta": "expressions",
    "Por favor": "expressions",

    "Apellido": "vocabulari", "Edad": "vocabulari",
    "Luna": "vocabulari", "Bruja": "vocabulari",
    "Escoba": "casa", "Fiebre": "cos",
    "Libro": "vocabulari", "Ruido": "vocabulari",
    "Silencio": "vocabulari", "Fiesta": "vocabulari",
    "Presupuesto": "economia",
}


# =========================================================================
# FIELD FIXES - Spanish removed from Backs, missing articles added
# =========================================================================
FIELD_FIXES = {
    # --- Chunk cards: remove Spanish translations ---
    "Partes del cuerpo": {
        "Back": (
            "<b>El cos</b><br><br>"
            "El cap<br>L'orella<br>El coll<br>"
            "Les mans<br>Els peus<br>Les cames<br>"
            "La panxa<br>L'esquena<br>El nas<br>"
            "La boca<br>Els ulls"
        )
    },
    "Complementos / accesorios": {
        "Back": (
            "<b>Complements</b><br><br>"
            "El collaret<br>L'anell<br>El braçalet<br>"
            "Les arracades<br>Les orelleres<br>"
            "El gorro / la gorra<br>La bufanda<br>"
            "Els guants<br>El casc<br>"
            "Les botes<br>Els mitjons<br>"
            "Les sandàlies<br>Les xancletes"
        )
    },
    "Frutos secos": {
        "Back": (
            "<b>Els fruits secs</b><br><br>"
            "La nou<br>L'avellana<br>L'ametlla<br>"
            "El pistatxo<br>El cacauet"
        )
    },
    "Los días de la semana": {
        "Back": (
            "<b>Dies de la setmana</b><br><br>"
            "Dilluns · Dl<br>Dimarts · Dt<br>Dimecres · Dc<br>"
            "Dijous · Dj<br>Divendres · Dv<br>"
            "Dissabte · Ds<br>Diumenge · Dg"
        )
    },
    "Las estaciones del año": {
        "Back": (
            "<b>Les estacions de l'any</b><br><br>"
            "La primavera<br>L'estiu<br>La tardor<br>L'hivern"
        )
    },
    "Posesivos / possessius": {
        "Back": (
            "<b>Possessius</b> — m. / f. / m.pl / f.pl<br><br>"
            "meu / meva / meus / meves<br>"
            "teu / teva / teus / teves<br>"
            "seu / seva / seus / seves<br>"
            "nostre / nostra / nostres / nostres<br>"
            "vostre / vostra / vostres / vostres<br>"
            "seu / seva / seus / seves"
        )
    },

    # --- Pronoun card: Catalan only ---
    "A mí / a ti / a ell / a nosaltres...": {
        "Back": (
            "<b>Pronoms febles — complement indirecte</b><br><br>"
            "em<br>et<br>li<br>ens<br>us<br>els<br><br>"
            "<b>Davant vocal:</b><br>"
            "em → m'<br>et → t'"
        )
    },

    # --- Expression cards: remove Spanish translations ---
    "Parece / parece que": {"Back": "Sembla / sembla que...<br><br><i>Sembla que plourà</i>"},
    "Entonces / en aquel momento": {"Back": "Aleshores<br><br><i>Aleshores, va decidir marxar</i>"},
    "Cualquier / cualquiera": {"Back": "Qualsevol<br><br><i>Qualsevol dia és bo per aprendre</i>"},
    "Pues / entonces": {"Back": "Doncs<br><br><i>Doncs, ens quedem aquí</i>"},
    "Nunca / jamás": {"Back": "Mai<br><br><i>Mai he estat a Londres</i>"},

    # --- Fix hambre/sed ---
    "Hambre / sed": {"Back": "La fam<br>La set"},

    # --- Fix cambrer/client ---
    "Camarero / cliente": {"Back": "El cambrer / la cambrera<br>El client / la clienta"},

    # --- Hostelería: add Spanish list to Front ---
    "Trabajos en hostelería": {
        "Front": (
            "Trabajos en hostelería<br><br>"
            "Camarero/a<br>Cajero/a<br>Ayudante de cocina<br>"
            "Encargado/a de sala<br>Personal de limpieza<br>Basurero/a"
        ),
        "Back": (
            "<b>Feines de restauració</b><br><br>"
            "El cambrer / la cambrera<br>"
            "El caixer / la caixera<br>"
            "L'ajudant de cuina<br>"
            "L'encarregat / l'encarregada de sala<br>"
            "El personal de neteja<br>"
            "L'escombriaire"
        )
    },

    # --- Toalla: remove Spanish ---
    "Toalla / servilleta": {"Back": "La tovalla<br>El tovalló"},

    # --- Medico: remove Spanish ---
    "Medico": {"Back": "El metge / la metgessa"},

    # --- Baja: simplify ---
    "Baja": {"Back": "Baix / baixa"},

    # --- Edad: remove Spanish ---
    "Edad": {"Back": "L'edat"},

    # --- Still missing articles ---
    "Plaza": {"Back": "La plaça"},
    "Calle": {"Back": "El carrer"},
    "Avenida": {"Back": "L'avinguda"},
    "Barrio": {"Back": "El barri"},
    "Parque": {"Back": "El parc"},
    "Semana": {"Back": "La setmana"},
    "Día": {"Back": "El dia"},
    "Bruja": {"Back": "La bruixa"},
    "Cabello": {"Back": "El cabell"},
    "Piel": {"Back": "La pell"},
    "Cuerpo": {"Back": "El cos"},
    "Teatro": {"Back": "El teatre"},
    "Fiesta": {"Back": "La festa"},
    "Alacena": {"Back": "El rebost"},

    # --- Estovalles fix ---
    "Mantel / estovalles": {"Back": "Les estovalles"},

    # --- Por favor: Catalan only ---
    "Por favor": {"Back": "Si us plau"},

    # --- Verbs in Basic 1 with old <br> format: restyle ---
    "Ver":      {"Back": verb_table("veure",    ["veig","veus","veu","veiem","veieu","veuen"])},
    "Tener":    {"Back": verb_table("tenir",    ["tinc","tens","té","tenim","teniu","tenen"])},
    "Vivir":    {"Back": verb_table("viure",    ["visc","vius","viu","vivim","viviu","viuen"])},
    "Ir":       {"Back": verb_table("anar",     ["vaig","vas","va","anem","aneu","van"])},
    "Saber":    {"Back": verb_table("saber",    ["sé","saps","sap","sabem","sabeu","saben"])},
    "Quedarse": {"Back": verb_table("quedar-se",["em quedo","et quedes","es queda","ens quedem","us quedeu","es queden"])},
    "Querer":   {"Back": verb_table("voler",    ["vull","vols","vol","volem","voleu","volen"])},
    "Beber":    {"Back": verb_table("beure",    ["bec","beus","beu","bevem","beveu","beuen"])},
    "Ponerse":  {"Back": verb_table("posar-se", ["em poso","et poses","es posa","ens posem","us poseu","es posen"])},
    "Hacer":    {"Back": verb_table("fer",      ["faig","fas","fa","fem","feu","fan"])},
    "Estar":    {"Back": verb_table("estar",    ["estic","estàs","està","estem","esteu","estan"])},
    "Haber":    {"Back": verb_table("haver",    ["he","has","ha","hem","heu","han"])},
}


# =========================================================================
# MAIN
# =========================================================================
if __name__ == "__main__":
    log("=== Fixing card content ===")

    for deck in ["cpnl basic 1 [dev]", "cpnl bàsic 2 [dev]"]:
        ids = find_notes(f'deck:"{deck}"')
        notes = get_notes_info(ids)
        log(f"\n--- {deck} ({len(notes)} cards) ---")

        for n in notes:
            if not n: continue
            front = n["fields"]["Front"]["value"].strip()

            # Apply field fixes
            if front in FIELD_FIXES:
                update(n["noteId"], FIELD_FIXES[front])
                log(f"  Fixed: [{front}]")

            # Apply tags
            if front in TAG_MAP:
                tag([n["noteId"]], TAG_MAP[front])
                log(f"  Tagged: [{front}] -> {TAG_MAP[front]}")

            # Chunk cards in Front also need tags
            for key in TAG_MAP:
                if key in front and key != front:
                    tag([n["noteId"]], TAG_MAP[key])
                    break

    # Save log
    with open("fix_content_log.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(LOG))

    print("Done! Log saved to fix_content_log.txt")
