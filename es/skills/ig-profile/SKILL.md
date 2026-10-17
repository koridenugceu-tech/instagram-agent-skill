---
name: ig-profile
description: >-
  Puntúa un perfil de Instagram sobre 100 con una rúbrica de 12 partes y
  reescribe en español lo que pierde puntos: campo de nombre, bio, enlace,
  destacadas, los tres fijados y la cuadrícula. Úsala cuando el usuario diga
  "optimiza mi perfil", "arregla mi bio", "puntúa mi Instagram", "por qué no
  me sigue la gente", o pegue su perfil y pregunte cómo se lee.
---

# ig-profile

Casi todo el mundo optimiza aquí lo que no es. El perfil no es un escaparate
por el que se pasea. Es una **pantalla de decisión** a la que se llega desde un
reel, y tiene unos tres segundos para responder a una pregunta: ¿hay más de
eso aquí, y es para mí?

## Entrada

Pide al usuario que pegue o haga captura de: el campo de nombre, el @, la bio,
a dónde lleva el enlace, los nombres de las destacadas, lo que está fijado y
las nueve primeras portadas de la cuadrícula. Una captura de la parte de arriba
del perfil más las dos primeras filas de la cuadrícula basta para una primera
pasada.

No inicies sesión en Instagram en su nombre.

## Puntúalo

Lee `rubric.json` en esta carpeta. Doce apartados, 100 puntos, cada uno con lo
que es la nota máxima y cómo suele fallar. Puntúa todos, enseña la tabla, da el
total. Sé honesto. La mayoría de perfiles sacan entre 30 y 49 en la primera
pasada, y una nota generosa no le sirve a nadie.

```
NOTA DEL PERFIL  38/100

  campo de nombre   2/12   solo el nombre, ni una palabra que alguien busque
  primera línea     3/12   tres sustantivos y un emoji de café
  tres fijados      0/10   nada fijado
  destacadas        2/8    "Random", "Vida", "2023"
  cuadrícula        4/8    seis de nueve portadas son una cara a media frase
  ...
```

## Luego reescribe, en este orden

Arregla de más a menos puntos perdidos. No lo reescribas todo de golpe: el
usuario tiene que ir a cambiar cada cosa.

**1. El campo de nombre (30 caracteres).** La línea en negrita debajo de la
foto, no el @. Es el campo con el que coincide el buscador de Instagram, y casi
todas las cuentas ponen un nombre y nada más. Formato que funciona:
`{Nombre} | {qué haces, con las palabras que se buscan}`. Da tres opciones. En
español los términos son largos: "Lucía Gómez | Contratos freelance" ya son 33
caracteres. Recorta el apellido antes que el término.

**2. Primera línea de la bio.** Para quién es y qué le cambia. No un cargo, no
adjetivos, no una lista de identidades separadas por barras. El resto de los
150 caracteres lleva una prueba o una oferta clara.

**3. Los tres fijados.** Tres huecos, tres trabajos: la mejor prueba, la
explicación más clara de la oferta y la mejor presentación de la persona. Es el
arreglo con más impacto de todo el perfil y son cuatro toques. Una cuadrícula
sin fijados enseña lo último que se publicó, que es tirar una moneda.

**4. Destacadas.** De cuatro a seis, con el nombre de las preguntas que hace un
comprador: Precios, Resultados, Cómo funciona, Sobre mí. No "Random". Borra el
resto. Ojo con el límite de caracteres del nombre de la destacada: "Cómo
funciona" se corta en algunos móviles; "Proceso" no.

**5. El enlace.** Un destino que encaje con lo que acaba de prometer la bio. Se
permiten cinco; con dos ya es un menú, y un menú convierte peor que una puerta.

**6. Portadas de la cuadrícula.** Las nueve primeras en miniatura. Las
portadas de los reels se eligen, no se dejan en el fotograma uno. Cuatro
palabras de texto en una portada hacen que la cuadrícula se lea de un vistazo.

## Salida

Tabla de notas, luego las reescrituras como bloques listos para copiar en
orden de arreglo, cada una pasada por `/ig-human`. Vuelve a puntuar al final y
enseña la diferencia con honestidad. Si la reescritura llega a 84 y no a 98, di
84, y di qué falta, que suele ser una cuadrícula, un hábito de stories y un
post fijado que todavía no existe. Nada de eso es una reescritura.

Esta skill no guarda nada en Instagram. El usuario edita cada campo.
