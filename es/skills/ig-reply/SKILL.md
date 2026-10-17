---
name: ig-reply
description: >-
  Gestiona los comentarios en los reels y posts del propio usuario: redacta en
  español respuestas a los que merecen respuesta, ordenados por cuáles la
  merecen. Úsala cuando el usuario pegue sus comentarios, diga "responde a
  estos", "gestiona mis comentarios", "alguien ha dicho X en mi reel", o esté
  lidiando con un crítico, un hater o un posible cliente en los comentarios.
---

# ig-reply

El hilo de comentarios de tu propio post es donde se decide el alcance. Cada
respuesta es otra interacción en el post, las respuestas de la primera hora
hacen casi todo el trabajo, y en Instagram una respuesta también puede ser un
Reel, que es el movimiento más infrautilizado de la plataforma.

Pero no todos los comentarios valen lo mismo, así que esta skill ordena antes
de escribir.

## Entrada

El usuario pega los comentarios, a ser posible con el @. Las capturas valen. No
hagas scraping del hilo con un navegador.

## Primero, clasifica

Mete cada comentario en uno de seis grupos y di los recuentos en voz alta:

| grupo | qué es | qué recibe |
| --- | --- | --- |
| **PALABRA CLAVE** | la palabra que pediste que comentaran | lo prometido, enviado a mano o con tu herramienta aprobada |
| **CLIENTE** | alguien describiendo el problema que resuelves | una respuesta de verdad en público, y luego una puerta |
| **FONDO** | aporta datos, discrepa, amplía | la respuesta más larga del hilo |
| **PREGUNTA** | una pregunta que tiene mucha gente | esta se convierte en un Reel, no solo en una respuesta |
| **APOYO** | "🔥", "buenísimo", una mención | un me gusta, y de 3 a 8 palabras como mucho |
| **RUIDO** | venta, spam, mala fe, cebo | nada, o una línea y fuera |

Escribe en ese orden y para cuando se acabe el valor.

## El movimiento que casi todos se saltan

Si una pregunta de los comentarios la tienen otras treinta personas,
**contéstala con un Reel**. Instagram pega el comentario en el vídeo nuevo como
sticker, quien preguntó recibe un aviso, y una pregunta con demanda real se
convierte en un post con el gancho ya escrito. Marca cada PREGUNTA que cumpla y
pásasela a `/ig-reel` como fórmula #16. Usa la pregunta literal, con sus faltas
y sin el ¿ si no lo puso: así es como la buscará la gente.

## Cómo responder

- **Responde a la pregunta de verdad.** Si alguien pregunta cómo, dile cómo, en
  la respuesta. No le mandes al DM a oír una respuesta que podía tener ahí.
- **Usa su nombre una vez**, al principio, sin exclamación.
- **Iguala su longitud.** Un comentario de cuatro palabras no lleva una
  respuesta de cuatro líneas.
- **Iguala su registro.** Si te tutea, tutéale. Si te trata de usted, contesta
  de usted, aunque tu cuenta tutee.
- **A un crítico:** concede primero la parte verdadera, con sus palabras, y
  luego mantén tu postura. Nunca borres, nunca te pongas a la defensiva, nunca
  respondas dos veces en el mismo hilo.
- **A un hater:** nada. Una respuesta es alcance, y el alcance es a lo que vino.
  Oculta el comentario si es ofensivo. Los controles de comentarios de
  Instagram existen y usarlos no es perder.
- **A un posible cliente:** responde entero en público. La puerta es una frase
  al final y es una oferta de ayuda, no una venta. La respuesta pública es lo
  que hace que el siguiente te escriba por DM.

## Comentarios de palabra clave

Si el post usaba una petición de palabra clave, esos comentarios son el sentido
entero del post. Cada uno es una persona que levantó la mano. Responde a cada
uno y luego envía lo prometido. Si el usuario tiene una automatización con las
herramientas de Instagram o un partner aprobado, dilo y déjala funcionar; si
no, las respuestas son a mano y a este volumen está bien. Nunca mandes DM
masivos a gente que no comentó.

## Salida

Un bloque, agrupado por tipo, con cada respuesta lista para copiar y ya
humanizada:

```
RESPUESTAS  ·  84 comentarios  ·  41 PALABRA CLAVE, 2 CLIENTE, 3 FONDO, 2 PREGUNTA, 34 APOYO, 2 RUIDO

PALABRA CLAVE  (41)  manda la cláusula. Una línea cada uno, mismo cariño, no copiar y pegar.

CLIENTE
@cuenta - "a nosotros nos pasó esto mismo en junio"
> Lo que nos lo arregló fue sacar el pago de la aprobación del todo. Si te
> sirve, te paso la redacción.

PREGUNTA -> REEL
@cuenta - "y si se niegan a firmarla q haces"
  34 me gusta en este comentario. Eso es un Reel, no una respuesta. Fórmula #16.

RUIDO  (2)  ignorados. Responder les da alcance.
```

Luego la puerta: no se publica nada hasta que el usuario diga que sí. Él pega
las respuestas.
