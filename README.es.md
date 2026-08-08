# 🔮 Nostradamus

### Un motor determinista de predicción de enfrentamientos deportivos

**Nostradamus** es un proyecto de predicción deportiva diseñado para predecir **qué equipos o jugadores se enfrentarán durante una competición**.

A diferencia de los modelos tradicionales de predicción deportiva, Nostradamus no busca principalmente predecir los ganadores de los partidos. Su objetivo es anticipar la estructura de los enfrentamientos futuros a partir de las reglas oficiales de las competiciones, los datos disponibles y mecanismos de predicción deterministas.

El proyecto lleva el nombre de **Michel de Nostredame (Nostradamus)**, médico y boticario francés conocido principalmente por sus profecías. Sin embargo, en este caso, las predicciones de Nostradamus se basan en datos, razonamiento matemático, reglas oficiales y métodos reproducibles.

---

## 🎯 Objetivo

El objetivo principal de Nostradamus es predecir los **posibles enfrentamientos dentro de competiciones deportivas que incluyen un sorteo o un mecanismo similar**.

Actualmente, el proyecto se centra en dos deportes:

- ⚽ **Fútbol masculino**
- 🎾 **Tenis femenino**

El objetivo no es simplemente generar predicciones independientes. Nostradamus debe producir **predicciones globalmente coherentes**, respetando las reglas y las restricciones estructurales de cada competición.

---

## 🌍 Alcance del proyecto

Nostradamus se centra en competiciones para las que la predicción de los futuros enfrentamientos constituye un problema de predicción interesante.

### ⚽ Fútbol

La parte de fútbol se centra inicialmente en las principales competiciones internacionales que incluyen un sorteo.

El alcance actual comprende:

- UEFA Champions League
- Copa Africana de Naciones (CAN)
- Campeonato de Europa de la UEFA (EURO)
- Copa Mundial de la FIFA

La primera competición objetivo de Nostradamus es la **UEFA Champions League**.

Para la fase de liga de la Champions League, Nostradamus tiene como objetivo predecir los ocho rivales a los que se enfrentará cada uno de los 36 equipos participantes, así como la configuración de local/visitante.

Al finalizar la fase de liga, el proyecto también podrá predecir los posibles recorridos en las fases eliminatorias a partir de la clasificación final y de los siguientes sorteos.

### 🎾 Tenis femenino

La parte de tenis se centra en los principales torneos **WTA** que incluyen un sorteo.

El alcance inicial comprende:

- Torneos WTA 500
- Torneos WTA 1000
- Torneos de Grand Slam

Para cada torneo, Nostradamus tiene como objetivo predecir los primeros enfrentamientos, así como los posibles recorridos de las jugadoras a lo largo del torneo.

La parte de tenis podrá tener en cuenta, entre otros elementos:

- los cambios en la clasificación
- las bajas de jugadoras
- las wildcards
- otros cambios relevantes que se produzcan antes del sorteo

---

## ⚙️ Funcionamiento de Nostradamus

Nostradamus está diseñado para funcionar como una persona que realiza un sorteo respetando todas las reglas aplicables a la competición.

### Fútbol

Para la fase de liga de la Champions League, Nostradamus tiene como objetivo:

1. Identificar los equipos participantes.
2. Determinar la información y las restricciones relevantes de la competición.
3. Generar una predicción de los ocho rivales de cada equipo.
4. Determinar la configuración de local/visitante.
5. Comprobar que la predicción completa sea globalmente coherente.
6. Después de la fase de liga, utilizar la clasificación final y la información de los siguientes sorteos para generar los posibles recorridos de las fases eliminatorias.

### Tenis femenino

Para cada torneo seleccionado, Nostradamus tiene como objetivo:

1. Identificar a las participantes previstas.
2. Tener en cuenta la información relevante de clasificación.
3. Tener en cuenta las bajas, wildcards y otros cambios relevantes.
4. Generar una predicción de los primeros enfrentamientos.
5. Generar los posibles recorridos de las jugadoras en el torneo.

---

## 🧠 Principios fundamentales

### Predicciones deterministas

Nostradamus está diseñado para ser **determinista**.

A partir del mismo conjunto de datos, los mismos parámetros y las mismas reglas, Nostradamus debe producir **la misma predicción**.

No se debe generar una nueva predicción hasta que un cambio en la información disponible modifique los datos o parámetros utilizados por el sistema.

Este principio es conceptualmente similar al uso de un `random_state` fijo en un experimento de machine learning: entradas idénticas deben producir salidas idénticas.

El objetivo no es generar una predicción diferente cada vez que se ejecuta el programa, sino producir **una predicción reproducible para un estado determinado de la información disponible**.

### Principio de coherencia de los sorteos

Nostradamus respeta un **principio de coherencia de los sorteos**.

Un enfrentamiento predicho no puede considerarse de forma independiente de la predicción realizada para el adversario.

Por ejemplo, si Nostradamus predice:

> Paris Saint-Germain → Liverpool, jornada 4, local

la predicción correspondiente debe ser automáticamente:

> Liverpool → Paris Saint-Germain, jornada 4, visitante

La predicción completa debe, por tanto, mantenerse **globalmente coherente**.

