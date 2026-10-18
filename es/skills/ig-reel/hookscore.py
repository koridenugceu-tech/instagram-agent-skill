#!/usr/bin/env python3
"""
hookscore.py - puntúa la primera frase de un Reel en español según las cinco
cosas que tienen en común los ganchos fuertes, y ordena un lote de ellos.

Qué es:  cinco heurísticas locales, calculadas en tu máquina a partir del
texto. Miden propiedades que suelen compartir los ganchos que retienen: que
se diga en menos de tres segundos, que tenga algo concreto, que haya algo en
juego, que lo interesante esté delante y no detrás, y que vaya dirigido a
alguien.

Qué NO es:  un predictor de visualizaciones. Se probó contra 80 ganchos
reales en español (los tres primeros segundos de los subtítulos automáticos
de los 8 shorts con más y los 8 con menos vistas de cinco canales):
distingue un gancho real de uno escrito a propósito para ser malo (AUC 0,85)
y NO distingue los éxitos de un creador de sus fracasos (AUC 0,49, donde 0,50
es tirar una moneda). La versión inglesa dio lo mismo: 0,83 y 0,56.
Úsala para cazar saludos, preámbulos, ganchos sin nada concreto y ganchos que
tardan cinco segundos en decirse. Para elegir entre dos ganchos decentes,
fíate de la gráfica de retención, no de este script.

La duración se calcula por sílabas, no por palabras: en español "y" y
"desafortunadamente" no tardan lo mismo en decirse.

Cada comprobación devuelve de 0 a 100. Más alto es mejor.

Uso
  python3 hookscore.py ganchos.txt              # un gancho por línea, ordenados
  python3 hookscore.py --hook "Perdí 18.000 € por una cláusula que no estaba."
  pbpaste | python3 hookscore.py -
  python3 hookscore.py ganchos.txt --json
"""

import argparse
import json
import re
import statistics
import sys

SPS = 6.0                # sílabas por segundo al hablar a cámara (medido en 80 shorts:
                         # mediana 6,3, la mitad central entre 5,7 y 6,9). Ajústalo con --sps.
HOOK_SECONDS = 3.0

WORD_RE = re.compile(r"[^\W_]+(?:[.,]\d+)*[%€$]?|[$€]\d[\d.,]*|[€$%]")
NUMBER_RE = re.compile(
    r"[$€]\s?\d[\d.,]*"                                    # dinero delante
    r"|\b\d[\d.,]*\s?"                                     # una cifra, con o
    r"(?:%|€|k\b|x\b|h\b|horas?\b|min\b|minutos?\b"        # sin unidad
    r"|días?\b|semanas?\b|meses?\b|años?\b|mil\b)?",
    re.IGNORECASE)
UPPER_WORD = re.compile(r"^[A-ZÁÉÍÓÚÑÜ][a-záéíóúñü]{2,}$")
HASHTAG_RE = re.compile(r"(?:^|\s)#\w+")
EMOJI_RE = re.compile(r"[\U0001F300-\U0001FAFF☀-➿]")

# Los ganchos hablados dicen los números en voz alta. "Cero euros" y "veinte
# mil" son tan concretos como "0 €" y "20.000". "Uno" y "primero" no están a
# propósito: son relleno mucho más a menudo que una cantidad.
SPOKEN_NUMBER = re.compile(
    r"^(?:cero|dos|tres|cuatro|cinco|seis|siete|ocho|nueve|diez|once|doce|trece|"
    r"catorce|quince|dieci\w+|veinte|veinti\w+|treinta|cuarenta|cincuenta|sesenta|"
    r"setenta|ochenta|noventa|cien|ciento|\w+cientos|\w+cientas|mil|millón|millones|"
    r"docena|mitad|doble|triple)$")
MONEY_WORDS = {
    "euros", "euro", "dólares", "dólar", "pavos", "pelas", "pesos", "lucas",
    "céntimos", "facturación", "facturo", "facturé", "beneficio", "beneficios",
    "sueldo", "salario", "alquiler", "ingresos", "millonario", "millonaria", "precio",
}

