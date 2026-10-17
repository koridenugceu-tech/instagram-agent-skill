#!/usr/bin/env python3
"""
humanize.py - quita la huella de máquina de un borrador en español.

Tres pasadas, en este orden:

  1. INVISIBLES  borra o normaliza los caracteres que un teclado humano no
                 produce: espacios de ancho cero, unidores, guiones blandos,
                 BOM, caracteres de etiqueta Unicode, espacios duros y finos.
                 Sobreviven al copiar y pegar y son la señal más mecánica de
                 cualquier texto generado.
  2. TIPOGRAFÍA  raya -> coma, semirraya -> guion, comillas inglesas y
                 angulares -> rectas, puntos suspensivos de un carácter ->
                 tres puntos, viñeta -> guion. Los signos de apertura ¿ y ¡
                 no se tocan: son ortografía, no huella.
  3. LÉXICO      sustituye el léxico de slop.json por palabras llanas,
                 respetando mayúsculas, ignorando tildes al buscar y sin tocar
                 las URL.

Las señales estructurales (tríadas, "no es solo X, es Y", muros de hashtags)
se SEÑALAN, nunca se reescriben solas: cambiar la forma de una frase pide
criterio, y eso es trabajo del modelo, no de una regex.

Uso
  python3 humanize.py borrador.txt
  python3 humanize.py borrador.txt --report
  pbpaste | python3 humanize.py - --report
  python3 humanize.py borrador.txt --json
  python3 humanize.py borrador.txt -o limpio.txt
"""

import argparse
import json
import os
import re
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
LEX = os.path.join(HERE, "slop.json")

URL_RE = re.compile(r"https?://\S+|www\.\S+|\S+@\S+\.\S+")
SENT_RE = re.compile(r"[^.!?\n]+[.!?]*")
LETTER = r"[^\W\d_]"
# Las tildes se ignoran al buscar: mucha gente escribe sin ellas en el móvil.
# La eñe no, porque "año" y "ano" no son la misma palabra.
FOLD = {"a": "[aá]", "e": "[eé]", "i": "[ií]", "o": "[oó]", "u": "[uúü]",
        "á": "[aá]", "é": "[eé]", "í": "[ií]", "ó": "[oó]", "ú": "[uúü]", "ü": "[uúü]"}


def load_lexicon(path=LEX):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def term_pattern(find):
    """Regex para un término del léxico: sin tildes, espacios flexibles y
    límites que funcionan también cuando el término empieza por ¿ o ¡."""
    body = "".join(FOLD.get(c, re.escape(c)) if c != " " else r"\s+" for c in find.lower())
    return re.compile(r"(?<!\w)" + body + r"(?!\w)", re.IGNORECASE)


def _cp(spec):
    """'U+200B' -> 0x200b;  'U+E0000-U+E007F' -> (inicio, fin)."""
    if "-" in spec:
        a, b = spec.split("-")
        return (int(a[2:], 16), int(b[2:], 16))
    return int(spec[2:], 16)


def protect_urls(text):
    """Cambia las URL por marcadores para que ninguna pasada reescriba un enlace."""
    found = []

    def stash(m):
        found.append(m.group(0))
        return f"\x00URL{len(found) - 1}\x00"

    return URL_RE.sub(stash, text), found


def restore_urls(text, found):
    for i, url in enumerate(found):
        text = text.replace(f"\x00URL{i}\x00", url)
    return text


def pass_invisible(text, lex):
    """Borra o convierte en espacio los caracteres invisibles. Devuelve (texto, hits)."""
    hits = []
    for entry in lex["invisible"]:
        cp = _cp(entry["cp"])
        if isinstance(cp, tuple):
            pattern = "[" + re.escape(chr(cp[0])) + "-" + re.escape(chr(cp[1])) + "]"
        else:
            pattern = re.escape(chr(cp))
        n = len(re.findall(pattern, text))
        if n:
            hits.append({"name": entry["cp"] + " " + entry["name"], "count": n,
                         "action": "borrar" if entry["action"] == "delete" else "espacio"})
            text = re.sub(pattern, "" if entry["action"] == "delete" else " ", text)
    # Cualquier otro carácter Cf (de formato) es invisible por definición.
    stray = [c for c in text if unicodedata.category(c) == "Cf"]
    if stray:
        hits.append({"name": "otros caracteres de formato invisibles", "count": len(stray),
                     "action": "borrar"})
        text = "".join(c for c in text if unicodedata.category(c) != "Cf")
    return text, hits


