#!/usr/bin/env python3
"""
beats.py - convierte el guion de un Reel en español en una escaleta con
tiempos antes de grabarlo.

Calcula cuánto se tarda en decir cada línea, las apila en códigos de tiempo y
señala las cuatro cosas que matan un Reel en la edición: un gancho que pasa de
los tres segundos, un bloque tan largo que da tiempo a irse, una racha de
líneas sin nada concreto y una duración que no cuadra con lo que dijiste que
ibas a hacer.

Los tiempos son una estimación por sílabas, no por palabras, porque en
español la longitud de las palabras varía mucho más que en inglés. Por
defecto, 6 sílabas por segundo; mídete leyendo un guion en voz alta y
ajústalo con --sps. Si prefieres pensar en palabras por minuto, --wpm calcula
por palabras como la versión inglesa.

Uso
  python3 beats.py guion.txt
  python3 beats.py guion.txt --target 30
  python3 beats.py guion.txt --sps 6.2 --target 45
  python3 beats.py guion.txt --wpm 170
  pbpaste | python3 beats.py -
  python3 beats.py guion.txt --json
"""

import argparse
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hookscore import SPS, syllables, words   # noqa: E402

SENT_RE = re.compile(r"[^.!?]+[.!?]*")
CONCRETE_RE = re.compile(r"[$€]\s?\d|\b\d[\d.,]*\b")
UPPER_WORD = re.compile(r"^[A-ZÁÉÍÓÚÑÜ][a-záéíóúñü]{2,}$")
CONCRETE_WORD = re.compile(
    r"^(?:cero|dos|tres|cuatro|cinco|seis|siete|ocho|nueve|diez|once|doce|quince|"
    r"dieci\w+|veinte|veinti\w+|treinta|cuarenta|cincuenta|sesenta|setenta|ochenta|"
    r"noventa|cien|ciento|\w+cientos|mil|millón|millones|euros?|dólar(?:es)?|pesos|"
    r"enero|febrero|marzo|abril|mayo|junio|julio|agosto|septiembre|octubre|"
    r"noviembre|diciembre|lunes|martes|miércoles|jueves|viernes|sábado|domingo)$")
STOPWORDS = {
    "el", "la", "los", "las", "un", "una", "unos", "unas", "y", "e", "o", "u", "pero",
    "si", "de", "del", "a", "al", "en", "con", "por", "para", "que", "qué", "esto",
    "este", "esta", "eso", "es", "son", "era", "fue", "ser", "estar", "está", "lo",
    "le", "les", "se", "te", "tu", "tú", "yo", "mi", "me", "nos", "su", "sus", "ya",
    "no", "sí", "muy", "más", "como", "cómo", "hay", "he", "ha", "han", "todo", "uno",
    "ni", "sin", "sobre", "entre", "hasta", "desde", "cuando", "porque", "así",
}

HOOK_WINDOW = 3.0        # segundos. Pasado esto, el pulgar ya ha decidido.
MAX_BEAT = 4.0           # segundos con una sola idea y nada que cambie en pantalla.
ABSTRACT_RUN = 3         # bloques seguidos sin nada comprobable.


def concrete(text):
    toks = re.findall(r"[^\W\d_]+", text)
    n = len(CONCRETE_RE.findall(text))
    n += sum(1 for t in toks[1:] if UPPER_WORD.match(t))
    n += sum(1 for t in toks if CONCRETE_WORD.match(t.lower()))
    return n


def pretty(token):
    """Vuelve a poner el punto de los miles para mostrarlo."""
    return re.sub(r"(\d)(?=(\d{3})+$)", r"\1.", token) if token.isdigit() else token


def tc(seconds):
    m, s = divmod(seconds, 60)
    return f"{int(m)}:{s:04.1f}".replace(".", ",")


class Clock:
    """Duración de una línea: por sílabas (por defecto) o por palabras (--wpm)."""

    def __init__(self, sps=SPS, wpm=None):
        self.sps, self.wpm = sps, wpm

    def secs(self, text):
        w = words(text)
        if self.wpm:
            return len(w) / (self.wpm / 60.0)
        return sum(syllables(t) for t in w) / self.sps

    def units(self, seconds):
        """Cuántas palabras caben en `seconds`, para dar consejos en palabras."""
        if self.wpm:
            return int(seconds * self.wpm / 60.0)
        return int(seconds * self.sps / 2.3)        # ~2,3 sílabas por palabra en español

    def label(self):
        return f"{self.wpm:g} ppm" if self.wpm else f"{self.sps:g} síl/s".replace(".", ",")


def split_beats(raw, clock):
    """Una línea es un bloque, salvo que sea demasiado larga para serlo."""
    beats = []
    for line in [l.strip() for l in raw.splitlines()]:
        if not line:
            continue
        if clock.secs(line) <= MAX_BEAT * 1.5:
            beats.append(line)
            continue
        # Párrafo largo: se parte por los finales de frase para que los
        # tiempos signifiquen algo, y el informe dice que se partió.
        parts = [p.strip() for p in SENT_RE.findall(line) if p.strip()]
        buf = ""
        for part in parts:
            candidate = (buf + " " + part).strip()
            if buf and clock.secs(candidate) > MAX_BEAT:
                beats.append(buf)
                buf = part
            else:
                buf = candidate
        if buf:
            beats.append(buf)
    return beats


def fmt(x):
    return f"{x:.1f}".replace(".", ",")


