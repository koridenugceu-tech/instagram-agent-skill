#!/usr/bin/env python3
"""
caption.py - revisa un caption de Instagram en español y enseña exactamente lo
que muestra el feed antes del "... más".

Instagram da a un caption unos 125 caracteres en el feed y esconde el resto
detrás de un toque. Casi todos los captions que fallan, fallan ahí: el gancho
está en la tercera frase, la primera línea es un saludo o todo empieza con un
hashtag. Esto imprime la ventana visible en una caja, para que la leas como la
lee un desconocido haciendo scroll, y luego revisa las ocho cosas que merece
la pena revisar.

El corte de 125 caracteres es aproximado. El número real cambia con el
dispositivo, el tamaño de letra y dónde caen tus saltos de línea, y por eso
quieres margen y no un caption calculado para acabar justo en 125. El español
gasta más caracteres que el inglés para decir lo mismo, así que ese margen
importa más aquí. Cámbialo con --truncate si quieres probar uno más estricto.

Uso
  python3 caption.py caption.txt
  python3 caption.py caption.txt --keywords "contratos freelance,precios de agencia"
  pbpaste | python3 caption.py -
  python3 caption.py caption.txt --json
"""

import argparse
import json
import re
import sys
import textwrap

LIMIT = 2200             # el límite duro de Instagram para un caption.
TRUNCATE = 125           # más o menos donde el feed corta con "... más".
HASHTAG_LIMIT = 5        # el tope de Instagram por publicación o reel desde el
                         # 18 de diciembre de 2025, antes 30. Lo anunció la
                         # cuenta @Creators: usar menos hashtags (hasta 5) y más
                         # específicos, en vez de muchos genéricos, mejora el
                         # rendimiento del contenido y la experiencia de la gente.

HASHTAG_RE = re.compile(r"(?:^|\s)(#\w+)")
MENTION_RE = re.compile(r"(?:^|\s)(@[\w.]+)")
LINK_RE = re.compile(r"https?://\S+|\bwww\.\S+|\b[a-z0-9-]+\.(?:com|es|mx|ar|co|io|net|org|ai|app)/\S*",
                     re.IGNORECASE)
EMOJI_RE = re.compile(r"[\U0001F300-\U0001FAFF☀-➿←-⇿️]")
CONCRETE_RE = re.compile(r"[$€]\s?\d|\b\d[\d.,]*\b")
UPPER_WORD = re.compile(r"^[A-ZÁÉÍÓÚÑÜ][a-záéíóúñü]{2,}$")
CONCRETE_WORD = re.compile(
    r"^(?:dos|tres|cuatro|cinco|seis|siete|ocho|nueve|diez|quince|veinte|treinta|"
    r"cien|mil|millón|millones|euros?|dólares|enero|febrero|marzo|abril|mayo|junio|"
    r"julio|agosto|septiembre|octubre|noviembre|diciembre)$")

ASKS = [
    (re.compile(r"(?i:\b(?:comenta|escribe|pon|déjame)\b)\s+(?i:la palabra\s+)?[\"«']?[A-ZÁÉÍÓÚÑ0-9]{2,}\b"),
     "comentar una palabra clave"),
    (re.compile(r"(?i)\b(?:escríbeme|mándame un (?:dm|md|mensaje)|por (?:dm|md|privado)|háblame por)\b"),
     "escribir por DM"),
    (re.compile(r"(?i)\bguárda(?:lo|la|te)\b|\bguarda (?:este|esta|esto)\b"), "guardar"),
    (re.compile(r"(?i)\bcompárte(?:lo|la)\b|\bcomparte (?:este|esta|esto)\b|\b(?:envíaselo|mándaselo|pásaselo)\b"),
     "compartir"),
    (re.compile(r"(?i)\bsígueme\b|\bsigue a @"), "seguir"),
    (re.compile(r"(?i)\b(?:link|enlace) en (?:la |mi )?bio\b"), "enlace en la bio"),
    (re.compile(r"(?i)\bdesliza\b|\bswipe\b|\btoca (?:para|aquí)\b"), "deslizar o tocar"),
    (re.compile(r"(?i)\bcuéntame\b|\bdime\b|¿qué harías\b|¿cuál (?:prefieres|eliges|te quedas)\b"),
     "responder una pregunta"),
]

FILLER_TAGS = {"#viral", "#fyp", "#explore", "#explorepage", "#explorar", "#foryou",
               "#foryoupage", "#parati", "#paratii", "#tendencia", "#tendencias",
               "#trending", "#instagood", "#love", "#amor", "#follow", "#sigueme",
               "#seguidores", "#like4like", "#likes", "#megusta", "#reels",
               "#reelsinstagram", "#viralreels", "#reelsviral", "#instadaily"}


