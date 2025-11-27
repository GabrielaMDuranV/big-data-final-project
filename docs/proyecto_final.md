# ANÁLISIS DE DATOS CENSALES PARA DETERMINAR LA UBICACIÓN ÓPTIMA Y NECESARIA DE CENTROS EDUCATIVOS EN BOLIVIA

## 1. Introducción
La planificación urbana y la asignación eficiente de recursos públicos son pilares fundamentales para el desarrollo social y económico de cualquier país. En este contexto, la educación se erige como un derecho básico y un motor de movilidad social, cuya accesibilidad depende de una infraestructura educativa bien distribuida. La era del Big Data permite transformar datos censales en decisiones estratégicas para reducir desigualdades y orientar inversiones educativas con mayor precisión.

## 2. Justificación

### Perspectiva Big Data
Los datos censales poseen gran **volumen**, **variedad** y requieren **velocidad** de procesamiento, manteniendo **veracidad** y generando alto **valor** para la planificación.

### Justificación Técnica
Se emplearon tecnologías como Apache Spark, HDFS/S3, GeoPandas, modelos de clustering y optimización para analizar brechas educativas y localizar puntos óptimos.

### Justificación Social
Una adecuada distribución de escuelas reduce desigualdades, mejora acceso y seguridad, y fortalece el bienestar comunitario.

### Justificación Económica
Una infraestructura mal ubicada genera costos altos y bajo impacto. Este análisis optimiza la inversión pública.

## 3. Planteamiento del Problema
La infraestructura educativa no se adapta con suficiente rapidez a los cambios demográficos, generando escuelas saturadas o subutilizadas. La falta de herramientas basadas en datos perpetúa estas desigualdades.

## 4. Objetivos de Investigación

### Objetivo General
Desarrollar un modelo basado en Big Data que identifique las zonas óptimas para nuevos centros educativos.

### Objetivos Específicos
- Recopilar y limpiar datos censales y educativos.
- Geocodificar direcciones.
- Analizar densidades y brechas.
- Aplicar algoritmos de optimización.
- Visualizar resultados mediante dashboards y mapas interactivos.

## 5. Fuentes de Datos
- Censo Nacional de Población y Vivienda.
- Encuestas de Hogares.
- Registro Nacional de Instituciones Educativas.
- Cartografía geográfica oficial.

## 6. Cronograma (4 meses)
- **Mes 1:** Adquisición, limpieza y geocodificación.
- **Mes 2:** Análisis exploratorio y modelos.
- **Mes 3:** Validación y dashboards.
- **Mes 4:** Informe final y presentación.

## 7. Relación con las 5V del Big Data
- **Volumen:** datos masivos.
- **Variedad:** tablas, texto, geodatos.
- **Velocidad:** análisis paralelo.
- **Veracidad:** fuentes oficiales.
- **Valor:** decisiones de alto impacto.

---

# SECCIONES ADICIONADAS

## Introducción (Ampliada)
El uso estratégico de datos masivos permite detectar patrones invisibles a la intuición y construir una planificación educativa basada en evidencia real, reduciendo brechas históricas.

## Historia de los Datos
Los datos provienen de censos nacionales, registros educativos oficiales, cartografía base y encuestas complementarias. Todas las fuentes poseen validez institucional.

## Arquitectura Técnica y Flujo ETL

### Flujo del Proceso
```
FUENTES DE DATOS
   - Censo
   - Escuelas
   - Cartografía
   - Encuestas
        ↓
ADQUISICIÓN DE DATOS
        ↓
PROCESO ETL (Limpieza)
   - Eliminación de duplicados
   - Valores faltantes
   - Normalización
   - Validación de rangos
   - Estandarización de direcciones
   - Geocodificación
        ↓
INTEGRACIÓN FINAL
        ↓
ANÁLISIS Y MODELOS
```

## Insights Clave del Proyecto
1. **Crecimiento periurbano acelerado** donde la oferta educativa no acompaña el aumento poblacional.
2. **Desbalance rural**, con centros saturados y otros subutilizados.
3. **Zonas óptimas identificadas**, seleccionadas mediante modelos de optimización P-Mediano.

---

# Impacto Social y Cierre
Este proyecto aporta a la equidad educativa al identificar con precisión las áreas que requieren con mayor urgencia infraestructura escolar. Esto garantiza que la inversión pública genere el mayor impacto social, beneficiando a miles de familias y mejorando el acceso a una educación digna.

**Frase final:**  
**"Transformar números en decisiones es transformar el futuro de miles de estudiantes."**
