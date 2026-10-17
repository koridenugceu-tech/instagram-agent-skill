#!/usr/bin/env python3
"""
detect.py - panel de cinco comprobaciones que puntúa cuánto parece escrito
por una máquina un borrador en español.

Qué es:  cinco heurísticas locales basadas en las señales que miden los
detectores públicos de IA: variación en la longitud de las frases,
concreción, vocabulario de relleno, huella tipográfica y voz. Cada nota se
calcula en tu máquina a partir del texto. No se sube nada.

Qué NO es:  GPTZero, Originality, Copyleaks, Winston ni Turnitin. No llama a
sus API y no puede prometer su veredicto. Detecta lo mismo en lo que se fijan
todos, y por eso arreglarlo suele mover también sus números, pero la única
afirmación honesta es la de esta línea.

Lo que cambia respecto a la versión inglesa: el español no tiene
contracciones ("don't", "I'm"), así que la VOZ se mide con marcas coloquiales
(pues, vale, o sea, ¿no?, en plan...) y con la persona gramatical. Y como el
español omite el pronombre ("perdí 18.000 €", no "yo perdí"), la primera y la
segunda persona se cuentan también por la forma del verbo, no solo por los
pronombres.

Cada comprobación devuelve una nota HUMANA de 0 a 100. Más alto es mejor.

Uso
  python3 detect.py borrador.txt
  pbpaste | python3 detect.py -
  python3 detect.py borrador.txt --json
  python3 detect.py antes.txt despues.txt      # comparar dos borradores
"""

import argparse
import json
import os
import re
import statistics
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
LEX = os.path.join(HERE, "slop.json")

sys.path.insert(0, HERE)
from humanize import term_pattern          # noqa: E402  (misma búsqueda que el humanizador)

SENT_RE = re.compile(r"[^.!?\n]+[.!?]*")
WORD_RE = re.compile(r"[^\W\d_]+(?:'[^\W\d_]+)?")
NUMBERS = re.compile(r"\b\d[\d.,]*\s?%?|[$€]\s?\d|\d\s?€")
# En español los meses y los días van en minúscula y las cifras se dicen con
# letra, así que la mayúscula no basta para encontrar lo concreto. "Uno" y
# "primero" no están: son relleno mucho más a menudo que una cantidad.
CONCRETE_WORD = re.compile(
    r"^(?:cero|dos|tres|cuatro|cinco|seis|siete|ocho|nueve|diez|once|doce|trece|"
    r"catorce|quince|dieci\w+|veinte|veinti\w+|treinta|cuarenta|cincuenta|sesenta|"
    r"setenta|ochenta|noventa|cien|ciento|\w+cientos|\w+cientas|mil|millón|millones|"
    r"docena|mitad|doble|triple|euros?|dólar(?:es)?|pesos|pavos|céntimos|"
    r"enero|febrero|marzo|abril|mayo|junio|julio|agosto|septiembre|setiembre|"
    r"octubre|noviembre|diciembre|lunes|martes|miércoles|jueves|viernes|sábado|domingo)$")
UPPER_WORD = re.compile(r"^[A-ZÁÉÍÓÚÑÜ][a-záéíóúñü]{2,}$")
COLLOQUIAL = re.compile(
    r"(?i)(?<!\w)(?:pues|vale|o sea|en plan|tío|tía|guay|súper|mogollón|la verdad|"
    r"jaja\w*|jeje\w*|xd|uf+|buah|venga|ojo|mira|oye|che|wey|güey|órale|chido|neta|"
    r"bacán|chévere|parce|ahorita|nomás|pa)(?!\w)"
    r"|¿(?:no|vale|sabes|eh|ves|verdad)\?"
    r"|(?m:^\s*bueno,)")

FIRST_PERSON = {
    "yo", "me", "mi", "mis", "mí", "conmigo", "mío", "mía", "míos", "mías",
    "nosotros", "nosotras", "nos", "nuestro", "nuestra", "nuestros", "nuestras",
    "soy", "estoy", "tengo", "llevo", "hago", "he", "hice", "tuve", "fui", "estuve",
    "pude", "puse", "dije", "quise", "vine", "creo", "pienso", "quiero", "puedo",
    "voy", "vi", "somos", "estamos", "tenemos", "hemos", "hicimos",
}
SECOND_PERSON = {
    "tú", "te", "ti", "tu", "tus", "contigo", "tuyo", "tuya", "tuyos", "tuyas",
    "vosotros", "vosotras", "os", "vuestro", "vuestra", "vuestros", "vuestras",
    "usted", "ustedes", "vos", "eres", "estás", "tienes", "haces", "puedes",
    "quieres", "sabes", "necesitas", "llevas", "vas", "has", "sigues", "crees",
    "piensas", "publicas", "subes", "cobras", "vendes", "pierdes", "ganas",
    "buscas", "usas", "sois", "estáis", "tenéis",
}
# Palabras que acaban como un pretérito en primera persona (-é, -í) o como un
# voseo (-ás, -és) y no lo son.
NOT_FIRST = {"aquí", "allí", "ahí", "así", "café", "bebé", "puré", "josé", "rené",
             "esquí", "rubí", "maniquí", "jabalí", "colibrí", "olé", "también"}