# Palabras que ponen algo en juego. Un gancho sin ninguna es una afirmación;
# con una, es un motivo para seguir mirando.
STAKES = {
    "deja", "dejes", "dejé", "dejar", "nunca", "jamás", "mal", "error", "errores",
    "equivocas", "equivocado", "equivocada", "perdí", "perdió", "perdimos", "perder",
    "pierdes", "pierde", "pierden", "perdiendo", "perdido", "costó", "cuesta",
    "cuestan", "costar", "costado", "arruiné", "arruinó", "roto", "rota", "fracasé",
    "fracaso", "fracasó", "fallé", "falla", "fallo", "nadie", "ninguno", "ninguna",
    "no", "ni", "sin", "renuncié", "dimití", "despidieron", "despedí", "despedido",
    "despedida", "borré", "borra", "borrar", "eliminé", "elimina", "mató", "mata",
    "sustituyó", "reemplazó", "sustituye", "reemplaza", "recorté", "gratis",
    "pagué", "pagas", "pagaba", "pagando", "cobré", "cobras", "cobraba", "cobro",
    "cobrar", "contraté", "ahorré", "ahorra", "ahorrar", "primera", "primer",
    "prohibido", "prohibida", "ilegal", "peor", "odio", "odiaba", "desperdicié",
    "tiré", "estafa", "mentira", "mentí", "mienten", "verdad", "secreto", "oculto",
    "oculta", "robé", "robado", "robaron", "antes", "hasta", "pero", "excepto",
    "salvo", "problema", "riesgo", "peligro", "cuidado", "ojo", "arrepiento",
    "ojalá", "debería", "deberías", "todavía", "aún", "ya", "solo", "sólo",
    "contra", "realmente", "vs", "versus", "frente",
}

# Aperturas que gastan el primer segundo sin decir nada. Se comparan por
# palabras completas, no por prefijo: "es" no debe atrapar a "esto".
WEAK_OPENERS = [
    "bueno", "vale", "ok", "okey", "hola", "hey", "buenas", "chicos", "chicas",
    "gente", "amigos", "familia", "bienvenidos", "bienvenidas", "hoy", "básicamente",
    "sinceramente", "honestamente", "la verdad", "mira", "oye", "eh", "em", "pues",
    "simplemente", "solo quería", "quería", "quiero", "vamos a", "uno de", "una de",
    "alguna vez", "sabías", "te has", "has", "en este", "en el vídeo", "en el video",
    "la cosa", "hay", "esto es", "este es", "esta es", "es", "como un", "como una",
    "cuando se trata", "si alguna", "ya sabes", "qué tal", "muy buenas", "así que",
    "entonces",
]

# Imperativos que se ganan el primer puesto.
IMPERATIVES = {
    "deja", "roba", "copia", "borra", "elimina", "prueba", "mira", "lee", "guarda",
    "usa", "construye", "haz", "escribe", "envía", "manda", "coge", "toma", "empieza",
    "nunca", "no", "pon", "revisa", "apunta", "cambia", "sube", "olvida", "evita",
    "pregunta", "cobra", "dejad", "mirad", "probad", "haced", "dejá", "mirá", "probá",
    "róbame", "cópiame", "guárdalo", "guárdate", "pruébalo", "apúntate", "quítate",
    "olvídate", "mándame", "escríbeme",
}

FIRST_PERSON = {
    "yo", "me", "mi", "mis", "mí", "conmigo", "mío", "mía", "nosotros", "nosotras",
    "nos", "nuestro", "nuestra", "nuestros", "nuestras", "soy", "estoy", "tengo",
    "llevo", "hago", "he", "hice", "tuve", "fui", "estuve", "pude", "puse", "dije",
    "creo", "quiero", "puedo", "voy", "somos", "estamos", "tenemos", "hemos",
}
SECOND_PERSON = {
    "tú", "te", "ti", "tu", "tus", "contigo", "tuyo", "tuya", "vosotros", "vosotras",
    "os", "vuestro", "vuestra", "usted", "ustedes", "vos", "eres", "estás", "tienes",
    "haces", "puedes", "quieres", "sabes", "necesitas", "llevas", "vas", "has",
    "sigues", "crees", "piensas", "publicas", "subes", "cobras", "vendes", "pierdes",
    "ganas", "buscas", "usas", "sois", "estáis", "tenéis",
}
NOT_FIRST = {"aquí", "allí", "ahí", "así", "café", "bebé", "esquí", "también"}
NOT_SECOND = {"más", "jamás", "atrás", "detrás", "demás", "quizás", "además",
              "después", "través", "revés", "inglés", "francés", "interés", "estrés"}

