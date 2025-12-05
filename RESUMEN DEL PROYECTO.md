# 📝 Resumen General del Proyecto  
## Análisis de Datos Censales para Centros Educativos en Bolivia

El proyecto propone un modelo analítico basado en **Big Data** para optimizar la planificación de la infraestructura educativa en Bolivia a nivel estratégico.

---

## 🎯 Objetivo Principal
Identificar, mediante un **índice de priorización departamental**, los nueve departamentos de Bolivia con la mayor necesidad de inversión para la construcción de nuevos centros educativos.

---

## 💡 Problema Identificado
La planificación educativa actual a menudo es lenta e inexacta frente a los cambios demográficos, lo que resulta en una distribución desequilibrada de la oferta educativa. Esto se manifiesta en:

- Subutilización de recursos en departamentos donde la demanda ha decrecido.  
- Carencia de establecimientos y largos desplazamientos para estudiantes en departamentos con reciente crecimiento poblacional.  
- Insuficiente cobertura en áreas periféricas o con población dispersa.

---

## 📊 Metodología y Alcance
El proyecto se centra en un enfoque **macro a nivel departamental**, evitando el análisis a nivel municipal o de coordenadas específicas.

### 1. Fuentes de Datos
- **Censo Nacional de Población y Vivienda (CPV):** Datos demográficos, composición por edad y población en edad escolar.  
- **Registro Nacional de Instituciones Educativas (Ministerio de Educación):** Inventario oficial de unidades educativas y métricas de capacidad (la variable de oferta).  
- **Órgano Electoral Plurinacional (OEP):** Conteo actualizado de recintos (colegios) por departamento.

### 2. Indicadores Clave
Los datos se integran utilizando el **departamento** como clave de unión para calcular indicadores como:

- Población en edad escolar por departamento.  
- Número total de unidades educativas por departamento.  
- **Ratio Alumno/Escuela:** población en edad escolar ÷ número de escuelas.  
- Densidad de población en edad escolar por kilómetro cuadrado.  
- Diferencia entre el ratio alumno/escuela departamental y el promedio nacional.

### 3. Proceso y Herramientas
El flujo de trabajo es secuencial y reproducible, utilizando herramientas de código abierto como **Python**, **pandas** y **matplotlib**.

- **Adquisición y Almacenamiento:** Descarga de datos oficiales del INE y el Ministerio de Educación.  
- **Transformación y Limpieza (ETL):** Depuración de inconsistencias y estandarización.  
- **Análisis y Modelado:** Cálculo del **Índice de Priorización** (score o ranking compuesto de indicadores normalizados).  
- **Visualización y Despliegue:** Creación de un dashboard interactivo con el ranking, gráficos y un mapa temático de Bolivia para la toma de decisiones.

---

## 🔑 Hallazgos Esperados
Se espera que el análisis revele:

- **Disparidades Interdepartamentales:** Ratios alumno/escuela significativamente más altos en departamentos urbanos de alta densidad (p. ej., La Paz, Cochabamba) o de alta dispersión (p. ej., Pando, Beni).  
- **Déficits Relativos:** Identificación de posibles “desiertos educativos” a nivel departamental.  
- **Ranking de Priorización:** Potencial señalamiento de La Paz, Santa Cruz y Cochabamba como los departamentos de mayor necesidad de inversión en infraestructura escolar.

---

## 🚧 Límites del Proyecto
El principal límite es el **nivel de agregación departamental**, lo que impide identificar necesidades específicas a nivel municipal o de micro-localización de escuelas. Además, al no usar coordenadas, los indicadores de accesibilidad son **proxies** (densidad y ratio) y no miden distancias reales de viaje.


## Créditos

**Estudiante:** Gabriela Micaela Durán Villafán  
**Asignatura:** Big Data  
**Docente:** Ing. Enrique Laurel  
**Universidad Privada Franz Tamayo — UNIFRANZ**  
**La Paz, Bolivia – 2025**