Este principio es fundamental para Nostradamus: el sistema no genera una colección de predicciones independientes, sino **una predicción coherente de la estructura de la competición**.

### Reglas oficiales de las competiciones

Nostradamus se basa en las reglas oficiales que regulan cada competición.

Las restricciones específicas de cada competición constituyen requisitos fundamentales del proceso de predicción.

El uso de machine learning solo se considerará cuando aporte un valor real al problema de predicción. Nostradamus no tiene como objetivo utilizar machine learning simplemente por utilizar machine learning.

### Explicabilidad

Nostradamus tiene como objetivo producir resultados **comprensibles y accesibles**, en lugar de predicciones opacas.

Las predicciones finales deben presentarse de manera clara y legible.

---

## 🔮 Visión a largo plazo

A largo plazo, Nostradamus tiene como objetivo convertirse en un **motor de predicción deportiva** capaz de seguir continuamente la información relevante relacionada con las competiciones.

Idealmente, Nostradamus generaría una predicción para un estado determinado de una competición y mantendría dicha predicción hasta que se produjera un evento relevante.

Estos eventos pueden incluir, entre otros:

- bajas de jugadoras
- cambios en la clasificación
- wildcards
- cambios que afecten a la estructura de la competición

Cuando la información relevante cambie, Nostradamus podría generar una nueva predicción a partir del estado actualizado de la información.

Una versión futura también podría notificar a los usuarios cuando un evento importante provoque el recalculo de una predicción.

---

## 🚧 Estado del proyecto

Nostradamus se encuentra actualmente en la **fase de diseño y desarrollo inicial**.

La primera implementación se centra en la parte de fútbol y, más concretamente, en la UEFA Champions League.

Las prioridades actuales son:

- definir los datos necesarios
- identificar fuentes de datos fiables
- recopilar datos históricos de las competiciones
- documentar las reglas oficiales de las competiciones
- traducir las reglas de las competiciones en restricciones informáticas
- diseñar el mecanismo de predicción determinista
- desarrollar el primer prototipo de fútbol

Todavía no se ha implementado ningún motor de predicción final.

---

## 🗺️ Hoja de ruta

### Fase 0 — Definición del proyecto
- [x] Definir el concepto del proyecto
- [x] Definir el alcance del proyecto
- [x] Definir los principios fundamentales
- [x] Definir la filosofía de predicción determinista
- [x] Definir el principio de coherencia de los sorteos

### Fase 1 — Datos y reglas del fútbol
- [x] Definir los datos necesarios
- [ ] Identificar las fuentes de datos
- [ ] Recopilar datos históricos de las competiciones
- [ ] Documentar las reglas de la competición UEFA
- [ ] Traducir las reglas en restricciones informáticas

### Fase 2 — Motor de predicción de fútbol
- [ ] Diseñar el mecanismo de predicción
- [ ] Implementar el mecanismo de sorteo determinista
- [ ] Implementar la coherencia de los sorteos
- [ ] Gestionar las restricciones de local/visitante
- [ ] Validar las predicciones utilizando sorteos históricos

### Fase 3 — Predicción de la Champions League
- [ ] Generar una predicción antes del sorteo oficial
- [ ] Comparar la predicción de Nostradamus con el sorteo oficial
- [ ] Analizar la precisión y las limitaciones de la predicción

### Fase 4 — Fases eliminatorias
- [ ] Modelizar los sorteos de las fases eliminatorias
- [ ] Predecir los posibles recorridos
- [ ] Integrar la clasificación final de la fase de liga
- [ ] Extender la predicción hasta la final

### Fase 5 — Tenis femenino
- [ ] Definir las necesidades de datos para el tenis
- [ ] Identificar las fuentes de datos WTA
- [ ] Modelizar las restricciones específicas de los sorteos de los torneos
- [ ] Desarrollar el primer motor de predicción de tenis
- [ ] Probar el enfoque en torneos históricos

### Futuro
- [ ] Desarrollar una interfaz de usuario
- [ ] Implementar actualizaciones de las predicciones en función de los eventos
- [ ] Añadir notificaciones de predicción
- [ ] Explorar otros deportes y competiciones

---

## 🛠️ Tecnologías

La stack tecnológica de Nostradamus no está deliberadamente fijada al comienzo del proyecto.

Las decisiones tecnológicas se tomarán en función de las necesidades identificadas durante el desarrollo.

Las tecnologías potenciales pueden incluir:

- Python
- Bibliotecas de procesamiento y análisis de datos
- Métodos matemáticos y probabilísticos
- Machine learning, cuando sea pertinente
- Docker para un despliegue reproducible
- Una interfaz web para futuras versiones

---

## 👩🏾‍💻 Autora

**Lorame Bakaboula**

Nostradamus es un proyecto personal diseñado, desarrollado y documentado por Lorame Bakaboula.

El proyecto pretende documentar no solo el resultado final, sino también el **proceso de investigación, experimentación, recopilación de datos y desarrollo** que se encuentra detrás del motor de predicción.

---

## 📄 Licencia

Consulta el archivo [`LICENSE`](LICENSE) para obtener información sobre la licencia del proyecto.