---
name: ig-reel
description: >-
  Escribe un Reel de Instagram en español a partir de una idea en bruto:
  opciones de gancho sacadas de 26 fórmulas, el guion hablado, el texto en
  pantalla y una escaleta con tiempos, en la voz del usuario y puntuado antes
  de grabar. Úsala cuando el usuario quiera un Reel, un guion de vídeo corto,
  un gancho, una locución, "hazme un reel sobre X", "qué digo en este vídeo",
  o cuando vaya a grabar y aún no tenga la primera frase.
---

# ig-reel

Convierte una idea en bruto en un Reel que la gente termina.

En esta carpeta viven dos herramientas y las dos funcionan. Úsalas. No
juzgues el gancho a ojo ni adivines la duración.

```bash
python3 hookscore.py ganchos.txt              # ordena tus opciones de gancho
python3 hookscore.py --hook "una frase"       # puntúa una sola
python3 beats.py guion.txt --target 30        # escaleta con tiempos antes de grabar
```

`beats.py` calcula por **sílabas**, no por palabras: en español "y" y
"desafortunadamente" no tardan lo mismo en decirse. Por defecto, 6 sílabas por
segundo. Si `voice.md` trae el ritmo del usuario, pásalo con `--sps` (o con
`--wpm` si lo midió en palabras por minuto).

## Antes de escribir

1. Lee `~/.claude/instagram/voice.md` si existe. Es el perfil de voz del
   usuario: cómo habla a cámara, qué no diría nunca, a quién le habla, y en qué
   variante (España, México, Argentina...; tú, vos o usted; vosotros o
   ustedes). Si no existe, pide **tres de sus reels**, transcríbelos o léelos,
   deduce la voz y escribe el archivo. Un guion con la voz equivocada no sirve,
   porque lo tiene que decir en voz alta. Y uno con el "vosotros" equivocado,
   menos.
2. Lee `hooks.json` en esta carpeta. 26 fórmulas, cada una con plantilla,
   ejemplo relleno, versión en pantalla, para qué sirve y cómo se estropea.
3. Si la idea es floja, no la rellenes. Haz una sola pregunta agrupada: qué
   pasó, a quién, y qué costó o qué devolvió. Un Reel necesita una cosa
   concreta y verdadera. Consíguela antes de escribir.
4. Si existe `~/.claude/instagram/swipe.md`, léelo. Lo escribe `/ig-viral`, y
   son las pruebas del propio usuario sobre qué fórmulas funcionan ahora en su
   nicho. Pesan más que lo que dice este archivo.

## La forma

Un Reel se decide en los dos primeros segundos y se sostiene en los cinco
siguientes.

```
0:00 - 0:02   GANCHO      la afirmación. Frase hablada y frase en pantalla,
                          escritas por separado. Movimiento en el primer plano,
                          no una cara quieta.
0:02 - 0:07   LO QUE ESTÁ EN JUEGO   por qué le importa a quien mira. Una frase.
0:07 - ...    EL CUERPO   una idea por bloque, y el plano cambia en cada bloque.
ÚLTIMOS 3s    LA RECOMPENSA   cumple lo que prometió el gancho, y luego la única petición.
ÚLTIMA FRASE  EL BUCLE    repite una palabra del gancho para que la segunda vista encaje.
```

Duración: de 15 a 45 segundos es el rango de trabajo. Los Reels llegan a 3
minutos y casi nadie debería usarlos. Por debajo de 7 segundos se inflan las
repeticiones y nada más.

## El proceso

**1. Elige tres ganchos, no uno.** Pasa la idea por `hooks.json`, escoge tres
fórmulas que de verdad encajen y escribe para cada una la frase hablada y la
de pantalla. Fórmulas distintas, no tres versiones de la misma.

**2. Puntúalos.** Pon las tres frases habladas en un archivo, una por línea, y
ejecuta `hookscore.py`. Enséñale el ranking al usuario. Si el primero está por
debajo de 50, todavía no tienes el gancho y ninguna edición lo arregla.

**3. Escribe el guion** sobre el gancho ganador. Lenguaje hablado, como habla
el usuario de verdad. Frases cortas. Ninguna frase que tenga que ensayar. En
español es fácil escribir subordinadas de tres pisos que nadie dice; si una
frase tiene más de una coma, probablemente sean dos.

