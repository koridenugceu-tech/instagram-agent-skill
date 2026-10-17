---
name: ig-plan
description: >-
  Planifica la semana en Instagram: qué publicar, en qué formato, cuándo y con
  quién interactuar. Úsala cuando el usuario diga "planifica mi semana", "qué
  publico", "calendario de contenido", "no sé de qué publicar", o quiera un
  horario de publicación y una lista de cuentas con las que interactuar.
---

# ig-plan

La sala de control. Todo lo demás del pack ejecuta; esto decide qué se ejecuta.
Úsala una vez a la semana, siempre el mismo día.

## Entrada

Si existen `~/.claude/instagram/voice.md`, `swipe.md` y `log.md`, léelos. El
archivo de referencias son las pruebas del propio usuario, sacadas con
`/ig-viral`, sobre qué fórmulas funcionan ahora mismo en su nicho, y pesa más
que cualquier cosa de este archivo. El registro evita que el plan repita un
tema de las dos últimas semanas.

Si no existen, pide cuatro cosas y apúntalas:

1. Qué vende el usuario y a quién.
2. Los tres o cuatro temas por los que quiere que le conozcan.
3. Qué ha pasado de verdad esta semana: una llamada con un cliente, una cifra,
   un error, algo que ha construido, una discusión. De ahí salen los posts.
4. Diez cuentas ante las que merece la pena dejarse ver.

## Qué publicar

De cuatro a cinco posts a la semana, y al menos tres de ellos Reels. Los Reels
son el único formato de Instagram que llega de forma fiable a gente que no
sigue la cuenta. Los carruseles profundizan con quien ya la sigue. Las Stories
son diarias y se planifican aparte.

Mezcla a lo largo de la semana, nunca dos del mismo tipo seguidos:

| tipo | cuántos | trabajo |
| --- | --- | --- |
| **Prueba** | 1 por semana | algo que pasó, con una cifra. Reel. |
| **Enseñar** | 1 o 2 por semana | una cosa que quien mira puede hacer hoy. Reel o carrusel. |
| **Opinión** | 1 por semana | una postura que te podría costar seguidores. Reel. |
| **Historia** | 1 cada dos semanas | una escena con un coste. Reel. |
| **Oferta** | 1 cada dos semanas | lo que vendes, dicho claro, sin pedir perdón. Carrusel o stories. |

Para cada hueco da: el tema, el ángulo concreto sacado de lo que pasó esta
semana, el formato y el número de fórmula de gancho de `ig-reel/hooks.json`. No
un tema, un ángulo. "IA" no es un plan. "La propuesta que perdimos porque el
borrador tenía una raya en cada párrafo" es un Reel.

## Cuándo publicar

Publica cuando tu público está despierto y no está trabajando. Para la mayoría
de públicos de consumo es a última hora de la tarde; para un público
profesional, a primera hora de la mañana.

Con público hispanohablante esto cambia mucho según el país. En España la
noche empieza más tarde que en buena parte de Latinoamérica, y entre Madrid y
Ciudad de México hay entre siete y ocho horas de diferencia, así que un público
repartido entre los dos lados te obliga a elegir a quién priorizas. Pregunta de dónde
es la mayoría del público (lo dicen las estadísticas de la cuenta) y ancla las
horas a **su** zona horaria, no a la del usuario.

Pero dilo claro: **la hora importa mucho menos que los dos primeros segundos.**
Instagram sigue enseñando un Reel durante días si funciona, y entierra uno bien
programado que no funciona. Si el usuario está optimizando la hora de
publicación antes de que funcionen sus ganchos, está puliendo lo que no es, y
tienes que decírselo.

## La ronda de interacción, que no es opcional

20 minutos al día, antes de publicar, no después. Haz una lista de 10:

- **5 de alcance**: cuentas con un público que el usuario quiere, donde un buen
  comentario se ve. Comenta pronto, antes de que el hilo tenga 200 respuestas.
- **3 iguales**: mismo tamaño, mismo campo. Es el grupo que devuelve.
- **2 compradores**: gente que de verdad podría comprar. Comenta durante
  semanas antes de cualquier DM, y nunca vendas en un comentario.

Pásale la lista a `/ig-comment`.

## Salida

```
SEMANA DEL 15 DE SEPTIEMBRE

LUN  solo interacción  (20 min, lista abajo)
MAR  21:00  REEL      PRUEBA    #5  Tiempo comprimido - propuestas de 5 h a 20 min
MIÉ  solo stories + interacción
JUE  20:30  CARRUSEL  ENSEÑAR   caption Trabajo B     - la cláusula en 4 diapositivas
VIE  21:00  REEL      OPINIÓN   #2  Orden negativa    - deja de hacer llamadas de descubrimiento
SÁB  -
DOM  19:30  REEL      HISTORIA  #21 A media frase     - el correo del reembolso

STORIES  todos los días, de 3 a 5 pantallas, caja de preguntas el jueves.

INTERACCIÓN  (5 alcance / 3 iguales / 2 compradores)
  ...

Di "escribe el martes" y lo redacto.
```

Escribe el plan en `~/.claude/instagram/plan.md` para que lo lean las demás
skills. No se programa ni se publica nada en ningún sitio. Es un plan y lo
ejecuta el usuario.
