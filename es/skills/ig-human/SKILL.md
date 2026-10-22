---
name: ig-human
description: >-
  Quita la huella de máquina de cualquier borrador en español (rayas, léxico de
  relleno típico de la IA, calcos del inglés, comillas angulares, caracteres
  invisibles) y lo puntúa con un panel de cinco comprobaciones antes de que
  salga. Úsala siempre que un texto tenga que sonar humano, cuando el usuario
  diga humaniza, "¿esto suena a IA?", "quita las rayas", "esto suena a
  ChatGPT", "límpialo", o antes de enseñarle cualquier caption, guion,
  comentario, respuesta o DM.
---

# ig-human

En esta carpeta viven dos herramientas y las dos funcionan de verdad. Úsalas.
No lo hagas a ojo.

```bash
python3 humanize.py borrador.txt --report        # límpialo y enseña qué cambió
python3 detect.py borrador.txt                    # puntúalo, cinco comprobaciones
python3 detect.py antes.txt despues.txt           # demuestra la diferencia
```

Las dos leen `slop.json`: 266 palabras y expresiones de relleno con su
reemplazo en español llano, 18 clases de caracteres invisibles, 12
sustituciones tipográficas y 19 señales estructurales. Está pensado para
editarse. Si el usuario tiene una palabra que usa siempre y el léxico se la
quita, sácala del archivo.

## Qué cambia respecto a la versión inglesa

El español de máquina no falla en lo mismo que el inglés de máquina, así que
esto no es una traducción del léxico sino uno nuevo:

- **Género y número.** "Robusto" no se puede cambiar por "sólido" sin mirar a
  qué acompaña. Cada forma (robusto, robusta, robustos, robustas) tiene su
  entrada y su reemplazo concordado.
- **Tildes.** La búsqueda ignora las tildes (no la eñe), porque en el móvil
  mucha gente escribe sin ellas.
- **Calcos del inglés.** "Al final del día", "hace sentido", "mover la aguja",
  "poco sabía yo", "corre, no camines". Son la señal más clara de un texto
  escrito en inglés y pasado por máquina.
- **Signos de apertura.** El ¿ y el ¡ no se tocan, son ortografía. Si un
  borrado deja un "¿?" vacío, se limpia, y la mayúscula se recupera también
  detrás del ¿ ("¿qué" pasa a "¿Qué").
- **Rayas y comillas angulares.** En un libro, "—inciso—" y «comillas» son
  correctos. En un caption de Instagram, escrito desde un móvil, delatan un
  texto que no se tecleó ahí.
- **Mayúsculas a la inglesa.** "Cómo Escribir Un Caption Que Vende" se señala:
  en español solo va en mayúscula la primera palabra.

**El humanizador no cambia de variante.** Si el usuario escribe "vídeo" o
"video", "vosotros" o "ustedes", "tenés" o "tienes", se respeta. Mira
`voice.md` antes de reescribir nada a mano.

## Por qué importa más en Instagram de lo que parece

Los captions son cortos y los guiones se dicen en voz alta. Una frase que
suena a escrita pesa más en un caption de 600 caracteres que en un ensayo, y
un guion que nadie diría de forma natural se nota en la primera toma. Aquí la
señal no es que un detector marque el post. Es que alguien pase de largo
porque suena a marca, o que el creador se trabe con su propio guion.

## Qué se arregla solo

**1. Caracteres invisibles.** Espacios de ancho cero y unidores, guiones
blandos, marcas de orden de bytes, caracteres de etiqueta Unicode,
separadores invisibles, espacios duros y finos. Un teclado no los produce.
Sobreviven al copiar y pegar, no se ven en ningún editor y son lo más mecánico
de un texto generado. `humanize.py` los borra todos, incluido cualquier otro
carácter de formato Unicode que no tenga nombrado.

**2. Tipografía.** Raya a coma, semirraya a guion, comillas inglesas y
angulares a rectas, puntos suspensivos de un carácter a tres puntos, viñeta a
guion. La pasada de la raya es la que importa: la convierte en coma y luego
limpia la puntuación doble y los puntos huérfanos que deja.

**3. El léxico de relleno.** adentrarse, potenciar, sumergirse, crucial,
robusto, sinergia, "en el mundo actual", "cabe destacar que", y el bloque de
Instagram: "deja de hacer scroll", "en el vídeo de hoy", "sígueme para más",
"etiqueta a alguien que necesite esto", "al algoritmo le encanta". Cada uno se
cambia por una palabra llana o se borra, respetando mayúsculas y sin tocar las
URL.