**4. Mídelo.** `beats.py guion.txt --target {duración}`. Arregla cada aviso: un
gancho de más de 3 segundos, cualquier bloque de más de 4, una racha de bloques
sin nada concreto, la falta de bucle. Repite hasta que salga limpio.

**5. Humanízalo.** Pasa el guion por `/ig-human` antes de enseñarlo. Una frase
que suena a escrita se nota en cuanto alguien la dice en voz alta.

**6. Imprime el bloque.** El guion en un bloque de código, el texto en
pantalla como lista aparte con tiempos, y después:

```
REEL LISTO
gancho:     #3 Nadie te cuenta, 80 FUERTE
duración:   28,4s en 9 bloques a 6 síl/s
pantalla:   6 rótulos
humanizar:  4 artefactos quitados, nota humana 81 APTO
caption:    lo siguiente es /ig-caption

Responde "sí" para registrarlo, o dime qué cambio.
```

**7. Nunca publiques.** Esta skill produce un guion. El usuario lo graba y lo
publica. Con un "sí", añade a `~/.claude/instagram/log.md` la fecha, la
fórmula usada y la primera frase, para que `/ig-audit` tenga historial.

## El texto en pantalla es otro guion

Escríbelo aparte, siempre. Se lee antes de oírse.

- **Seis palabras o menos por rótulo.** Lo lee alguien con el brazo estirado
  que todavía no está escuchando. El español es más largo que el inglés:
  recorta artículos y verbos que sobren ("5 HORAS -> 20 MIN").
- **El rótulo del gancho está en el fotograma 1**, no después de un silencio.
- **Dentro de la zona segura.** En un fotograma de 1080x1920, nada por encima
  de y=230 ni por debajo de y=1440, y deja libres los 230 píxeles de la
  derecha. La interfaz tapa todo lo que queda fuera: el caption, la barra de
  acciones, la tira del audio.
- **Nunca pongas el gancho donde va el caption.** Es la parte de abajo y queda
  tapada.
- **Subtítulos quemados en el cuerpo.** La mayoría lo ve primero sin sonido.

## Reglas que marcan la diferencia

- **Una idea por Reel.** Si el guion tiene dos, tienes dos Reels. Dilo.
- **Cifras antes que adjetivos.** "4.200 €" gana a "un montón". Si el usuario
  no ha dado una cifra, pídesela en vez de escribir alrededor del hueco.
- **Fuera la intro.** Sin saludo, sin "en este vídeo", sin nombre, sin cortinilla
  del logo. El vídeo empieza en la frase a la que llegarías en el segundo seis.
- **Cambia el plano en cada bloque.** Un plano quieto de 8 segundos es donde la
  gente se va, y `beats.py` lo va a señalar.
- **Una petición al final.** Comentar una palabra, guardar o seguir. Una.
- **Nunca te inventes nada.** Ni métricas, ni clientes, ni facturación, ni
  resultados a nombre del usuario, ni como relleno. Si hace falta una cifra y
  no la sabes, deja `{{tu cifra}}` en el guion y avísalo.
- **No escribas un guion alrededor de un audio en tendencia que el usuario no
  puede usar.** Si la idea necesita su propia voz, dilo.

## Una advertencia sobre la nota

`hookscore.py` se midió contra 80 ganchos reales en español: caza bien los
malos (AUC 0,85) y **no distingue los éxitos de un creador de sus fracasos**
(AUC 0,49, una moneda al aire). Úsala para descartar saludos, preámbulos y
ganchos sin nada concreto, y fíate de la gráfica de retención para lo demás.

## Ejemplo

```
/ig-reel hemos bajado el tiempo de las propuestas de 5 horas a 20 minutos con una plantilla
```

```
GANCHOS  (puntuados)
  76  FUERTE  #5  Tiempo comprimido  "Las propuestas me llevaban cinco horas. Ahora, solo veinte minutos."
                                     en pantalla: 5 HORAS -> 20 MIN
  55  OK      #1  Confesión de coste "Facturé cuatro horas a la semana de maquetar. Durante dos años."
                                     en pantalla: 2 AÑOS TIRADOS
  37  FLOJO   #9  Róbamelo           "Róbame la plantilla que lo consiguió."
                                     en pantalla: RÓBAME ESTO

Grabaría el #5: la proporción es creíble, se lee de un vistazo en pantalla
y la cifra es tuya.
```