def analyse(raw, sps=SPS, wpm=None, target=None):
    clock = Clock(sps, wpm)
    beats = split_beats(raw, clock)
    if not beats:
        return None

    rows, t = [], 0.0
    for i, text in enumerate(beats):
        dur = clock.secs(text)
        rows.append({
            "n": i + 1,
            "start": round(t, 2),
            "dur": round(dur, 2),
            "words": len(words(text)),
            "syllables": sum(syllables(x) for x in words(text)),
            "text": text,
            "concrete": concrete(text),
            "label": "",
            "flags": [],
        })
        t += dur
    total = t

    # Etiqueta las posiciones sobre las que se construye un Reel.
    for r in rows:
        if r["n"] == 1 or r["start"] + r["dur"] <= HOOK_WINDOW:
            r["label"] = "GANCHO"
    rows[-1]["label"] = "CTA" if rows[-1]["label"] != "GANCHO" else "GANCHO/CTA"
    half = total / 2
    for r in rows:
        if not r["label"] and r["start"] <= half < r["start"] + r["dur"]:
            r["label"] = "MITAD"

    notes = []
    if rows[0]["dur"] > HOOK_WINDOW:
        rows[0]["flags"].append(f"el gancho dura {fmt(rows[0]['dur'])}s, pasa de los "
                                f"{HOOK_WINDOW:.0f}s")
        notes.append(f"El bloque 1 tarda {fmt(rows[0]['dur'])}s en decirse. Déjalo en unas "
                     f"{clock.units(HOOK_WINDOW)} palabras, o el gancho llega cuando la "
                     "decisión ya está tomada.")
    if rows[0]["concrete"] == 0:
        notes.append("El bloque 1 no tiene ni una cifra ni un nombre. Los ganchos sin nada "
                     "comprobable son los que se pasan de largo.")

    for r in rows:
        if r["dur"] > MAX_BEAT:
            r["flags"].append(f"{fmt(r['dur'])}s en un solo bloque")
    long_beats = [r["n"] for r in rows if r["dur"] > MAX_BEAT]
    if long_beats:
        notes.append(f"El/los bloque(s) {', '.join(map(str, long_beats))} pasan de "
                     f"{MAX_BEAT:.0f}s. Parte la línea o cambia lo que hay en pantalla dentro "
                     "de ella. Un plano quieto es donde la gente se va.")

    run, start = 0, None
    for r in rows:
        if r["concrete"] == 0:
            run += 1
            start = start if start is not None else r["n"]
            if run == ABSTRACT_RUN:
                notes.append(f"Los bloques {start}-{r['n']} no tienen nada concreto. Mete una "
                             "cifra, un nombre o un precio en alguno.")
        else:
            run, start = 0, None

    # ¿La última línea te devuelve a la primera?
    def key(text):
        return {re.sub(r"[.,](?=\d{3})", "", w.lower()) for w in words(text)
                if w.lower() not in STOPWORDS and w not in "€$%"}
    loop = sorted(pretty(w) for w in key(rows[0]["text"]) & key(rows[-1]["text"]))
    if loop:
        notes.append(f"Bucle: el último bloque repite \"{', '.join(loop[:3])}\" del gancho. "
                     "Las segundas vistas son alcance gratis.")
    else:
        notes.append("Sin bucle. El último bloque no comparte ninguna palabra con el gancho, "
                     "así que el vídeo acaba plano. Repetir una palabra del bloque 1 es la "
                     "segunda vista más barata que vas a conseguir.")

    if target:
        delta = total - target
        if abs(delta) <= target * 0.1:
            notes.append(f"La duración cuadra ({fmt(total)}s frente a {target:g}s).")
        elif delta > 0:
            notes.append(f"{fmt(delta)}s por encima del objetivo. Quita unas "
                         f"{clock.units(delta)} palabras.")
        else:
            notes.append(f"{fmt(-delta)}s por debajo del objetivo. Añade unas "
                         f"{clock.units(-delta)} palabras o grábalo más corto. Más corto "
                         "suele ser lo correcto.")

    return {
        "rate": clock.label(), "target": target,
        "total_seconds": round(total, 2),
        "total_words": sum(r["words"] for r in rows),
        "total_syllables": sum(r["syllables"] for r in rows),
        "beats": rows,
        "notes": notes,
    }


def render(a, out=sys.stdout):
    head = (f"ESCALETA  ·  {a['total_words']} palabras, {a['total_syllables']} sílabas  ·  "
            f"~{fmt(a['total_seconds'])}s a {a['rate']}"
            + (f"  ·  objetivo {a['target']:g}s" if a["target"] else ""))
    print("\n" + head, file=out)
    print("=" * max(len(head), 72), file=out)
    for r in a["beats"]:
        label = f"{r['label']:<11}" if r["label"] else " " * 11
        print(f"  {tc(r['start'])}  {fmt(r['dur']):>4}s  {label}{r['text']}", file=out)
        for f in r["flags"]:
            print(f"  {'':>6}  {'':>5}  {'':<11}^ {f}", file=out)
    print("-" * max(len(head), 72), file=out)
    for n in a["notes"]:
        print(f"  - {n}", file=out)
    print("", file=out)


def main():
    ap = argparse.ArgumentParser(description="Convierte un guion de Reel en una escaleta con tiempos.")
    ap.add_argument("input", nargs="?", default="-", help="archivo del guion, o - para stdin")
    ap.add_argument("--sps", type=float, default=SPS,
                    help=f"sílabas por segundo al hablar (por defecto {SPS})")
    ap.add_argument("--wpm", type=float, help="calcula por palabras por minuto en vez de por sílabas")
    ap.add_argument("--target", type=float, help="duración objetivo en segundos")
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
    a = analyse(raw, sps=args.sps, wpm=args.wpm, target=args.target)
    if not a:
        print("guion vacío", file=sys.stderr)
        sys.exit(2)
    if args.json:
        print(json.dumps(a, indent=2, ensure_ascii=False))
    else:
        render(a)
    sys.exit(0)


if __name__ == "__main__":
    main()
