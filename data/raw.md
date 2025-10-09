# Datos Crudos - Censo Nacional 2024

## Fuentes de Datos Primarios
- **Fuente Principal**: Instituto Nacional de Estadística (INE) - Censo Nacional de Población y Vivienda 2024
- **Tipo**: Datos estructurados en formato tabular
- **Volumen estimado**: 10 millones de registros (población boliviana) × 80+ variables
- **Características**: Datos anonimizados a nivel individual, agregables por manzana, barrio, distrito, municipio

## Variables Principales
- **Demográficas**: _AGE, _SEX, _URBAN
- **Socioeconómicas**: _EDATTAIN, _WALL, _ROOF, _FLOOR  
- **Tecnología y Bienes**: _COMPUTER, _INTERNET, _AUTO, _MOTORCYC
- **Servicios**: _WATSRC, _TOILET, _SEWAGE, _ELECTRIC
- **Movilidad**: _TRANS
- **Hogar**: _ROOMS, _BEDROOMS, _OWNERSHIP

## Estructura Esperada de Archivos
- `censo_2024_poblacion.csv` - Datos individuales de población
- `censo_2024_vivienda.csv` - Datos de características de viviendas
- `diccionario_variables.pdf` - Documentación de variables y categorías