DEALBREAKERS = [
    (re.compile(r"(?i)^\s*(?:deja de (?:hacer scroll|scrollear|bajar)|para de hacer scroll|"
                r"no hagas scroll|no sigas bajando)"),
     "Empieza con \"deja de hacer scroll\". Pedir atención demuestra que no te la has ganado."),
    (re.compile(r"(?i)\b(?:en (?:este|el) (?:vídeo|video|reel)(?: de hoy)?|"
                r"hoy te voy a (?:enseñar|mostrar|contar)|te voy a (?:enseñar|mostrar) (?:cómo|como))\b"),
     "Preámbulo de vídeo. Bórralo y empieza por la recompensa."),
    (re.compile(r"(?i)^\s*[¡¿]?(?:hola|hey|buenas|qué tal|muy buenas|bienvenid[oa]s)\b"),
     "Saludo. Nadie abre Instagram para que le saluden."),
    (HASHTAG_RE,
     "Hashtag en el gancho. Los hashtags van al final del caption, si van en algún sitio."),
    (EMOJI_RE,
     "Emoji en el gancho. El texto en pantalla a tamaño de gancho tiene sitio para palabras o "
     "para un emoji, no para las dos cosas."),
]

STRONG_VOWELS = set("aeoáéóíú")


def number_syllables(v):
    """Sílabas aproximadas de un número dicho en voz alta."""
    if v < 10:
        return 2
    if v < 30:
        return 3
    if v < 100:
        return 4
    if v < 1000:
        return 5
    if v < 1_000_000:
        k, r = divmod(v, 1000)
        return (number_syllables(k) if k > 1 else 0) + 1 + (number_syllables(r) if r else 0)
    m, r = divmod(v, 1_000_000)
    return number_syllables(m) + 3 + (number_syllables(r) if r else 0)


def syllables(token):
    """Cuenta sílabas en español: núcleos vocálicos, con hiato entre dos vocales fuertes."""
    w = token.lower()
    extra = 0
    if "%" in w:
        extra += 4                                   # "por ciento"
    if "€" in w:
        extra += 2                                   # "euros"
    if "$" in w:
        extra += 3                                   # "dólares"
    digits = re.sub(r"[^\d]", "", w.split(",")[0]) if re.search(r"\d", w) else ""
    if digits:
        return number_syllables(int(digits)) + extra
    if w == "y":
        return 1
    n = 0
    for g in re.findall(r"[aeiouáéíóúü]+", w):
        n += 1
        n += sum(1 for a, b in zip(g, g[1:]) if a in STRONG_VOWELS and b in STRONG_VOWELS)
    return (n or (0 if extra else 1)) + extra


def clamp(n):
    return max(0.0, min(100.0, n))


def words(text):
    return WORD_RE.findall(text)


def lower_tokens(text):
    return [x.lower() for x in words(text)]


def is_number(tok):
    return bool(re.match(r"^[$€]?\d", tok))


def check_length(text, sps=SPS):
    """Un gancho tiene que llegar antes de que se mueva el pulgar. Unos dos o tres segundos."""
    w = words(text)
    n = len(w)
    syl = sum(syllables(t) for t in w)
    secs = syl / sps
    chars = len(text.strip())
    if 5 <= n <= 14:
        score = 100.0
    elif n < 5:
        score = clamp(100 - (5 - n) * 20)
    else:
        score = clamp(100 - (n - 14) * 10)
    if secs > HOOK_SECONDS + 1.5:          # el margen que la versión inglesa da a 12 palabras
        score -= (secs - HOOK_SECONDS - 1.5) * 15
    if chars > 65:                       # dos líneas de texto grande en pantalla
        score -= 12
    return clamp(score), (f"{n} palabras, {syl} sílabas, {chars} caracteres, "
                          f"~{secs:.1f}s dicho (lo ideal, 5-14 palabras)")


