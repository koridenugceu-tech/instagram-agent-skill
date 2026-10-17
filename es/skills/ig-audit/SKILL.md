---
name: ig-audit
description: >-
  Autopsia de lo que el usuario ya ha publicado: qué reels funcionaron de
  verdad, por qué, y qué dejar de hacer. Úsala cuando el usuario pegue sus
  estadísticas de Instagram o sus posts anteriores y pregunte "qué está
  funcionando", "por qué ha fracasado esto", "léeme las estadísticas",
  "audita mi contenido", o quiera saber de qué hacer más.
---

# ig-audit

La única fuente honesta de lo que funciona en una cuenta es esa cuenta. Cada
regla de cada guía de Instagram, incluidas las de este pack, es una suposición
previa. Los últimos 30 posts del usuario son la prueba.

## Entrada

Pide lo que tenga el usuario:

- Estadísticas por post: visualizaciones, alcance, interacciones, tiempo de
  reproducción, guardados, veces compartido, seguidores ganados y el
  porcentaje del alcance que no le sigue. Las capturas valen. Si tiene la app
  en español, los nombres de las métricas cambian un poco según la versión;
  pídele la captura en vez de que te los dicte.
- O la gráfica de retención de sus mejores y peores reels recientes. Esa sola
  captura vale más que todo lo demás junto.
- O solo los posts y sus visualizaciones, que basta para una primera pasada.

Lee también `~/.claude/instagram/log.md` si existe, porque apunta qué fórmula
de gancho usó cada post.

## Qué medir de verdad

Las visualizaciones en bruto son el número menos útil de la pantalla, porque
dependen sobre todo de cuánta gente sigue ya la cuenta. Calcula esto en su
lugar y enseña las cuentas:

| métrica | cómo | qué te dice |
| --- | --- | --- |
| **Múltiplo** | visualizaciones / la mediana de visualizaciones de la propia cuenta | si fue un éxito de verdad o un día normal |
| **Alcance de no seguidores** | % del alcance que viene de gente que no sigue | si viajó o no |
| **Retención a los 3 s** | quienes siguen a los 3 s / quienes empezaron | si funcionó el gancho. Es la nota del gancho. |
| **Tiempo medio de reproducción** | directo de las estadísticas | si funcionó la mitad |
| **Envíos por alcance** | veces compartido / alcance | la señal individual más fuerte que puedes ganar. Un envío es alguien poniendo su nombre detrás. |
| **Seguidores por alcance** | seguidores ganados / alcance | si el perfil convirtió la atención |

Ordena por múltiplo y por envíos por alcance, no por visualizaciones. Un reel
con 4.000 visualizaciones y 90 envíos le ganó al de 60.000 y 11.

## Luego busca el patrón

Con los cinco de arriba y los cinco de abajo uno al lado del otro, busca qué
los separa, y prepárate para concluir algo que al usuario no le va a gustar:

- **Retención a los 3 segundos.** Si arriba y abajo difieren aquí, es el gancho
  y nada más, y todo lo que viene después es una distracción.
- **Fórmula de gancho.** ¿Qué números de `ig-reel/hooks.json` están en los cinco
  de arriba?
- **Formato.** Reel, carrusel, imagen suelta.
- **Duración.** Agrupa en menos de 15 s, de 15 a 30 s, de 30 a 60 s, más de 60 s.
- **Tema.**
- **Si el usuario respondió a los comentarios en la primera hora.**
- **Idioma o variante**, si la cuenta mezcla. Un público repartido entre España
  y Latinoamérica, o entre español e inglés, a veces explica más que el gancho.
- **Día y hora.** Mírala **la última** y solo si lo demás no enseña nada. Casi
  nunca es la causa y es donde la gente quiere que esté.

Di el hallazgo como una afirmación con su prueba al lado, y di cuánta confianza
tiene. Con 30 posts se ve un patrón. Con 6 no, y decirlo es mejor que
inventárselo.

## La distinción que ahorra meses

**Un reel con visualizaciones y sin seguidores nuevos no es un reel fallido, es
un problema de perfil.** Un reel sin visualizaciones es un problema de gancho.
Separa los dos antes de recomendar nada. Si el alcance de no seguidores es alto
y los seguidores por alcance son bajos, deja de reescribir ganchos y pasa a
`/ig-profile`.

## Salida

```
AUDITORÍA  ·  31 posts  ·  12 jun - 5 sep  ·  mediana 4.100 visualizaciones

LOS 5 DE ARRIBA POR MÚLTIPLO
  18,2x  #3  Nadie te cuenta      74.600 visu.  62 % no seguidores  ret.3s 71 %  128 envíos
   6,4x  #1  Confesión de coste   26.300 visu.  48 % no seguidores  ret.3s 64 %   71 envíos
  ...

LOS 5 DE ABAJO
   0,3x  #11 Lista con favorito    1.200 visu.   9 % no seguidores  ret.3s 31 %    2 envíos
  ...

LO QUE DICEN LOS DATOS
1. La retención a los 3 segundos lo explica todo. Arriba, media del 66 %; abajo, del 33 %.
   Todo lo demás que te preocupa depende de los dos primeros segundos.
2. Los posts en los que el que queda mal eres tú: media de 8,1x frente a 0,9x en el
   resto. n=5. La señal más fuerte de aquí y no está ni cerca.
3. Las listas de herramientas consiguen visualizaciones y nada más. Mucho alcance, ni
   envíos ni seguidores. Tres de tus cinco de abajo.
4. El día de la semana no dice nada. Tus medias del martes y del viernes están dentro
   del ruido. Deja de optimizarlo.

DEJA: las listas.
HAZ MÁS: los que tienen un coste que pagaste y una cifra detrás.
```

Luego pásale las conclusiones a `/ig-plan` para que la semana que viene se
construya sobre las pruebas del propio usuario y no sobre valores por defecto,
y a `/ig-viral` para que el archivo de referencias se filtre a las fórmulas que
funcionan en esta cuenta en concreto.
