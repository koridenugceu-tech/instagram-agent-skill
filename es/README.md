# La skill de Instagram, en español

Trece skills de Claude que llevan una cuenta de Instagram, adaptadas al
español. Gratis, MIT, sin registro, sin clave de API, sin nada que conectar.

Es la misma idea que el pack en inglés que hay en la raíz de este repositorio,
pero **no es una traducción**. Las herramientas del original estaban hechas
para el inglés por dentro: sus regex solo veían letras de la A a la Z, su
detector medía la voz contando contracciones ("don't", "I'm"), su léxico era de
palabras inglesas y su clasificador de ganchos buscaba frases en inglés. Pasado
un texto en español, casi todo daba cero o daba igual. Aquí se ha reescrito lo
que hacía falta.

**No se publica nada hasta que digas que sí.** Estas skills escriben. Tú
publicas.

## Instalar

Como plugin, en Claude Code:

```
/plugin marketplace add koridenugceu-tech/instagram-agent-skill
/plugin install instagram-agent-es
```

O a mano:

```bash
git clone https://github.com/koridenugceu-tech/instagram-agent-skill.git
cp -r instagram-agent-skill/es/skills/ig-* ~/.claude/skills/
```

Las skills se llaman igual que las inglesas (`/ig-reel`, `/ig-human`...), así
que **instala una variante u otra, no las dos** en la misma carpeta de skills.
Como plugin no chocan, porque cada una va con su espacio de nombres.

Después dedica diez minutos a `templates/voice.md`. Cópialo en
`~/.claude/instagram/voice.md` y rellénalo, o mándale a Claude tres de tus
reels y dile "escribe mi voice.md a partir de estos". Lo leen todas las skills.
En esta variante pregunta además lo que en español cambia un guion entero: de
dónde eres, si tuteas, voseas o hablas de usted, y si dices vosotros o
ustedes.

## Las trece

| comando | qué hace |
| --- | --- |
| `/ig-reel` | Una idea a un Reel. Tres ganchos de [26 fórmulas en español](skills/ig-reel/hooks.json), puntuados, y luego el guion, el texto en pantalla y una escaleta con tiempos. |
| `/ig-viral` | Busca lo que funciona en tu nicho, lo ordena por múltiplo sobre la mediana de cada cuenta, nombra la fórmula y escribe el archivo de referencias. |
| `/ig-caption` | El caption, revisado. Te enseña los 125 caracteres que muestra el feed antes del toque. |
| `/ig-carousel` | Posts para deslizar. La portada que se gana el deslizamiento, el texto de cada diapositiva y los archivos de 1080x1350. |
| `/ig-story` | La secuencia diaria de stories, qué sticker hace qué, y el embudo a DM que empieza cuando ellos se mueven primero. |
| `/ig-profile` | Puntúa tu perfil con una [rúbrica de 12 partes](skills/ig-profile/rubric.json) sobre 100 y lo reescribe empezando por lo que más resta. |
| `/ig-plan` | La semana. Qué publicar, en qué formato, cuándo y las 10 cuentas con las que interactuar. |
| `/ig-human` | El humanizador. Dos scripts que funcionan. Más abajo. |
| `/ig-comment` | Comentarios en posts ajenos. Nueve tipos, según lo que es el post. Nunca "🔥🔥🔥". |
| `/ig-reply` | El hilo de tu propio post. Clasifica en palabra clave / cliente / fondo / pregunta / apoyo / ruido y responde en ese orden. |
| `/ig-dm` | La entrega de la palabra clave, el primer mensaje, la propuesta de colaboración y los dos seguimientos. Dos. |
| `/ig-repurpose` | Un vídeo, pódcast o newsletter a una semana de reels y carruseles que se sostienen solos. |
| `/ig-audit` | Autopsia de lo publicado. Ordena por múltiplo y por envíos por alcance, no por visualizaciones. |

## Qué ha cambiado de verdad respecto al inglés

