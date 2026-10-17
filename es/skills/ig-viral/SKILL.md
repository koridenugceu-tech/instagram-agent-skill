---
name: ig-viral
description: >-
  Busca los reels que de verdad están funcionando ahora mismo en el nicho del
  usuario, los ordena según cuánto superaron a su propia cuenta, nombra la
  fórmula de gancho de cada uno y lo convierte en un archivo de referencias
  del que se puede grabar. Úsala cuando el usuario diga "busca vídeos
  virales", "qué está funcionando", "qué publica la gente de mi nicho",
  "analiza esta cuenta", "hazme un swipe file", "por qué este reel está
  petándolo", o pregunte qué hacer ahora sin pruebas con las que responder.
---

# ig-viral

La skill de investigación. Todo lo demás del pack escribe; esta va y mira.
Úsala una vez al mes, no a diario. Las fórmulas duran una temporada.

En esta carpeta vive una herramienta y funciona:

```bash
python3 swipe.py recogidos.tsv --out ~/.claude/instagram/swipe.md
```

## La única idea que hace que merezca la pena

**Las vistas en bruto no son una prueba.** Una cuenta con dos millones de
seguidores que hace 400.000 vistas tuvo un martes flojo. Una cuenta con cuatro
mil seguidores que hace 400.000 vistas encontró algo, y ese algo se puede
copiar.

Así que todo aquí se ordena por el **múltiplo**: vistas divididas por la
mediana reciente de esa misma cuenta. Por encima de 3x es una señal. Por debajo
de 1,5x es un día normal de esa cuenta y no enseña nada, por grande que parezca
el número.

Recoge cuentas **de hasta unas 10 veces el tamaño del usuario**. Una fórmula
que funciona con 2 millones de seguidores muchas veces funciona porque tiene 2
millones de seguidores.

## Paso 1: elige las cuentas

Pide al usuario entre 6 y 12 cuentas, o propónselas y que las apruebe:

- **4 directas**: mismo nicho, misma oferta, un poco por delante.
- **4 vecinas**: otro nicho, mismo público. De aquí se toman los formatos antes
  de que los tenga nadie del nicho.
- **De 2 a 4 enormes**: cuentas mucho más grandes, solo para el formato, nunca
  para el ritmo de publicación ni el tono.

Un apunte propio del español: **mira también cuentas en inglés del mismo
nicho.** Muchos formatos llegan al mercado hispano con meses de retraso, y ese
retraso es una ventaja si lo adaptas (no lo traduces) antes que los demás.

Pide también que abra su colección de **Guardados**. Es el corpus más rápido y
relevante que existe, y ya viene filtrado por su gusto.

## Paso 2: ve a mirar

Usa la herramienta de navegación que tenga de verdad esta sesión: un navegador
integrado, una extensión conectada al Chrome del propio usuario, o una
herramienta de uso del ordenador. No hay API para esto y no hace falta, porque
el volumen es lo bastante pequeño como para leerlo.

**Reglas que no se negocian:**

- **Nunca inicies sesión en Instagram en nombre del usuario y nunca pidas una
  contraseña.** Si una página pide login, quien ya tiene la sesión iniciada es
  el usuario. Maneja su navegador con él delante, o pídele que pegue los datos.
- **Esto es leer, no hacer scraping.** Diez cuentas, una docena de reels cada
  una, a velocidad humana. La recogida automatizada a volumen incumple las
  Condiciones de uso de Instagram y hace que bloqueen cuentas. No construyas un
  crawler, no uses un servicio de scraping y no lo dejes en bucle en segundo
  plano.
- **Copia la fórmula, nunca el vídeo.** La forma del gancho, la estructura, la
  duración, el patrón de cortes. No su guion, ni su voz, ni su edición.
  Atribuye cada fila del archivo a la cuenta de la que salió.

**Qué recoger de cada reel**, con las palabras del creador:

| campo | notas |
| --- | --- |
| cuenta | el @ |
| seguidores | del perfil |
| mediana | mira los últimos 12 reels y quédate con las vistas del del medio |
| vistas | las de este reel |
| gancho | la primera frase, dicha o en pantalla, literal, con faltas incluidas |
| pantalla | el primer rótulo, si es distinto |
| duración | segundos |
| cta | qué pidieron al final |

La mediana es la importante. Sin ella vuelves a ordenar por seguidores, que es
justo lo que esta skill existe para evitar.