NOT_SECOND = {"más", "jamás", "atrás", "detrás", "demás", "quizás", "además",
              "después", "través", "revés", "inglés", "francés", "interés", "cortés",
              "japonés", "portugués", "holandés", "estrés", "ciempiés", "compás",
              "satanás", "tomás", "andrés", "inés", "jesús"}


def clamp(n):
    return max(0.0, min(100.0, n))


def scale(value, human, machine):
    """Lleva value a 0-100, donde `human` -> 100 y `machine` -> 0."""
    if human == machine:
        return 50.0
    return clamp((value - machine) / (human - machine) * 100)


def sentences(text):
    return [s.strip() for s in SENT_RE.findall(text) if len(s.split()) > 2]


def words(text):
    return WORD_RE.findall(text)


def person_hits(tokens):
    """Primera y segunda persona, con pronombre o sin él."""
    n = 0
    for t in (w.lower() for w in tokens):
        if t in FIRST_PERSON or t in SECOND_PERSON:
            n += 1
        elif len(t) >= 4 and t[-1] in "éí" and t not in NOT_FIRST:
            n += 1                                  # perdí, gasté, aprendí
        elif len(t) >= 4 and re.search(r"(?:ás|és|áis|éis)$", t) and t not in NOT_SECOND:
            n += 1                                  # tenés, podés, tenéis
    return n


def proper_nouns(text):
    """Palabras con mayúscula que no abren frase. ¿ y ¡ abren frase."""
    found = set()
    for seg in re.split(r"[.!?¿¡\n]+", text):
        toks = re.findall(r"[^\W\d_]+", seg)
        for t in toks[1:]:
            if UPPER_WORD.match(t):
                found.add(t)
    return found


def check_burstiness(text):
    """Las personas varían mucho la longitud de las frases. Los modelos escriben parejo."""
    lens = [len(s.split()) for s in sentences(text)]
    if len(lens) < 4:
        return 50.0, "demasiado corto para juzgar"
    mean = statistics.mean(lens)
    cv = statistics.pstdev(lens) / mean if mean else 0
    score = scale(cv, human=0.70, machine=0.22)
    return score, f"variación {cv:.2f} en {len(lens)} frases (lo ideal, 0.55+)"


def check_specificity(text):
    """Cifras, nombres y sustantivos concretos. El relleno es abstracto."""
    w = words(text)
    if len(w) < 25:
        return 50.0, "demasiado corto para juzgar"
    per100 = 100 / len(w)
    hits = (len(NUMBERS.findall(text)) + len(proper_nouns(text))
            + sum(1 for t in w if CONCRETE_WORD.match(t.lower())))
    density = hits * per100
    score = scale(density, human=6.0, machine=0.5)
    return score, f"{hits} marcas concretas, {density:.1f} por cada 100 palabras (lo ideal, 4+)"


def check_slop(text, lex):
    """Densidad de vocabulario de relleno según el léxico."""
    w = words(text)
    if not w:
        return 50.0, "vacío"
    hits, found = 0, []
    for entry in lex["words"] + lex["phrases"]:
        n = len(term_pattern(entry["find"]).findall(text))
        if n:
            hits += n
            found.append(entry["find"])
    density = hits * 100 / len(w)
    score = scale(density, human=0.0, machine=4.0)
    detail = f"{hits} términos de relleno, {density:.1f} por cada 100 palabras"
    if found:
        detail += " (" + ", ".join(sorted(found)[:4]) + (", ..." if len(found) > 4 else "") + ")"
    return score, detail


def check_fingerprint(text):
    """Caracteres que el teclado de un móvil no produce."""
    invisible = sum(1 for c in text if unicodedata.category(c) == "Cf")
    em = text.count("—")
    curly = sum(text.count(c) for c in "‘’“”«»")
    ellip = text.count("…")
    nbsp = sum(text.count(c) for c in "   ")
    total = invisible * 4 + em * 2 + curly + ellip + nbsp
    per1k = total * 1000 / max(len(text), 1)
    score = scale(per1k, human=0.0, machine=12.0)
    detail = (f"{invisible} invisibles, {em} rayas, {curly} comillas tipográficas, "
              f"{ellip} puntos suspensivos de un carácter, {nbsp} espacios duros")
    return score, detail