def check_specificity(text):
    """Una cosa concreta gana a tres abstractas."""
    nums = [x.strip() for x in NUMBER_RE.findall(text) if x.strip()]
    toks = words(text)
    propers = {t for t in toks[1:] if UPPER_WORD.match(t)}
    low = [t.lower() for t in toks]
    spoken = [t for t in low if SPOKEN_NUMBER.match(t) or t in MONEY_WORDS]
    hits = len(nums) + len(propers) + len(spoken)
    score = 15.0 if hits == 0 else clamp(45 + hits * 30)
    found = ", ".join(nums[:2] + sorted(propers)[:2] + spoken[:2])
    return score, (f"{hits} marca(s) concreta(s)" + (f": {found}" if found else
                   " - ni cifra, ni nombre, nada comprobable"))


def check_stakes(text):
    """Tensión, coste, negación. Algo que quien mira podría perder."""
    low = lower_tokens(text)
    markers = sorted({x for x in low if x in STAKES})
    if re.search(r"[$€]\s?\d|\d\s?€", text):
        markers.append("un precio")
    n = len(markers)
    score = {0: 20.0, 1: 70.0}.get(n, 100.0)
    detail = f"{n} marca(s) de tensión" + (f": {', '.join(markers[:4])}" if markers else
                                           " - en esta frase no hay nada en juego")
    return clamp(score), detail


def starts_with(low, phrase):
    p = phrase.split()
    return low[:len(p)] == p


def check_frontload(text):
    """La palabra interesante no puede estar en la posición nueve."""
    w = words(text)
    if not w:
        return 0.0, "vacío"
    low = [x.lower() for x in w]
    penalty = 0
    hit_opener = None
    for weak in WEAK_OPENERS:
        if starts_with(low, weak):
            penalty, hit_opener = 30, weak
            break
    payload = None
    for i, token in enumerate(low):
        if (token in STAKES or SPOKEN_NUMBER.match(token) or token in MONEY_WORDS
                or is_number(w[i]) or (i and UPPER_WORD.match(w[i]))):
            payload = i
            break
    if payload is None:
        base = 30.0
        where = "no hay ninguna palabra con carga en toda la frase"
    elif payload <= 3:
        base = 100.0
        where = f"la carga está en la palabra {payload + 1}"
    elif payload <= 6:
        base = 70.0
        where = f"la carga está en la palabra {payload + 1}, podría ir antes"
    else:
        base = 40.0
        where = f"la carga está en la palabra {payload + 1}, demasiado tarde"
    detail = where + (f"; apertura floja \"{hit_opener}\"" if hit_opener else "")
    return clamp(base - penalty), detail


def is_second(t):
    return t in SECOND_PERSON or (len(t) >= 4 and re.search(r"(?:ás|és|áis|éis)$", t)
                                  and t not in NOT_SECOND)


def is_first(t):
    return t in FIRST_PERSON or (len(t) >= 4 and t[-1] in "éí" and t not in NOT_FIRST)


def check_address(text):
    """Dirigido a una persona, o flotando en el aire. El español omite el
    pronombre, así que también cuenta la forma del verbo ("llevas", "perdí")."""
    low = lower_tokens(text)
    if any(is_second(t) for t in low):
        return 100.0, "le habla a quien mira"
    if low and low[0] in IMPERATIVES:
        return 90.0, f"empieza con un imperativo (\"{low[0]}\")"
    if any(is_first(t) for t in low):
        return 70.0, "primera persona, sin nombrar a quien mira"
    return 35.0, "tercera persona, no hay nadie en la sala"


CHECKS = ["LONGITUD", "CONCRECIÓN", "TENSIÓN", "ARRANQUE", "DESTINATARIO"]