FOLD = str.maketrans("áéíóúüÁÉÍÓÚÜ", "aeiouuAEIOUU")


def fold(s):
    """Compara sin tildes: "vídeo" y "video" son la misma búsqueda."""
    return s.lower().translate(FOLD)


def concrete_hits(text):
    toks = []
    for seg in re.split(r"[.!?¿¡\n]+", text):
        t = re.findall(r"[^\W\d_]+", seg)
        toks.extend((i, w) for i, w in enumerate(t))
    n = len(CONCRETE_RE.findall(text))
    n += sum(1 for i, w in toks if i and UPPER_WORD.match(w))
    n += sum(1 for _, w in toks if CONCRETE_WORD.match(w.lower()))
    return n


def visible_window(text, cut):
    """Lo que enseña el feed. Instagram corta a mitad de palabra, así que esto también."""
    flat = text.strip()
    return flat if len(flat) <= cut else flat[:cut]


def render_box(window, truncated, out=sys.stdout, width=52):
    print("\n  LO QUE ENSEÑA EL FEED", file=out)
    print("  +" + "-" * (width + 2) + "+", file=out)
    lines = []
    for raw in window.split("\n"):
        lines.extend(textwrap.wrap(raw, width) or [""])
    for line in lines[:8]:
        print(f"  | {line:<{width}} |", file=out)
    tail = "... más" if truncated else "(cabe entero)"
    print("  +" + "-" * (width + 2 - len(tail) - 2) + f" {tail} " + "+", file=out)