def check_voice(text, lex):
    """Coloquialidad, persona gramatical y las formas por defecto de los modelos."""
    w = words(text)
    if len(w) < 25:
        return 50.0, "demasiado corto para juzgar"
    per100 = 100 / len(w)
    colloquial = len(COLLOQUIAL.findall(text)) * per100
    person = person_hits(w) * per100
    tells = 0
    names = []
    for s in lex["structures"]:
        try:
            n = len(re.compile(s["regex"], re.MULTILINE).findall(text))
        except re.error:
            continue
        if n:
            tells += n
            names.append(s["id"])
    bullets = [len(b.split()) for b in re.findall(r"(?m)^\s*[-*•]\s+(.+)$", text)]
    uniform = (len(bullets) >= 3 and statistics.pstdev(bullets) < 1.6)
    score = (scale(colloquial, human=2.0, machine=0.0) * 0.30
             + scale(person, human=8.0, machine=1.0) * 0.40
             + clamp(100 - tells * 22) * 0.30)
    if uniform:
        score -= 12
        names.append("viñetas-uniformes")
    detail = (f"{colloquial:.1f} marcas coloquiales y {person:.1f} marcas de 1.ª/2.ª persona "
              f"por cada 100 palabras, {tells} señal(es) estructural(es)")
    if names:
        detail += " [" + ", ".join(names[:4]) + "]"
    return clamp(score), detail


CHECKS = ["VARIACIÓN", "CONCRECIÓN", "RELLENO", "HUELLA", "VOZ"]


def run(text, lex):
    results = {}
    results["VARIACIÓN"] = check_burstiness(text)
    results["CONCRECIÓN"] = check_specificity(text)
    results["RELLENO"] = check_slop(text, lex)
    results["HUELLA"] = check_fingerprint(text)
    results["VOZ"] = check_voice(text, lex)
    scores = [results[c][0] for c in CHECKS]
    # La comprobación más floja arrastra el veredicto: a un detector le basta una señal.
    overall = statistics.mean(scores) * 0.6 + min(scores) * 0.4
    verdict = "APTO" if overall >= 70 and min(scores) >= 55 else (
        "REVISAR" if overall >= 50 else "MARCADO")
    return results, overall, verdict


def bar(score, width=24):
    filled = round(score / 100 * width)
    return "#" * filled + "." * (width - filled)


def render(results, overall, verdict, label=None, out=sys.stdout):
    title = "PANEL DE DETECCIÓN" + (f"  -  {label}" if label else "")
    print("\n" + title, file=out)
    print("=" * max(len(title), 62), file=out)
    for name in CHECKS:
        score, detail = results[name]
        print(f"  {name:<13} {bar(score)} {score:5.1f}", file=out)
        print(f"  {'':<13} {detail}", file=out)
    print("-" * 62, file=out)
    print(f"  {'NOTA HUMANA':<13} {bar(overall)} {overall:5.1f}   {verdict}", file=out)
    if verdict != "APTO":
        weakest = min(CHECKS, key=lambda c: results[c][0])
        print(f"\n  Señal más floja: {weakest}. Arregla esa primero.", file=out)
    print("", file=out)


def main():
    ap = argparse.ArgumentParser(description="Puntúa cuánto parece escrito por máquina un borrador.")
    ap.add_argument("input", nargs="?", default="-", help="archivo, o - para stdin")
    ap.add_argument("compare", nargs="?", help="segundo archivo, para ver antes y después")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--lexicon", default=LEX)
    args = ap.parse_args()

    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except Exception:
            pass
    lex = json.load(open(args.lexicon, encoding="utf-8"))

    def read(p):
        if p == "-":
            sys.stdin.reconfigure(encoding="utf-8")
            return sys.stdin.read()
        return open(p, encoding="utf-8").read()

    targets = [(args.input, read(args.input))]
    if args.compare:
        targets.append((args.compare, read(args.compare)))

    payload = []
    for name, text in targets:
        results, overall, verdict = run(text, lex)
        payload.append({
            "source": name,
            "checks": {k: {"score": round(v[0], 1), "detail": v[1]} for k, v in results.items()},
            "human_score": round(overall, 1),
            "verdict": verdict,
        })

    if args.json:
        print(json.dumps(payload if args.compare else payload[0], indent=2, ensure_ascii=False))
        return

    for (name, text), p in zip(targets, payload):
        results, overall, verdict = run(text, lex)
        render(results, overall, verdict, label=os.path.basename(name) if args.compare else None)
    if args.compare:
        a, b = payload
        delta = b["human_score"] - a["human_score"]
        print(f"  {a['human_score']:.1f} {a['verdict']}  ->  "
              f"{b['human_score']:.1f} {b['verdict']}   ({delta:+.1f})\n")

    sys.exit(0 if payload[-1]["verdict"] == "APTO" else 1)


if __name__ == "__main__":
    main()