def pass_typographic(text, lex):
    hits = []
    for entry in lex["typographic"]:
        ch = entry["from"]
        n = text.count(ch)
        if not n:
            continue
        hits.append({"name": f"{ch} {entry['name']}", "count": n,
                     "to": entry["to"].strip() or "(espacio)"})
        if ch == "—":
            # La raya que abre un turno de diálogo, a principio de línea, se
            # quita. El inciso a la española ("palabra —inciso— palabra") o a
            # la inglesa ("palabra — palabra") acaba en coma. Nunca se come un
            # salto de línea.
            text = re.sub(r"(?m)^([ 	]*)—[ 	]*", r"", text)
            text = re.sub(r"[ 	]*—[ 	]*", ", ", text)
        elif ch == "–":
            text = re.sub(r"[ 	]*–[ 	]*(?=\d)", "-", text)  # 5–10  -> 5-10
            text = re.sub(r"(?m)^([ 	]*)–[ 	]*", r"", text)
            text = re.sub(r"[ 	]+–[ 	]+", ", ", text)        # usada como raya
            text = text.replace("–", "-")
        else:
            text = text.replace(ch, entry["to"])
    # Una coma metida delante de otro signo queda mal. Una raya que abría un
    # diálogo al principio de línea tampoco debe dejar una coma huérfana.
    text = re.sub(r",\s*([,.;:!?])", r"\1", text)
    text = re.sub(r",\s*\n", "\n", text)
    text = re.sub(r"(?m)^[ \t]*,\s*", "", text)
    return text, hits


def _match_case(src, repl):
    if not repl:
        return repl
    letters = [c for c in src if c.isalpha()]
    if len(letters) > 1 and all(c.isupper() for c in letters):
        return repl.upper()
    if letters and letters[0].isupper():
        i = next(k for k, c in enumerate(repl) if c.isalpha()) if any(
            c.isalpha() for c in repl) else 0
        return repl[:i] + repl[i].upper() + repl[i + 1:]
    return repl