**Cuando Instagram no te deja ver lo suficiente:** la misma gramática de
gancho funciona en YouTube Shorts, donde las vistas y las transcripciones son
públicas y no hace falta iniciar sesión. Es un segundo corpus legítimo, y el
gancho hablado es más fácil de sacar:

```bash
# vistas de los shorts de un canal
python3 -m yt_dlp --flat-playlist --playlist-end 40 -J \
  "https://www.youtube.com/@CANAL/shorts" > canal.json

# la primera frase hablada de un short, de sus subtítulos automáticos en español
python3 -m yt_dlp --skip-download --write-auto-subs --sub-langs "es.*" \
  --sub-format json3 -o gancho "https://www.youtube.com/watch?v=ID_DEL_VIDEO"
```

Quédate con cada palabra de los subtítulos con marca de tiempo por debajo de
3,0 segundos. Ese es el gancho, como se dijo, no como se escribió. Los
subtítulos automáticos en español fallan más con nombres propios y cifras:
revísalos contra el vídeo.

## Paso 3: ordénalo

Rellena un archivo separado por tabuladores con una fila de cabecera (vale en
español o en inglés) y ejecuta el script:

```
cuenta	seguidores	mediana	vistas	gancho
@alguien	48000	11000	412000	nadie te cuenta que tus primeros 30 reels tienen que fracasar
```

```bash
python3 swipe.py recogidos.tsv --out ~/.claude/instagram/swipe.md
```

Calcula el múltiplo, nombra la fórmula de gancho con las mismas 26 fórmulas de
las que escribe `/ig-reel`, puntúa cada gancho con `hookscore.py` e imprime qué
separa el tercio de arriba del de abajo.

## Paso 4: di qué significa, con cuidado

Informa de tres cosas y nada más:

1. **Qué fórmulas están sobrerrepresentadas** en el tercio de arriba, con
   recuento. Dos fórmulas que aparecen cuatro veces cada una en seis cuentas es
   un hallazgo. Una que aparece dos veces, no.
2. **Qué tienen en común estructuralmente** las de arriba que no tengan las de
   abajo: longitud del gancho, si la recompensa es visual, si el primer plano
   se mueve, dónde está la petición.
3. **Las filas sin clasificar.** Cada gancho que el clasificador no supo nombrar
   es ruido o una fórmula que aún no está en `hooks.json`. Léelos a mano. Es la
   columna más valiosa de la salida y por eso el script imprime el recuento. En
   esta variante cuenta doble: las regex de `hooks.json` en español todavía no
   se han contrastado con un corpus real, así que lo que salga aquí sirve para
   corregirlas.

Después di el tamaño de la muestra y la confianza con palabras normales.
Cuarenta reels de seis cuentas sostienen una afirmación. Doce no, y decirlo es
la diferencia entre investigar y leer el horóscopo.

## Paso 5: conviértelo en algo que grabar

Para las tres fórmulas de arriba, escribe **la versión del usuario**: su
historia, su cifra, con la forma que está funcionando. Pásale cada una a
`/ig-reel` con el número de fórmula ya elegido.

Nunca devuelvas "haz un reel como este". Devuelve una frase de gancho que
pueda decir mañana.

## Salida

```
REFERENCIAS  ·  38 reels  ·  7 cuentas  ·  referencia: mediana de la cuenta

DESTACADOS (por encima de 3x)
  38,4x  gancho 86  #3  Nadie te cuenta   @cuenta_a    412.000  (mediana 10.700)
  11,2x  gancho 79  #9  Róbamelo          @cuenta_c    180.000  (mediana 16.100)
  ...

LO QUE ESTÁ SOBRERREPRESENTADO
  #3 Nadie te cuenta   x5 en el tercio de arriba, 0 en el de abajo
  #2 Orden negativa    x4
  longitud mediana del gancho   8 palabras arriba, 19 abajo

SIN CLASIFICAR (6)
  Dos tienen la misma forma y no está en hooks.json: un gancho que empieza
  leyendo en voz alta el comentario de otra persona. Merece entrar.

TU VERSIÓN
  #3  "Nadie te cuenta que las primeras 20 propuestas están para perderse."
  ...
```

Escribe el archivo en `~/.claude/instagram/swipe.md`. Lo leen `/ig-reel` y
`/ig-plan`, y esa es la gracia: después de ejecutarlo una vez, el resto del pack
trabaja con las pruebas del propio usuario en vez de con los valores por
defecto.

Esta skill no publica, no sigue, no da me gusta ni manda mensajes. Lee.
