---
name: ig-caption
description: >-
  Escribe el caption de Instagram en español (la línea que sobrevive al corte
  del "... más", el cuerpo, la única petición, los términos de búsqueda y los
  hashtags) y lo revisa antes de que salga. Úsala cuando el usuario diga
  "escribe el caption", "ponle texto a esto", "qué pongo en la descripción",
  tenga un reel o un carrusel listo y necesite el texto, o pregunte por
  hashtags.
---

# ig-caption

En esta carpeta vive una herramienta y funciona:

```bash
python3 caption.py caption.txt
python3 caption.py caption.txt --keywords "propuestas para clientes,precios de agencia"
```

Imprime el caption como lo imprime el feed: los primeros 125 caracteres en una
caja y todo lo demás detrás del toque. Lee esa caja antes que cualquier otra
cosa que hayas escrito.

El español necesita más caracteres que el inglés para decir lo mismo, así que
esos 125 se acaban antes. Escribe la primera línea pensando en 100.

## Primero, decide qué trabajo tiene este caption

Esta es la decisión que arruina captions cuando se salta.

**Trabajo A: el vídeo ya los enganchó.** Un Reel trae su propio gancho en los
dos primeros segundos, hablado y en pantalla. El caption no es un segundo
gancho, y competir con el vídeo es la forma de perder los dos. Su trabajo es la
petición, el contexto que hace que la petición tenga sentido, y las palabras
que la gente busca.

**Trabajo B: el caption es el contenido.** Una foto, una sola imagen, una
portada de carrusel que abre un bucle. Aquí la primera línea es el gancho y
funciona igual que el de un Reel: concreta, corta, y cortada en un momento de
intriga, no a media subordinada.

Pregunta cuál estás escribiendo. Si el usuario tiene un Reel con un gancho
fuerte, escribe el A y di por qué.

## La forma

```
Línea 1     125 caracteres visibles. Trabajo A: la petición, sin rodeos.
            Trabajo B: el gancho.
            Nunca un saludo, nunca un hashtag, nunca un emoji como primer carácter.
Cuerpo      párrafos cortos, con una línea en blanco entre cada uno. De dos a
            seis. Aquí viven los términos de búsqueda.
Petición    una. Comentar una palabra, guardar o escribir por DM. Una.
Hashtags    hasta cinco, en su propia línea al final, o ninguno.
```

El límite es de 2.200 caracteres y casi nada necesita 2.200. Un caption que se
gana el toque y luego entrega 600 caracteres gana a uno que entrega 1.800.

## Hashtags, con honestidad

Los hashtags ya no son una palanca de alcance, y la plataforma lo ha dicho con
un cambio de producto. **Instagram limitó los hashtags a cinco por publicación
el 18 de diciembre de 2025**, frente a los treinta de antes, y explicó a los
creadores que menos hashtags y más específicos funcionan mejor que muchos
genéricos. Adam Mosseri ya había dicho en febrero de 2025 que los hashtags no
sirven para aumentar el alcance y que son una etiqueta, no una vía de
distribución.

Así que: hasta cinco, específicos, como etiquetas de tema. Si el usuario tiene
un bloque de veinte guardado en las notas del móvil, ese bloque ya es peso
muerto y el revisor lo va a suspender.

`#viral`, `#parati`, `#fyp`, `#explorar`, `#megusta` no describen nada.
Fuera. Un hashtag en español puede llevar tildes y eñes (`#diseño`); decide
una forma y úsala siempre igual.

## Los términos de búsqueda importan más que los hashtags

El buscador de Instagram lee el texto del caption. Así que la frase por la que
el usuario quiere que le encuentren va en el caption, como la escribiría una
persona, en una frase que se lee normal. "Propuestas para clientes" como
palabras en la tercera línea, no "#propuestasparaclientes" en un bloque al
final.

Pide dos o tres de esos términos y pásaselos al revisor. Compara sin tildes,
así que "video" encuentra "vídeo":

```bash
python3 caption.py borrador.txt --keywords "propuestas para clientes,precios de agencia"
```

## Reglas

- **Sin enlaces en el caption.** No son clicables. Una URL en el texto es texto
  muerto que dice "no uso esta plataforma". A la bio o al DM.
- **Una petición.** Dos peticiones es lo mismo que ninguna. `caption.py` las
  cuenta.
- **La palabra clave tiene que poder escribirse.** Una palabra, sin espacios,
  sin emoji, mejor sin tilde (en el móvil la mitad de la gente no la pondrá), y
  dila también en el vídeo. `Comenta CONTRATO` funciona. `Comenta "la guía del
  contrato"` no.
- **Escribe aparte el primer comentario** si hay un enlace. Dilo en el
  resumen.
- **Emojis como puntuación, no como decoración.** El revisor avisa a partir de
  4 por cada 100 caracteres.
- **El texto alternativo vale 20 segundos.** En carruseles y fotos, escríbelo.
  Lo leen los lectores de pantalla y lo lee Instagram.

## El proceso

1. Decide Trabajo A o Trabajo B y dilo.
2. Escribe el borrador.
3. Pásalo por `/ig-human`. Los captions son cortos, así que el relleno se nota
   aquí más que en ningún otro sitio del pack.
4. Ejecuta `caption.py` con los términos de búsqueda del usuario. Arregla cada
   MAL. Decide en voz alta cada OJO en vez de callártelo.
5. Imprime el bloque listo para copiar y luego el resumen:

```
CAPTION LISTO
trabajo:    A - el reel lleva el gancho
visible:    118 de 125 caracteres antes del corte
petición:   una, comentar CONTRATO
hashtags:   3
búsqueda:   "propuestas para clientes" en la línea 3, "precios de agencia" en la 5
revisor:    LISTO
```

No se publica nada. El usuario lo pega.