**El humanizador tiene léxico propio.** 266 términos escritos para el español
de máquina, no traducidos del inglés: "adentrarse en", "sumérgete en",
"potenciar", "crucial", "sinergia", "cabe destacar que", "en el mundo actual",
"en el vídeo de hoy", "sígueme para más".

- **Concuerda en género y número.** "Robusto, robusta, robustos, robustas"
  tienen cada uno su reemplazo ("sólido, sólida..."), para que la frase siga
  siendo gramatical después del cambio.
- **Ignora las tildes al buscar** (no la eñe), porque en el móvil mucha gente
  escribe sin ellas.
- **Caza calcos del inglés**, que es la señal más clara de un texto pensado en
  inglés y pasado por máquina: "al final del día", "hace sentido", "mover la
  aguja", "poco sabía yo", "corre, no camines".
- **Respeta el ¿ y el ¡.** Si un borrado deja un "¿?" vacío lo limpia, y
  recupera la mayúscula detrás del signo de apertura.
- **Rayas y comillas angulares.** "—Inciso—" y «comillas» son correctos en un
  libro y raros en un caption escrito desde el móvil: se pasan a coma y a
  comillas rectas.
- **Señales nuevas:** las aperturas serviciales ("¡Claro!", "¡Excelente
  pregunta!"), el "¿Estás listo para...?" y las mayúsculas a la inglesa ("Cómo
  Escribir Un Caption Que Vende").

**El detector mide la voz de otra manera.** Sin contracciones que contar, la
VOZ se mide con marcas coloquiales (pues, vale, o sea, en plan, ¿no?, ¿sabes?,
che, wey) y con la persona gramatical. Y como el español omite el pronombre
("perdí 18.000 €", no "yo perdí"), la primera y la segunda persona se cuentan
también por el verbo: "perdí", "llevas", "tenés".

**La concreción entiende el español.** Los meses y los días van en minúscula,
así que la mayúscula no bastaba para encontrar lo concreto. Ahora cuentan
también "marzo", "el jueves", "dieciocho mil", "euros".

**Los tiempos se miden por sílabas.** En español la longitud de las palabras
varía mucho más que en inglés ("y" frente a "desafortunadamente"), así que
contar palabras daba duraciones malas. `beats.py` y `hookscore.py` cuentan
sílabas (con diptongos e hiatos), y dicen las cifras como se dicen en voz alta:
"18.000 €" son seis sílabas, "dieciocho mil euros".

**Las 26 fórmulas de gancho están reescritas**, con ejemplos en euros, con su
versión en pantalla y con regex que reconocen el español hablado ("nadie te
cuenta", "me llevaba", "róbame esto", "no necesitas"). La fórmula del refrán al
revés usa refranes de verdad: "quien mucho abarca, mucho aprieta".

**Los formatos son los de aquí.** Miles con punto ("1.200.000"), decimales con
coma ("60,0x"), euros detrás de la cifra, hashtags con eñe y tildes, y
cabeceras del TSV de `/ig-viral` en español (cuenta, seguidores, mediana,
vistas, gancho).

## Las cinco herramientas

Sin dependencias, sin red, no se sube nada. Se ejecutan en tu máquina, sobre tu
texto.

### Ganchos

```bash
python3 hookscore.py ganchos.txt              # ordena tus opciones
python3 beats.py guion.txt --target 30        # mídelo antes de grabar
```

```
RANKING DE GANCHOS
==============================================================================
->  81.4 FUERTE  Nadie te cuenta que tus primeros 30 reels tienen que fracasar.
        más floja: TENSIÓN (70)
    81.4 FUERTE  Perdí 18.000 € por una cláusula que no estaba en el contrato.
        más floja: DESTINATARIO (70)
    54.4 OK      Deja de hacer scroll si quieres crecer en Instagram en 2026 🔥
        más floja: TENSIÓN (70)
        eliminatorio: Empieza con "deja de hacer scroll". Pedir atención demuestra que no te la has ganado.
        eliminatorio: Emoji en el gancho. El texto en pantalla a tamaño de gancho tiene sitio para palabras o para un emoji, no para las dos cosas.
    51.2 OK      Las propuestas me llevaban cinco horas. Ahora, veinte minutos.
        más floja: TENSIÓN (20)
     5.4 FLOJO   Hola chicos, hoy quería hablaros de estrategia de contenido
        más floja: ARRANQUE (0)
        eliminatorio: Saludo. Nadie abre Instagram para que le saluden.
```

`beats.py` calcula cuánto se tarda en decir cada línea, las apila en códigos de
tiempo y señala las cuatro cosas que matan un Reel en la edición: un gancho de
más de tres segundos, un bloque tan largo que da tiempo a irse, una racha de
líneas sin nada concreto y la falta de bucle con la primera frase.

```
ESCALETA  ·  69 palabras, 129 sílabas  ·  ~21,5s a 6 síl/s  ·  objetivo 30s
=============================================================================
  0:00,0   4,0s  GANCHO     Perdí 18.000 € por una cláusula que no estaba en el contrato.
                            ^ el gancho dura 4,0s, pasa de los 3s
  0:04,0   8,0s  MITAD      Esta es la cláusula exacta que ahora pongo en todos mis contratos, ...
                            ^ 8,0s en un solo bloque
  ...
  - Bucle: el último bloque repite "18.000" del gancho. Las segundas vistas son alcance gratis.
```

### El caption

```bash
python3 caption.py caption.txt --keywords "contratos freelance,edición de vídeo"
```

```
  LO QUE ENSEÑA EL FEED
  +------------------------------------------------------+
  | Perdí 18.000 € por una cláusula que no estaba en el  |
  | contrato, y lo peor es que me lo había leído dos     |
  | veces antes de firmarlo.                             |
  +--------------------------------------------- ... más +

  BIEN  PRIMERA LÍNEA      125 caracteres, cabe entera
  BIEN  GANCHO CONCRETO    2 cifra(s), fecha(s) o nombre(s) en la ventana visible
  BIEN  HASHTAGS           3 hashtag(s): #freelance #contratos #autonomos
  BIEN  UNA PETICIÓN       una llamada a la acción: comentar una palabra clave
```

Aplica el tope actual de **cinco hashtags por publicación**, que Instagram
fijó el 18 de diciembre de 2025. Los términos de búsqueda se comparan sin
tildes, así que "video" encuentra "vídeo".

### El humanizador

```bash
python3 humanize.py borrador.txt --report     # límpialo y enseña cada cambio
python3 detect.py borrador.txt                 # puntúalo, cinco comprobaciones
python3 detect.py antes.txt despues.txt        # demuestra la diferencia
```

Contra un caption escrito para ser lo peor posible ("Deja de hacer scroll. En
el mundo actual, crear contenido es crucial — y no es solo publicar, es
conectar..."):

```
  NOTA HUMANA   ##......................   6.4   MARCADO
```

Después de `humanize.py`, sin reescribir todavía las estructuras señaladas:

```
  NOTA HUMANA   ######..................  24.1   MARCADO    (+17.7)
```

Y un texto escrito por una persona, con cifras, fechas y su forma de hablar:

```
  NOTA HUMANA   #####################...  88.7   APTO
```

Fíjate en que el borrador limpio sigue MARCADO. Es lo correcto: el script quita
lo mecánico, pero un texto sin una sola cifra, sin nadie que hable y con tres
estructuras de plantilla necesita una reescritura, y eso lo hace una persona.

### El archivo de referencias

```bash
python3 swipe.py recogidos.tsv --out ~/.claude/instagram/swipe.md
```

```
REFERENCIAS  ·  4 reels  ·  4 cuentas  ·  referencia: mediana de la cuenta
==============================================================================
    60,0x  gancho  80  #9  Róbamelo                 @c                   180.000
           "roba este seguimiento de cuatro líneas, me costó dos años"
    37,5x  gancho  81  #3  Nadie te cuenta          @a                   412.000
           "nadie te cuenta que tus primeros 30 reels tienen que fracasar"
     1,5x  gancho  30  -   sin clasificar           @d                     9.000
           "qué buena tarde hace hoy"
     1,3x  gancho  13  -   sin clasificar           @b                 1.200.000
           "en este vídeo te voy a enseñar mi rutina de mañana"
```

## Lo que está medido y lo que no, que es lo importante

Repetí en español la medición del README inglés. El corpus son **80 ganchos
reales**: los tres primeros segundos de los subtítulos automáticos (`es-orig`,
el reconocimiento de voz original, no una traducción) de los 8 shorts con más
y los 8 con menos vistas de cinco canales: Euge Oller (negocios), Farmacéutico
Fernández (salud), QuantumFracture (ciencia), La Hiperactina (biología) y
Xavier Mitjana (IA). Las vistas van de 281 a 31 millones. Son YouTube Shorts y
no Reels por la misma razón que en inglés: Instagram no da las vistas sin
entrar en la cuenta de otro.

**1. Caza bien los ganchos malos.** Contra diez ganchos escritos a propósito
para ser malos (saludos, "en este vídeo te voy a enseñar", "bueno, pues hoy os
quería hablar"), **AUC 0,85**, y nueve de los diez quedan por debajo de la
mediana del corpus real. En inglés, 0,83.

**2. No elige ganadores.** Separando los éxitos de un creador de sus fracasos,
**AUC 0,49: una moneda al aire**. Canal a canal va de 0,38 a 0,67, y con 34
ganchos más de los mismos canales, 0,58. En inglés, 0,56. De las cinco
comprobaciones, solo CONCRECIÓN tiene medianas distintas (45 arriba, 15
abajo), y aun así su AUC es 0,53. TENSIÓN da 20 de mediana en los éxitos, en
los fracasos y en los ganchos malos: en este corpus no mide nada. Y
DESTINATARIO va al revés (AUC 0,36): los fracasos le hablan más a quien mira,
sobre todo con "¿quieres...?" de vídeo patrocinado.

**3. El clasificador de fórmulas estaba roto, como en inglés.** Las regex de
`hooks.json`, escritas a partir de las plantillas, nombraban el **12 %** de los
ganchos reales. Reescritas con esos casos, el 62 %, pero eso es contra los
mismos ganchos con los que se escribieron. **Contra 34 ganchos que no se
usaron para escribirlas, nombran el 26 %** (las de plantilla, el 6 %). Esa es
la cifra que vale. Lo que faltaba:

- La Presentación no reconocía la apertura más común en divulgación: "esto que
  ves aquí son...", "esta de aquí es un bazo", y tampoco "nueva herramienta
  gratis de Google" ni "ya puedes...".
- La Pregunta literal exigía el signo de cierre, y los subtítulos automáticos
  casi nunca lo ponen: "qué pasaría si pusieras la mano dentro de un
  acelerador" no contaba.
- El Resultado de otro no veía "esta chica no pudo vender ni 36 camisetas" ni
  "hay gente que...". El Superlativo no veía "una de las fuerzas más
  poderosas".
- Un fallo: El aviso a un grupo tomaba "Antes de empezar, dale a like" por un
  aviso a "-antes", como "estudiantes".

**Lo que no cambié en `hookscore.py`, porque no hay evidencia:** probé a quitar
"esto es" de las aperturas flojas, ya que tantos éxitos de divulgación empiezan
así, y el AUC pasó de 0,49 a 0,50. Nada. El ritmo de habla medido en los 80
shorts es de 6,3 sílabas por segundo de mediana (la mitad central, entre 5,7 y
6,9), así que el 6 por defecto se queda.

**4. El detector de texto de IA distingue algo, pero casi nunca aprueba a una
persona.** El README inglés no mide `detect.py`, así que esta es su primera
medición. Lado humano: 36 descripciones de YouTube publicadas antes de
diciembre de 2022, es decir, antes de ChatGPT, por nueve canales (Academia
Play, CdeCiencia, Date un Vlog, Euge Oller, Jaime Altozano, La Gata de
Schrödinger, La Hiperactina, Nate Gentile y Un Mundo Inmenso). Solo el cuerpo,
sin enlaces ni firmas, con una mediana de 70 palabras, el largo de un caption.
Lado IA: el mismo encargo para cada vídeo ("Escribe la descripción para
YouTube del vídeo «título» del canal X, unas N palabras, sin enlaces ni
hashtags"), una petición independiente por texto a través de OpenRouter, a
cinco modelos: GPT 6.1, Gemini 4, Grok 4.7, DeepSeek v4.1 y Mistral Large 4.
Son 180 textos y ningún modelo había visto el detector.

- **AUC 0,75** con los cinco juntos. Por modelo, de 0,71 (Grok) a 0,79
  (DeepSeek). Antes del cambio de abajo era 0,71. Gemini pedido a mano, en
  dos bloques de 18 encargos en el mismo chat, da 0,72: coherente.
- **El veredicto separa a medias.** IA: APTO 1 de 180, REVISAR 22 %, MARCADO
  77 %. Humanos: APTO 1 de 36 (3 %), REVISAR 56 %, **MARCADO 42 %**. Un
  MARCADO es más probable en un texto de máquina, pero le pasa a casi la
  mitad de las personas, y el APTO no lo alcanza casi nadie.
- Por comprobación, AUC: VOZ 0,69, VARIACIÓN 0,68, RELLENO 0,64, CONCRECIÓN
  0,62 y HUELLA 0,49. HUELLA no mide nada aquí: ningún texto de ninguno de los
  dos lados traía rayas ni comillas tipográficas. VOZ castiga a los humanos
  divulgativos (37 de mediana) por escribir en tercera persona y sin
  coletillas; separa porque a la IA la castiga más (25).
- La señal más clara ya estaba en `slop.json`: el preámbulo "en este vídeo"
  sale en 115 de los 180 textos de IA y en 11 de los 36 humanos. La tríada no
  separa: 6 % de los textos de IA y 8 % de los humanos.
- `humanize.py` cambió 65 de los 180 textos de IA y subió su nota 6,5 puntos
  de media. De esos 65, los MARCADO bajaron de 56 a 45, y ninguno llegó a
  APTO. Uno de sus cambios, "descubre cómo" -> "mira cómo", le regala unos 4
  puntos de VOZ, porque el detector cuenta "mira" como coloquial: el
  humanizador se puntúa a sí mismo. Es poco y queda anotado.

**Lo que cambié en `slop.json`, y con qué evidencia:** dos estructuras nuevas,
sacadas de una primera tanda de 36 textos que escribí yo (Claude Opus 5.5)
antes de tener los de los otros cinco modelos. "Descubre", "descubrirás" y
"descubriremos" salen en 80 de los 180 textos de esos modelos y en ningún
humano. El índice en primera del plural ("veremos", "exploramos",
"analizamos") sale en 80 de 180 y en 2 de 36 humanos. Juntas suben el AUC de
0,71 a 0,75, y lo suben en los cinco modelos, sin marcar a ningún humano más.
Eso es validarlas fuera de la muestra en que se escribieron. Mis 36 textos,
que se escribieron después de leer `detect.py`, eran los más difíciles: AUC
0,62 antes del cambio y 0,66 después.

**Lo que no cambié, porque no hay evidencia:** quitar la tríada sube el AUC
0,002. Que una comprobación "demasiado corta para juzgar" valga 50 le cierra
el APTO a 13 de los 36 humanos, pero sacarla del cálculo deja 2 humanos APTO
frente a 1 de la IA. No arregla nada.

Los límites pesan. El género es la descripción divulgativa de YouTube, no el
caption personal de Instagram: en captions en primera persona, VOZ puede
portarse distinto, y "veremos" o "descubre" quizá salgan menos. Y 36 textos
humanos son pocos. Lo que sí sostiene es esto: sirve para ver qué arreglar (la
comprobación más floja, las palabras que lista), no para dictaminar si un
texto parece humano.

**Lo que sigue sin medir:**

- `detect.py` con captions de Instagram en primera persona escritos por
  personas.
- Los subtítulos automáticos no llevan mayúsculas y destrozan cifras ("1,000€n
  de€"), así que CONCRECIÓN infravalora los ganchos transcritos. Con lo que tú
  escribes no pasa.
- 80 ganchos de cinco canales sostienen "caza los malos" y "no elige
  ganadores". No sostienen nada más fino.

Si lo repites con un corpus mayor y te sale otra cosa, prefiero saberlo. El
script de medición no está en el repo porque depende de `yt-dlp`, pero el
método está en [`/ig-viral`](skills/ig-viral/SKILL.md).

## La letra pequeña

Vale todo lo del README inglés, y conviene repetirlo:

- **Estas skills no publican en Instagram.** Todo lo que se usa para
  automatizar publicaciones, comentarios, follows o DM es automatización del
  navegador o una herramienta de terceros, y las dos incumplen las
  [Condiciones de uso de Instagram](https://help.instagram.com/581066165581870)
  y hacen que bloqueen cuentas. Cada skill acaba con un bloque listo para
  copiar, y lo publicas tú.
- **`/ig-viral` lee, no hace scraping.** Diez cuentas, una docena de reels cada
  una, a velocidad humana, contigo manejando tu propio navegador. Nunca pide tu
  contraseña.
- **Las cinco comprobaciones del detector son heurísticas locales**, no
  GPTZero, Originality, Copyleaks, Winston ni Turnitin. No llaman a esos
  servicios y no pueden prometer su veredicto. Nadie puede venderte
  "indetectable" con honestidad.
- **No se inventa nada.** Si un borrador necesita una cifra que no has dado,
  vuelve con `{{tu cifra}}` dentro y un aviso.
- **Los números de la plataforma caducan.** Si algo de aquí contradice lo que
  hace Instagram cuando lo leas, Instagram tiene razón.

## Archivos

```
skills/ig-reel/hooks.json          26 fórmulas de gancho en español: plantilla, ejemplo,
                                   versión en pantalla, para qué sirve, cómo se estropea y regex
skills/ig-reel/hookscore.py        el panel de cinco propiedades del gancho (sílabas, persona por verbo)
skills/ig-reel/beats.py            del guion a la escaleta con tiempos, por sílabas
skills/ig-caption/caption.py       la vista previa del corte y el revisor de captions
skills/ig-human/slop.json          el léxico: 266 términos, 18 clases invisibles, 19 señales
skills/ig-human/humanize.py        las tres pasadas de limpieza
skills/ig-human/detect.py          el panel de cinco comprobaciones
skills/ig-viral/swipe.py           orden por múltiplo y clasificación por fórmula
skills/ig-profile/rubric.json      la nota del perfil sobre 100
templates/voice.md                 tu perfil de voz, con variante y trato. Rellénalo primero.
```

## Créditos

Pack original de **Jake Schincariol**, [opusjake.ai](https://opusjake.ai), en
[Jakeschincariol/instagram-agent-skill](https://github.com/Jakeschincariol/instagram-agent-skill),
con licencia MIT. Las skills, su diseño y el pack en inglés son suyos.

Variante en español adaptada a partir de él por
[koridenugceu-tech](https://github.com/koridenugceu-tech), en este fork.

## Licencia

MIT. Cógelo, cámbialo, publícalo.
