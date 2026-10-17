---
name: ig-carousel
description: >-
  Monta un carrusel de Instagram en español: la portada que se gana el
  deslizamiento, el texto diapositiva a diapositiva y los archivos de
  1080x1350 para subir. Úsala cuando el usuario diga "carrusel",
  "diapositivas", "post para deslizar", "convierte esto en un carrusel", o
  tenga una idea en forma de lista o de pasos que moriría como imagen suelta.
---

# ig-carousel

Los carruseles son el formato con más tiempo de permanencia de la cuadrícula,
porque deslizar es una interacción y hacer scroll no. Además tienen una
segunda oportunidad: Instagram puede volver a enseñar un carrusel, empezando
por una diapositiva posterior, a quien no interactuó la primera vez, así que la
diapositiva dos también tiene que sostenerse sola.

El formato premia una idea partida en pasos. Castiga un caption cortado en
trozos.

## Cuándo usarlo en vez de un Reel

Usa un carrusel cuando la idea tiene **secuencia y hay que releerla**: pasos,
un método con partes, un antes y un después, una lista que merece captura. Usa
un Reel cuando la idea tiene movimiento, una cara o una recompensa que hay que
ver ocurrir.

Si la idea es una sola afirmación, no es ninguno de los dos. Pásasela a
`/ig-reel` y dilo.

## Estructura

De 6 a 10 diapositivas. El máximo es 20, y 20 casi siempre es un libro que
nadie termina. Por debajo de 5, el deslizamiento ni empieza.

```
1         PORTADA       el gancho. 6 palabras o menos, a un tamaño legible en
                        la cuadrícula en miniatura. Una línea de promesa debajo.
2         LO QUE ESTÁ EN JUEGO   por qué importa, en una frase. Esta diapositiva
                        también es una segunda portada, así que no puede ser preparación.
3 a N     UNA IDEA POR DIAPOSITIVA. Un titular de 3 a 7 palabras, como mucho
                        25 palabras debajo. Si necesita un párrafo, son dos diapositivas.
N+1       RESUMEN       todo como lista. Es la diapositiva de la captura.
ÚLTIMA    CTA           una acción. Guardar, comentar una palabra o seguir. Una.
```

## Reglas del texto

- **La portada es el 80 % del resultado.** Seis palabras. Grandes. Nada del
  resto salva una portada que nadie desliza. En español cuesta más caber en
  seis: quita artículos, usa cifras en vez de palabras ("5 ERRORES", no "CINCO
  DE LOS ERRORES").
- **Mayúscula solo donde toca.** "Cómo cobrar más sin perder clientes", no
  "Cómo Cobrar Más Sin Perder Clientes". Las mayúsculas a la inglesa suenan a
  traducción.
- **Diseña para el recorte de la cuadrícula.** La cuadrícula del perfil recorta
  a un rectángulo vertical, y la proporción exacta ha cambiado más de una vez.
  Monta a 1080x1350 y deja el texto de la portada bien en el centro, lejos de
  los 120 píxeles exteriores de cada lado, y el recorte deja de importar.
- **Numera las diapositivas** (3/8). La gente termina más cuando ve el final.
- **Ninguna diapositiva es un párrafo.** Si no cabe en 25 palabras, pártela.
- **El resumen es la que se captura y se envía.** Los envíos son la señal más
  fuerte que puedes ganar. Que se entienda sola, sin contexto.
- **El @ en todas las diapositivas**, pequeño, en una esquina de abajo. Las
  capturas viajan sin ti.
- **Texto alternativo al menos en la portada.** Lo leen los lectores de
  pantalla y lo lee Instagram.

## Montar los archivos

Instagram quiere 1080x1350 (4:5), JPEG o PNG, hasta 20 elementos. Móntalo en
HTML e imprime cada diapositiva:

```bash
# un <section> por diapositiva, 1080x1350, page-break-after: always
# y luego Chrome headless --print-to-pdf, o el HTML-a-imagen que ya uses
```

Escribe el HTML con `width:1080px; height:1350px`, un solo color de acento y
letra de 32px como mínimo, porque se lee en un móvil a un tercio de su tamaño
real. Usa una fuente que tenga bien la ñ, las tildes y los signos ¿ ¡ (muchas
fuentes de titulares los dibujan mal o no los tienen). Si el proyecto tiene una
skill de marca o un sistema de diseño, úsalo y no te inventes una paleta.

## Salida

Primero el texto diapositiva a diapositiva, como lista numerada que el usuario
pueda leer en diez segundos y editar antes de renderizar nada. Después el
**caption**, que en un carrusel es el Trabajo B de `/ig-caption`: aquí el
caption trabaja, porque la portada ya gastó sus seis palabras.

Pasa las dos cosas por `/ig-human`. Monta los archivos solo cuando el usuario
apruebe el texto.

```
CARRUSEL  ·  8 diapositivas

1  PORTADA  LA CLÁUSULA DE 18.000 €
            Una línea que ahora pongo en todos mis contratos.
2  JUEGO    Aprobé el trabajo. Nueve días después pidieron el dinero de vuelta.
3           QUÉ DICE
            Pago a la entrega, no a la aprobación.
...
7  RESUMEN  Las cuatro líneas, en orden.
8  CTA      Comenta CONTRATO y te mando la cláusula entera.

Caption: Trabajo B, gancho en la línea 1, una petición, 3 hashtags.
```

No se sube nada. El usuario lo publica.