def pass_lexical(text, lex):
    """Sustituye palabras y frases del léxico. Primero las más largas, para que ganen las frases."""
    hits = []
    entries = sorted(lex["phrases"] + lex["words"],
                     key=lambda e: len(e["find"]), reverse=True)
    for entry in entries:
        pattern = term_pattern(entry["find"])
        found = pattern.findall(text)
        if not found:
            continue
        hits.append({"find": entry["find"], "replace": entry["replace"] or "(borrado)",
                     "count": len(found), "family": entry["family"]})
        text = pattern.sub(lambda m: _match_case(m.group(0), entry["replace"]), text)
    # Limpieza tras los borrados. Quitar una oración entera deja puntuación
    # huérfana ("sistema. ." o una línea que ahora empieza por coma), y eso
    # se lee peor que el slop.
    text = re.sub(r"[ \t]{2,}", " ", text)
    text = re.sub(r"¿\s*\?|¡\s*!", "", text)           # signos que se quedaron vacíos
    text = re.sub(r"(?m)^[ \t]*(?:[,.;:]+[ \t]*)+", "", text)
    text = re.sub(r"(?m)^[ \t](?=\S)", "", text)       # un espacio que dejó un borrado.
                                                      # Las sangrías más hondas son a propósito.
    text = re.sub(r"\s+([,.;:!?])", r"\1", text)
    text = re.sub(r"([¿¡])\s+", r"\1", text)
    text = re.sub(r",\s*([,.;:!?])", r"\1", text)      # una raya pasó a coma y luego
                                                      # se fue la oración que venía detrás
    text = text.replace("...", "\x00ELL\x00")          # proteger los puntos suspensivos reales
    text = re.sub(r"\.\s*\.+", ".", text)
    text = re.sub(r"([!?])\s*\.", r"\1", text)
    text = text.replace("\x00ELL\x00", "...")
    text = re.sub(r"(?m)^[ \t]+$", "", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    # Una raya convertida en coma seguida de un conector deja una coma
    # empalmada ("es importante, además, es una prueba"). Pásala a punto.
    text = re.sub(r",\s*(también|así que|aun así|en el fondo|al final)\s*,\s*",
                  lambda m: ". " + m.group(1)[0].upper() + m.group(1)[1:] + ", ", text)
    return text, hits


def scan_structures(text, lex):
    flags = []
    for s in lex["structures"]:
        try:
            pattern = re.compile(s["regex"], re.MULTILINE)
        except re.error:
            continue
        found = pattern.findall(text)
        if found:
            flags.append({"name": s["name"], "count": len(found), "fix": s["fix"]})
    # La uniformidad en la longitud de las frases también es estructural.
    lens = [len(s.split()) for s in SENT_RE.findall(text) if len(s.split()) > 2]
    if len(lens) >= 4:
        mean = sum(lens) / len(lens)
        var = sum((n - mean) ** 2 for n in lens) / len(lens)
        cv = (var ** 0.5) / mean if mean else 0
        if cv < 0.35:
            flags.append({
                "name": f"Frases de longitud uniforme (variación {cv:.2f})",
                "count": len(lens),
                "fix": "Parte una frase por la mitad. Deja que otra se alargue. Las máquinas escriben parejo.",
            })
    return flags


START = r"(?:^|(?<=[.!?] )|(?<=[.!?]\n)|(?<=\n))(\s*[¿¡\"]?)(" + LETTER + ")"


def restore_capitals(original, text):
    """Borrar una apertura deja la siguiente palabra en minúscula.

    Solo se arregla para quien empieza sus frases con mayúscula: una voz en
    minúsculas a propósito es un estilo, no un artefacto, y pisarla sería
    justo lo que este script existe para evitar. Cuenta el ¿ y el ¡ como
    parte del inicio de frase, así que "¿qué" pasa a "¿Qué".
    """
    starts = [m.group(2) for m in re.finditer(START, original, re.MULTILINE)]
    if not starts or sum(1 for c in starts if c.isupper()) * 2 < len(starts):
        return text
    return re.sub(START, lambda m: m.group(1) + m.group(2).upper(), text, flags=re.MULTILINE)


def humanize(text, lex):
    raw_for_case = text
    text, urls = protect_urls(text)
    text, inv = pass_invisible(text, lex)
    text, typo = pass_typographic(text, lex)
    text, lexi = pass_lexical(text, lex)
    text = restore_capitals(raw_for_case, text)
    text = restore_urls(text, urls)
    return text.strip() + "\n", {
        "invisible": inv,
        "typographic": typo,
        "lexical": lexi,
        "structures": scan_structures(text, lex),
    }


def render_report(report, out=sys.stderr):
    def head(title):
        print(f"\n{title}\n" + "-" * len(title), file=out)

    total = sum(h["count"] for h in report["invisible"]) \
        + sum(h["count"] for h in report["typographic"]) \
        + sum(h["count"] for h in report["lexical"])

    head("INFORME DEL HUMANIZADOR")
    print(f"{total} artefactos de máquina eliminados, "
          f"{len(report['structures'])} señales estructurales para reescribir", file=out)

    if report["invisible"]:
        head("1. CARACTERES INVISIBLES")
        for h in report["invisible"]:
            print(f"  {h['count']:>3}x  {h['name']}  -> {h['action']}", file=out)
    if report["typographic"]:
        head("2. TIPOGRAFÍA")
        for h in report["typographic"]:
            print(f"  {h['count']:>3}x  {h['name']}  -> {h['to']}", file=out)
    if report["lexical"]:
        head("3. LÉXICO DE RELLENO")
        for h in report["lexical"]:
            print(f"  {h['count']:>3}x  {h['find']}  -> {h['replace']}   [{h['family']}]", file=out)
    if report["structures"]:
        head("4. SEÑALES ESTRUCTURALES  (no se arreglan solas: reescríbelas tú)")
        for h in report["structures"]:
            print(f"  {h['count']:>3}x  {h['name']}\n        {h['fix']}", file=out)
    if not any(report.values()):
        head("LIMPIO")
        print("  No hay nada que quitar.", file=out)
    print("", file=out)


def main():
    ap = argparse.ArgumentParser(description="Quita la huella de máquina de un borrador en español.")
    ap.add_argument("input", nargs="?", default="-", help="archivo, o - para stdin")
    ap.add_argument("-o", "--out", help="escribe aquí el texto limpio en vez de en stdout")
    ap.add_argument("--report", action="store_true", help="muestra qué cambió, por stderr")
    ap.add_argument("--json", action="store_true", help="emite {text, report} en JSON")
    ap.add_argument("--lexicon", default=LEX, help="ruta a slop.json")
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
    lex = load_lexicon(args.lexicon)
    clean, report = humanize(raw, lex)

    if args.json:
        print(json.dumps({"text": clean, "report": report}, indent=2, ensure_ascii=False))
        return
    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(clean)
        print(f"escrito {args.out}", file=sys.stderr)
    else:
        sys.stdout.write(clean)
    if args.report:
        render_report(report)


if __name__ == "__main__":
    main()