def run(text, sps=SPS):
    results = {
        "LONGITUD": check_length(text, sps),
        "CONCRECIÓN": check_specificity(text),
        "TENSIÓN": check_stakes(text),
        "ARRANQUE": check_frontload(text),
        "DESTINATARIO": check_address(text),
    }
    flags = [msg for pattern, msg in DEALBREAKERS if pattern.search(text)]
    scores = [results[c][0] for c in CHECKS]
    # La propiedad más floja limita el gancho, con la misma lógica que
    # detect.py: basta con una mala para que el pulgar siga bajando.
    overall = statistics.mean(scores) * 0.6 + min(scores) * 0.4 - len(flags) * 15
    overall = clamp(overall)
    verdict = "FUERTE" if overall >= 70 and min(scores) >= 55 and not flags else (
        "OK" if overall >= 50 else "FLOJO")
    return results, overall, verdict, flags


def bar(score, width=24):
    filled = round(score / 100 * width)
    return "#" * filled + "." * (width - filled)


def render_one(text, results, overall, verdict, flags, out=sys.stdout):
    print("\nNOTA DEL GANCHO", file=out)
    print("=" * 62, file=out)
    print(f"  \"{text.strip()}\"\n", file=out)
    for name in CHECKS:
        score, detail = results[name]
        print(f"  {name:<13} {bar(score)} {score:5.1f}", file=out)
        print(f"  {'':<13} {detail}", file=out)
    print("-" * 62, file=out)
    print(f"  {'NOTA':<13} {bar(overall)} {overall:5.1f}   {verdict}", file=out)
    for f in flags:
        print(f"\n  ELIMINATORIO  {f}", file=out)
    if verdict != "FUERTE":
        weakest = min(CHECKS, key=lambda c: results[c][0])
        print(f"\n  Propiedad más floja: {weakest}. Arregla esa y vuelve a pasarlo.", file=out)
    print("", file=out)


def render_table(rows, out=sys.stdout):
    print("\nRANKING DE GANCHOS\n" + "=" * 78, file=out)
    for i, r in enumerate(rows, 1):
        mark = "->" if i == 1 else "  "
        hook = r["hook"] if len(r["hook"]) <= 62 else r["hook"][:59] + "..."
        print(f"{mark} {r['score']:5.1f} {r['verdict']:<7} {hook}", file=out)
        print(f"        más floja: {r['weakest']} ({r['checks'][r['weakest']]['score']:.0f})", file=out)
        for f in r["flags"]:
            print(f"        eliminatorio: {f}", file=out)
    print("\nGraba el primero. Si el primero está por debajo de 50, ninguno de estos es el gancho.\n",
          file=out)


def main():
    ap = argparse.ArgumentParser(description="Puntúa un gancho de Reel en español en cinco propiedades.")
    ap.add_argument("input", nargs="?", default="-", help="archivo con un gancho por línea, o -")
    ap.add_argument("--hook", help="puntúa un solo gancho pasado por la línea de comandos")
    ap.add_argument("--sps", type=float, default=SPS,
                    help=f"sílabas por segundo al hablar (por defecto {SPS})")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except Exception:
            pass
    if args.hook:
        lines = [args.hook]
    else:
        if args.input == "-":
            sys.stdin.reconfigure(encoding="utf-8")
            raw = sys.stdin.read()
        else:
            raw = open(args.input, encoding="utf-8").read()
        lines = [l.strip() for l in raw.splitlines() if l.strip()]
    if not lines:
        print("no hay nada que puntuar", file=sys.stderr)
        sys.exit(2)

    payload = []
    for line in lines:
        results, overall, verdict, flags = run(line, args.sps)
        payload.append({
            "hook": line,
            "checks": {k: {"score": round(v[0], 1), "detail": v[1]} for k, v in results.items()},
            "weakest": min(CHECKS, key=lambda c: results[c][0]),
            "flags": flags,
            "score": round(overall, 1),
            "verdict": verdict,
        })

    if args.json:
        print(json.dumps(payload if len(payload) > 1 else payload[0], indent=2, ensure_ascii=False))
        return

    if len(payload) == 1:
        results, overall, verdict, flags = run(lines[0], args.sps)
        render_one(lines[0], results, overall, verdict, flags)
    else:
        render_table(sorted(payload, key=lambda r: -r["score"]))

    sys.exit(0 if max(p["score"] for p in payload) >= 70 else 1)


if __name__ == "__main__":
    main()
