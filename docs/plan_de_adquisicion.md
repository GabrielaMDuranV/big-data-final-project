# Plan de Adquisición de Datos

## Fuentes Principales
1. **INE Bolivia** - Censo Nacional de Población y Vivienda 2024
   - Modalidad: Descarga directa desde portal oficial
   - Formato: CSV/Excel con datos anonimizados
   - Frecuencia: Una vez (datos estáticos del censo)

## Estrategia de Adquisición
### Fase 1: Obtención Inicial
- Descarga masiva de microdatos censales
- Verificación de integridad y completitud
- Almacenamiento en formato original en `data/raw/`

### Fase 2: Actualizaciones
- Los datos censales son estáticos por 10 años
- Posible integración con proyecciones poblacionales anuales del INE
- Considerar APIs del INE para datos complementarios

## Metadatos y Documentación
- Conservar diccionarios de variables originales
- Documentar transformaciones aplicadas
- Mantener trazabilidad de fuentes y versiones

## Consideraciones Legales y Éticas
- Uso exclusivo de datos anonimizados y de acceso público
- Respeto a políticas de uso de datos del INE
- No incluir información personal identificable