def analyse(text, cut=TRUNCATE, keywords=None):
    text = text.rstrip()
    stripped = text.strip()
    chars = len(stripped)
    lines = [l for l in stripped.split("\n")]
    first_line = lines[0].strip() if lines else ""
    tags = HASHTAG_RE.findall(stripped)
    mentions = MENTION_RE.findall(stripped)
    links = LINK_RE.findall(stripped)
    emoji = EMOJI_RE.findall(stripped)
    window = visible_window(stripped, cut)
    truncated = chars > cut
    asks = [name for pattern, name in ASKS if pattern.search(stripped)]
    filler = [t for t in tags if t.lower() in FILLER_TAGS]
    keywords = [k.strip() for k in (keywords or []) if k.strip()]

    checks = []

    def add(name, status, detail):
        checks.append({"check": name, "status": status, "detail": detail})

    add("LONGITUD", "MAL" if chars > LIMIT else "BIEN",
        f"{chars} / {LIMIT} caracteres" + (f", {chars - LIMIT} por encima del límite"
                                           if chars > LIMIT else ""))

    if not first_line:
        add("PRIMERA LÍNEA", "MAL", "el caption empieza con una línea en blanco")
    elif first_line.startswith("#") or first_line.startswith("@"):
        add("PRIMERA LÍNEA", "MAL",
            "empieza con un hashtag o una mención, en el único sitio que merece una frase")
    elif re.match(r"(?i)^\s*[¡¿]?(?:hola|holi|buenas|hey|qué tal|feliz (?:lunes|martes|miércoles|jueves|viernes|finde))\b",
                  first_line):
        add("PRIMERA LÍNEA", "OJO", "empieza con un saludo. Nadie abre Instagram para que le saluden")
    elif len(first_line) > cut:
        add("PRIMERA LÍNEA", "OJO",
            f"{len(first_line)} caracteres, así que se corta en el {cut} a media idea. "
            "Bien si el corte deja intriga, mal si cae en una subordinada")
    else:
        add("PRIMERA LÍNEA", "BIEN", f"{len(first_line)} caracteres, cabe entera")

    hits = concrete_hits(window)
    add("GANCHO CONCRETO", "BIEN" if hits else "OJO",
        f"{hits} cifra(s), fecha(s) o nombre(s) en la ventana visible"
        + ("" if hits else " - nada comprobable antes del toque"))

    if len(tags) > HASHTAG_LIMIT:
        add("HASHTAGS", "MAL", f"{len(tags)} hashtags, por encima del tope de Instagram de "
                               f"{HASHTAG_LIMIT}. Los que pasan del quinto no cuentan y el bloque suena a 2019")
    elif len(tags) == HASHTAG_LIMIT and filler:
        add("HASHTAGS", "OJO", f"{len(tags)} hashtags, en el tope, y "
                               f"{len(filler)} genéricos. Gasta los cinco en temas")
    elif filler:
        add("HASHTAGS", "OJO", f"{len(tags)} hashtags, {len(filler)} genéricos "
                               f"({', '.join(filler[:3])}). Esos no describen nada")
    else:
        add("HASHTAGS", "BIEN", f"{len(tags)} hashtag(s)" + (f": {' '.join(tags)}" if tags else ""))

    if not tags:
        add("SITIO DE LOS TAGS", "BIEN", "no hay hashtags que colocar")
    elif any(re.search(r"(?:^|\s)" + re.escape(t) + r"\b", window) for t in tags):
        add("SITIO DE LOS TAGS", "OJO", "hay un hashtag dentro de la ventana visible, "
                                        "gastando espacio del feed en una etiqueta")
    else:
        add("SITIO DE LOS TAGS", "BIEN", "los hashtags están por debajo del corte")

    add("ENLACES", "OJO" if links else "BIEN",
        f"{len(links)} enlace(s) en el caption, y los captions no son clicables. "
        f"Llévalo a la bio o al DM" if links else "no hay enlaces muertos en el texto")

    if len(asks) == 1:
        add("UNA PETICIÓN", "BIEN", f"una llamada a la acción: {asks[0]}")
    elif not asks:
        add("UNA PETICIÓN", "OJO", "no hay llamada a la acción. Decide para qué es este post")
    else:
        add("UNA PETICIÓN", "OJO", f"{len(asks)} peticiones ({', '.join(asks)}). "
                                   "Dos peticiones es lo mismo que ninguna")

    density = len(emoji) * 100 / max(chars, 1)
    add("EMOJIS", "OJO" if density > 4 else "BIEN",
        f"{len(emoji)} emojis, {density:.1f} por cada 100 caracteres"
        + (" - parece decoración" if density > 4 else ""))

    if keywords:
        low = fold(stripped)
        found = [k for k in keywords if fold(k) in low]
        missing = [k for k in keywords if fold(k) not in low]
        in_window = [k for k in found if fold(k) in fold(window)]
        status = "BIEN" if not missing else ("OJO" if found else "MAL")
        add("BÚSQUEDA", status,
            f"{len(found)}/{len(keywords)} presentes"
            + (f", {len(in_window)} en la ventana visible" if found else "")
            + (f". Faltan: {', '.join(missing)}" if missing else ""))

    fails = sum(1 for c in checks if c["status"] == "MAL")
    warns = sum(1 for c in checks if c["status"] == "OJO")
    verdict = "ARREGLAR" if fails else ("REVISAR" if warns else "LISTO")

    return {
        "characters": chars, "limit": LIMIT, "truncate_at": cut,
        "visible": window, "truncated": truncated,
        "first_line_chars": len(first_line),
        "hashtags": tags, "mentions": mentions, "links": links,
        "emoji": len(emoji), "asks": asks,
        "checks": checks, "verdict": verdict,
    }


def render(a, out=sys.stdout):
    head = (f"REVISIÓN DEL CAPTION  ·  {a['characters']} / {a['limit']} caracteres  ·  "
            f"{len(a['hashtags'])} hashtags  ·  {len(a['asks'])} petición(es)")
    print("\n" + head, file=out)
    print("=" * max(len(head), 62), file=out)
    render_box(a["visible"], a["truncated"], out=out)
    print("", file=out)
    for c in a["checks"]:
        print(f"  {c['status']:<5} {c['check']:<18} {c['detail']}", file=out)
    print("-" * max(len(head), 62), file=out)
    print(f"  VEREDICTO  {a['verdict']}\n", file=out)


def main():
    ap = argparse.ArgumentParser(description="Revisa un caption de Instagram en español.")
    ap.add_argument("input", nargs="?", default="-", help="archivo del caption, o - para stdin")
    ap.add_argument("--truncate", type=int, default=TRUNCATE,
                    help=f"caracteres visibles antes de '... más' (por defecto {TRUNCATE})")
    ap.add_argument("--keywords", default="", help="términos separados por comas por los que quieres que te encuentren")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except Exception:
            pass
    if args.input == "-":
        sys.stdin.reconfigure(encoding="utf-8")
        raw = sys.stdin.read()
    else:
        raw = open(args.input, encoding="utf-8").read()
    a = analyse(raw, cut=args.truncate, keywords=args.keywords.split(","))
    if args.json:
        print(json.dumps(a, indent=2, ensure_ascii=False))
    else:
        render(a)
    sys.exit(0 if a["verdict"] == "LISTO" else 1)


if __name__ == "__main__":
    main()
