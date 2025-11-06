# 🧾 Documentación del Proceso de Limpieza de Datos del Censo

---

## Resumen 

Este documento presenta el proceso de limpieza, selección y estandarización de datos censales utilizados en el análisis poblacional.  
El objetivo principal fue estructurar la información censal para obtener variables relacionadas con:

- La **población total por departamento**  
- La **cantidad de personas y su distribución por sexo**  
- La **cantidad de niños agrupados por edades**

Este proceso permitió preparar los datos para posteriores análisis estadísticos y visualizaciones que apoyen la toma de decisiones basadas en evidencia.

---

##  Fuente de Datos

- **Fuente original:** <Nombre de la institución o enlace al dataset>  
- **Año del Censo:** <Año>  
- **Formato del archivo:** <CSV>  
- **Descripción:**  
  Conjunto de datos proveniente del Censo Nacional, donde cada registro representa a un individuo censado y cada columna corresponde a una variable censal (edad, sexo, departamento, entre otras).

---

##  Variables Seleccionadas

| Variable | Descripción | Tipo | Observaciones |
|-----------|--------------|------|----------------|
| `DEPARTAMENTO` | Identificador o nombre del departamento | Categórica | Utilizada para agrupar la población |
| `SEXO` | Sexo del individuo | Categórica (codificada) | 1 = Hombre, 2 = Mujer |
| `EDAD` | Edad del individuo | Numérica | Usada para clasificar por grupos etarios |
| `POBLACION` | Conteo  de personas | Numérica | Suma de individuos por departamento |

---

## Proceso de Limpieza de Datos

1. **Importación y exploración inicial**  
   - Se importó el archivo utilizando `pandas`.  
   - Se revisó la estructura mediante `.info()` y `.head()`.

2. **Selección de columnas relevantes**  
   - Se filtraron las variables necesarias (`DEPARTAMENTO`, `SEXO`, `EDAD`, `POBLACION`).

3. **Tratamiento de valores faltantes y duplicados**  
   - Se eliminaron registros incompletos y duplicados.  
   - Se verificó la coherencia de los tipos de datos.

4. **Estandarización de códigos censales**  
   - `SEXO`: 1 = Hombre, 2 = Mujer  
   - `DEPARTAMENTO`: según el catálogo oficial  
   - `EDAD`: agrupada en intervalos (0–5, 6–12, 13–17, 18–64, 65+)

5. **Exportación del dataset limpio**  
   - Archivo resultante:  
     ```
    censo2024.csv
     ```

---

##  Interpretación de Códigos

| Variable | Código | Significado |
|-----------|---------|-------------|
| `SEXO` | 1 | Hombre |
| `SEXO` | 2 | Mujer |
| `EDAD` | 0–5 | Niños pequeños |
| `EDAD` | 6–12 | Niños en edad escolar |
| `EDAD` | 13–17 | Adolescentes |
| `EDAD` | 18–24 | Adultos |
| `DEPARTAMENTO` | Según catálogo | Nombre del departamento |

---

##  Resultados Generales

- **Registros finales:** `<número>`  
- **Departamentos analizados:** `<número>`  
- **Promedio de edad:** `<valor>`  
- **Distribución por sexo:**  
  - Hombres: `<porcentaje>%`  
  - Mujeres: `<porcentaje>%`  
- **Distribución etaria:**  
  - 0–17 años: `<porcentaje>%`  
 

---

## Herramientas Utilizadas

- **Lenguaje:** Python 
- **Bibliotecas:**  
  - `pandas` – Limpieza y manipulación de datos  
  - `numpy` – Operaciones numéricas  
  - `matplotlib` / `seaborn` – Visualización  
- **Entorno:** Jupyter / Visual Studio Code  


