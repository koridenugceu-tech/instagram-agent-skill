---
name: ig-repurpose
description: >-
  Convierte un contenido largo (un vídeo de YouTube, un pódcast, un directo,
  una newsletter, un artículo o una llamada con un cliente) en una semana de
  reels y carruseles en español. Úsala cuando el usuario diga "reutiliza
  esto", "sácame reels de aquí", "tengo un vídeo/pódcast/transcripción",
  "trocea esto", o pegue algo largo y lo quiera en Instagram.
---

# ig-repurpose

Un buen contenido largo tiene dentro entre cuatro y seis posts. Casi todo el
mundo saca uno y tira el resto.

## Entrada

Una transcripción, un artículo, una newsletter, un guion, el resumen de una
llamada, un directo. Si el usuario da una URL y esta sesión tiene una
herramienta de transcripción, úsala; si no, pídele que lo pegue. Léelo entero
antes de sacar nada.

Si el original es un vídeo del usuario, pide también el archivo. Un Reel
montado con su propio metraje gana a uno montado con sus propias palabras
leídas otra vez.

**Si el original está en inglés**, no lo traduzcas frase a frase. Saca las
ideas y escríbelas de nuevo en español, con la voz de `voice.md`. Una
traducción literal es exactamente lo que el humanizador está hecho para cazar
("al final del día", "hace sentido", "mover la aguja").

## Extrae, no resumas

El resumen de un vídeo no es un Reel. Nadie quiere el resumen. Recorre el
contenido y saca lo que se sostiene solo:

| qué sacar | qué es |
| --- | --- |
| **Afirmaciones** | cada frase que empezaría una discusión |
| **Cifras** | cada número, coste, duración, porcentaje |
| **Historias** | cada momento con una persona, una escena y un coste |
| **Mecanismos** | cada "esto en realidad funciona así..." |
| **Errores** | cada admisión de algo que salió mal |
| **Frases** | cada frase que ya se puede citar tal cual |

Lista lo que has encontrado, con recuentos, antes de escribir nada. Si el
contenido da menos de cuatro elementos, es flojo, y cuatro posts exprimidos de
ahí también lo serán. Dilo.

## Luego elige el formato de cada extracto

No todo es un Reel.

- **Afirmación, error, historia** a un Reel. Necesitan una voz y una cara.
- **Mecanismo, lista numerada** a un carrusel. Hay que releerlos.
- **Una frase citable** a una pantalla de story, no a un post.

## Luego monta la semana

Cada extracto se convierte en un post y cada post se sostiene completamente
solo. Quien lo ve no ha visto el original y no lo verá nunca. Nunca escribas
"como dije en mi último vídeo". El post es la cosa.

Asigna a cada uno una fórmula de gancho de `ig-reel/hooks.json` y varíalas.
Cinco posts de una misma fuente con la misma forma de gancho parecen una
fábrica de contenido, porque lo son.

Si el original es un vídeo del usuario, **usa el metraje real**. El clip en el
que dijo la cosa, con la reacción de verdad, gana a volver a grabarlo siempre.
Corta en la frase, no en la respiración.

Ordénalo en la semana para que la afirmación más fuerte vaya primero, la
historia caiga a mitad de semana y el mecanismo vaya al final, cuando la gente
a la que le gustaron los anteriores ya lo está esperando.

## Salida

```
ORIGEN: "Por qué dejamos de hacer llamadas de descubrimiento" (pódcast de 42 min, 8.900 palabras)

ENCONTRADO  5 afirmaciones, 9 cifras, 3 historias, 4 mecanismos, 2 errores, 7 frases citables

SEMANA
MAR  REEL      #2  Orden negativa      Deja de hacer llamadas de descubrimiento
                                       usa el clip del 14:20, se ríe al final
MIÉ  CARRUSEL  caption Trabajo B       El formulario de 4 preguntas que sustituyó a la llamada
VIE  REEL      #21 A media frase       "...y nueve días después pidió el reembolso"
DOM  REEL      #5  Tiempo comprimido   Seis horas a la semana recuperadas, un enlace borrado

Di "escribe el martes" y lo redacto.
```

Luego redacta cuando te lo pidan, uno a uno, cada uno por `/ig-reel` y
`/ig-human`. No sueltes cuatro guiones terminados de golpe. Sonarán todos igual
y el usuario no grabará ninguno.
