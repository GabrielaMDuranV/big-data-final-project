# Análisis de Datos Censales para Determinar la Ubicación Óptima de Centros Educativos en Bolivia

## Descripción del Proyecto
Proyecto de análisis espacial basado en datos del **Censo de Población y Vivienda 2012** (Bolivia), cuyo objetivo es identificar **ubicaciones óptimas para la construcción de nuevos centros educativos**, integrando variables sociodemográficas, educativas y de accesibilidad para **maximizar la cobertura de la población en edad escolar**.  

Este proyecto utiliza técnicas de **Big Data y análisis geoespacial** para apoyar la planificación educativa y la toma de decisiones basada en evidencia.

---

## Objetivos

### **Objetivo General**
Desarrollar un análisis espacial basado en datos censales que permita identificar ubicaciones óptimas para la construcción o redistribución de centros educativos en Bolivia.

### **Objetivos Específicos**
- Identificar y georreferenciar la población en edad escolar (4–17 años) a nivel de unidades censales, manzanas y municipios.
- Analizar la **oferta educativa existente** (ubicación y capacidad de las unidades educativas).
- Evaluar la **accesibilidad educativa** considerando distancias y tiempos de desplazamiento.
- Identificar **zonas de vulnerabilidad socioeducativa** mediante un índice compuesto de condiciones de vida y nivel educativo familiar.
- Modelar **escenarios de ubicación óptima** utilizando algoritmos de optimización espacial (p-median, cobertura máxima).

---

## Flujo del Proyecto

1. **ETL y Limpieza de Datos:**  
   Importar, filtrar y estandarizar los datos censales, eliminando inconsistencias y valores nulos.
2. **Análisis Exploratorio Espacial:**  
   Detectar patrones de concentración de población escolar, brechas de acceso y zonas desatendidas.
3. **Modelado de Accesibilidad y Optimización:**  
   Aplicar modelos de localización para proponer ubicaciones óptimas de nuevos centros educativos.
4. **Validación y Visualización:**  
   Generar mapas temáticos, gráficos y reportes para la interpretación y comunicación de resultados.

---

## Justificación del Enfoque Aplicado

### **1. Análisis Exploratorio + Descriptivo**
- **Por qué:** Permite comprender la distribución espacial de la población escolar y la cobertura educativa.  
- **Herramientas:** `pandas`, `geopandas`, `matplotlib`, `JupyterLab`.  
- **Arquitectura:** notebooks para análisis y scripts reproducibles en `src/transform.py`.  
- **Reproducibilidad:** uso de `environment.yml`, control de versiones y almacenamiento en formato Parquet.

### **2. Optimización Espacial (Prescriptivo)**
- **Por qué:** Permite tomar decisiones concretas sobre dónde ubicar escuelas para maximizar cobertura.  
- **Herramientas:** `pulp`, `ortools`, `geopandas`, `osmnx`.  
- **Arquitectura:** módulo `src/model_opt.py` que genera escenarios de ubicación óptima.  
- **Reproducibilidad:** parámetros configurables en `config.yaml` y registro de resultados versionados.

### **3. Predictivo **
- **Por qué:** Estimar demanda futura o crecimiento poblacional.  
- **Herramientas:** `scikit-learn`, `xgboost`, `prophet`.  
- **Arquitectura:** módulo `src/predict.py` para escenarios futuros (optimista, medio, pesimista).  
- **Reproducibilidad:** documentación de supuestos y evaluación de modelos con métricas (MAE, RMSE).

---

## Tecnologías
- **Lenguaje:** Python  
- **Bibliotecas principales:**  
  - `pandas`, `numpy`, `geopandas`, `matplotlib`, `PySAL`, `scikit-learn`, `osmnx`, `pulp`, `ortools`  
- **Entorno de trabajo:** Miniconda + JupyterLab  
- **Visualización:** `plotly`, `folium`, `Kepler.gl`  

---

## Variables Principales

| Categoría | Variable | Tipo | Uso en el Proyecto | Justificación |
|------------|-----------|------|--------------------|----------------|
| Demográfica | Edad (_AGE) | Numérica continua | Calcular demanda educativa por nivel | Determina población escolar |
| Demográfica | Sexo (_SEX) | Categórica nominal | Análisis por género | Detectar brechas educativas |
| Geográfica | Coordenadas | Espacial | Georreferenciación de viviendas/escuelas | Cálculo de distancias |
| Educativa | Asistencia escolar | Binaria | Identificar población fuera del sistema | Indicador directo de déficit |
| Vivienda | Acceso a agua/energía/internet | Binaria | Índice de vulnerabilidad | Refleja desigualdades socioeducativas |
| Infraestructura | Capacidad de aulas | Numérica discreta | Evaluar saturación de escuelas | Planificar ampliaciones o nuevas construcciones |

---


## Créditos

**Estudiante:** Gabriela Micaela Durán Villafán  
**Asignatura:** Big Data  
**Docente:** Ing. Enrique Laurel  
**Universidad Privada Franz Tamayo — UNIFRANZ**  
**La Paz, Bolivia – 2025**
