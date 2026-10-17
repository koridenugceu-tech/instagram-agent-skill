---
name: ig-comment
description: >-
  Escribe comentarios en español en los posts y reels de otras personas que se
  lean como alguien con opinión, no como un bot. Úsala cuando el usuario pegue
  un post o un reel y quiera un comentario, diga "comenta esto", "interactúa
  con esto", "qué pongo aquí", o quiera un lote para su ronda diaria de
  interacción.
---

# ig-comment

Comentar son los veinte minutos con más palanca de Instagram y los más fáciles
de hacer mal. Un comentario arriba del todo en un reel de 40.000 vistas lo ve
más gente que la mayoría de posts de la mayoría de cuentas, y es el único sitio
donde un desconocido puede tocar y llegar directo a un perfil.

Un comentario genérico es peor que ninguno. Gasta un toque que no lleva a nada
y marca la cuenta como de grupo de interacción ante la única persona cuya
opinión importaba, que es el creador.

## Entrada

El usuario pega el texto del post o del reel, o una captura, con el nombre de
la cuenta. Si da una URL que no puedes abrir, pídele que lo pegue. No uses un
navegador para hacer scraping del feed y no publiques nada.

## Los nueve tipos de comentario

Elige según lo que es el post de verdad. Nunca por defecto el tipo 1.

| # | tipo | cuándo | forma |
| --- | --- | --- | --- |
| 1 | **Aporta un dato** | el post afirma algo que puedes apoyar con una cifra | "A nosotros igual: el 40 % de..." |
| 2 | **Aporta el caso que falta** | el post tiene razón pero se queda corto | "Esto se cumple hasta que {condición}." |
| 3 | **Discrepa con respeto** | de verdad crees que está mal | di primero en qué estás de acuerdo, luego dónde te separas |
| 4 | **Amplía una frase** | una de sus frases es la buena | cítala y construye encima |
| 5 | **Haz la pregunta de verdad** | el post se saltó la parte difícil | una pregunta, concreta |
| 6 | **El recibo** | tú has hecho lo que describe | qué pasó, en dos frases |
| 7 | **La corrección** | hay un error de hecho | ten razón, sé breve, sé amable, asegúrate |
| 8 | **El otro enfoque** | datos correctos, marco equivocado | "Otra forma de leer esto:" |
| 9 | **La frase corta** | el post no necesita nada, quieres estar | menos de 10 palabras, y que sea gracioso o verdad |

## Reglas

- **De una a tres frases.** Los comentarios de Instagram se leen en una columna
  estrecha debajo de un vídeo. Un párrafo se pliega detrás de "más" y nadie lo
  abre.
- **Nunca empieces con** "Gran post", "Me encanta", "Qué verdad", "Esto 👏",
  "Lo necesitaba hoy", "Brutal", "Top", "Tal cual", o el nombre del creador
  con exclamación. Todos son invisibles.
- **Nada de comentarios solo con emojis** ni con un emoji como primer carácter.
- **Nunca resumas el reel.** Todos los que lo ven lo acaban de ver.
- **Una idea.** Un comentario con dos puntos parece que quiere secuestrar el
  hilo.
- **Di lo concreto.** Si el comentario valdría debajo de cualquier post del
  tema, no es un comentario, es ruido.
- **Respeta el registro del creador.** Si el post tutea, tutea. Si es de una
  cuenta de Argentina que vosea, un "vosotros" de España suena a forastero. Y
  al revés.
- **Nunca vendas.** Ni la oferta, ni el enlace, ni "pásate por mi perfil". Es la
  forma más rápida de que te bloquee justo la persona a la que querías llegar.
- **Pronto importa más aquí que en ningún sitio.** Un comentario en la primera
  hora en un reel que luego viaja, viaja con él.

## Salida

Da **dos opciones de tipos distintos**, etiquetadas, más una línea sobre cuál
publicarías y por qué. Pasa las dos por `/ig-human` antes: los comentarios son
cortos, así que una raya o una frase hecha se nota proporcionalmente más que en
un caption.

```
OPCIONES DE COMENTARIO  (en el reel de @cuenta sobre precios)

[6 · Recibo]
Nosotros subimos un 40 % en marzo y perdimos exactamente un cliente, el que se
llevaba media bandeja de entrada. Tardé ocho meses en dejar de tenerle miedo.

[3 · Discrepa con respeto]
De acuerdo con lo del anclaje. Donde no lo veo es en hacerlo a mitad de
proyecto. Lo probamos y nos costó una renovación que iba bien.

Publicaría el primero. Concede algo y lleva una cifra.
```

## Modo lote

Para una ronda de interacción, pide los 5 a 10 posts pegados en un solo
mensaje, devuelve un comentario por post en un único bloque y lleva una nota en
`~/.claude/instagram/log.md` de a quién se ha comentado esta semana. Comentar a
las mismas tres cuentas todos los días se nota, y parece exactamente lo que es.

## Nunca

No publiques solo, no automatices comentarios y no uses un navegador para
publicar en nombre del usuario. La interacción automatizada incumple las
Condiciones de uso de Instagram y hace que bloqueen cuentas. Esta skill escribe
el comentario. El usuario lo publica.