## Qué NO se arregla solo

Las señales estructurales se **señalan, no se reescriben**, porque cambiar la
forma de una frase pide criterio:

- "No es solo X, es Y", "no solo X, sino también Y" y "no se trata de X, se
  trata de Y"
- Tríadas: "rápido, sencillo y eficaz."
- Líneas de pregunta retórica: "¿El resultado?"
- El preámbulo de vídeo: "en este vídeo te voy a enseñar"
- Aperturas serviciales: "¡Claro!", "¡Excelente pregunta!"
- "¿Estás listo para...?"
- Listas con emojis como viñetas
- Tres o más palabras gritadas seguidas
- Muros de hashtags
- Cebos reflejos: "sígueme para", "etiqueta a alguien", "dale like si"
- Mayúsculas a la inglesa en los títulos

Esa lista es trabajo tuyo. Reescribe a mano cada línea señalada manteniendo el
sentido y vuelve a pasar `detect.py`. Esto es lo que lleva la nota de REVISAR a
APTO, y es lo que un script no puede hacer.

## Las cinco comprobaciones

`detect.py` puntúa cinco señales de 0 a 100, más alto es más humano:

| comprobación | qué mide | cómo se ve la máquina |
| --- | --- | --- |
| VARIACIÓN | variación en la longitud de las frases | todas las frases igual de largas |
| CONCRECIÓN | cifras, nombres, fechas y cantidades dichas con letra por cada 100 palabras | sustantivos abstractos, sin cifras |
| RELLENO | términos del léxico por cada 100 palabras | vocabulario de plantilla |
| HUELLA | invisibles, rayas, comillas tipográficas por cada 1.000 caracteres | tipografía perfecta |
| VOZ | marcas coloquiales, primera y segunda persona, señales estructurales | registro neutro, revelaciones escenificadas |

La VOZ es la que más cambia respecto al inglés. El español no tiene
contracciones, así que se mide con marcas coloquiales (pues, vale, o sea, en
plan, ¿no?, ¿sabes?). Y como el español omite el pronombre, la persona se
cuenta también por el verbo: "perdí", "llevas", "tenés".

El veredicto pesa la media al 60 % y la **comprobación más floja** al 40 %,
porque basta una señal. APTO pide una nota de 70 o más sin ninguna
comprobación por debajo de 55.

## Dilo con honestidad

Son cinco heurísticas locales basadas en las señales en las que se fijan los
detectores públicos. Se ejecutan enteras en la máquina del usuario y no se
sube nada. **No** son GPTZero, Originality, Copyleaks, Winston ni Turnitin, no
llaman a esas API y no pueden prometer su veredicto. Arreglar lo que miden
suele mover esos números, porque miden lo mismo de fondo. Esa es la
afirmación. No hagas una mayor en nombre del usuario y no le digas nunca que su
texto es indetectable.

Y una más, propia de esta variante: **los umbrales vienen de la versión
inglesa y, medidos con textos en español, separan a medias.** Contra 36
descripciones de YouTube escritas por personas antes de 2022 y 180 generadas
con el mismo encargo por cinco modelos, la nota da AUC 0,75. La IA sale
MARCADO el 77 % de las veces, pero las personas también, el 42 %, y solo 1
de los 36 textos humanos sale APTO. El detalle está en el README. Úsalo para encontrar qué
arreglar (la comprobación más floja, las palabras que lista), no como prueba
de que un texto parece humano, y no le digas al usuario que su texto "suena a
IA" por un MARCADO.

## Orden de trabajo

1. `humanize.py borrador.txt -o limpio.txt --report`
2. Lee las señales estructurales. Reescribe tú esas líneas.
3. `detect.py borrador.txt limpio.txt` para enseñar el antes y el después.
4. Si el veredicto no es APTO, arregla la comprobación más floja que diga la
   salida y repite. Dos rondas como mucho: casi ningún texto humano llega a
   APTO, así que perseguirlo solo deforma el borrador. Si tras dos rondas
   sigue lleno de relleno, se escribió por fórmula, y lo que hace falta es
   otro borrador, no más pasadas.
5. Enseña al usuario el texto limpio y la nota. Nunca la nota sola.
