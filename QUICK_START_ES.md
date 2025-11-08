# Habilidades de Ingeniería de Contexto DSGS - Guía Rápida (Spanish)

## Resumen del Proyecto

DSGS (Dynamic Specification Growth System) Context Engineering Skills es una herramienta profesional de desarrollo asistido por IA diseñada específicamente para plataformas CLI de IA, que proporciona análisis de contexto, optimización y capacidades de plantillas cognitivas con flujo de trabajo de seguridad de IA.

## Mejoras Principales

### 1. Arquitectura de Habilidades Unificada
- **Implementación Consolidada**: Las habilidades de modo estándar y mejorado combinadas en una sola implementación
- **Alternancia de Modo**: Usa el parámetro `mode` para controlar el nivel de funcionalidad ('standard' o 'enhanced')
- **Interfaz Única**: Interfaz simplificada que evita funcionalidad duplicada

### 2. Estructura de Directorio Plana
- **Una Habilidad Por Directorio**: Cada habilidad en su propio directorio, sin anidamiento innecesario
- **Organización Simplificada**: Colocación intuitiva de habilidades, mantenimiento más sencillo
- **Reducida Confusión**: Límites claros de habilidades, sin funcionalidad superpuesta

### 3. Flujo de Trabajo de Seguridad de IA
- **Espacio de Trabajo Temporal**: El contenido generado por IA primero se almacena en área temporal
- **Gestión Automática**: Alerta automática cuando el conteo de archivos excede 20
- **Mecanismo de Confirmación**: El contenido debe verificarse antes de incluirse en proyecto principal
- **Limpieza Automática**: Limpieza automática del espacio de trabajo temporal tras completar tarea

## Instalación

```bash
# Clonar repositorio
git clone https://github.com/AgentPsy/dsgs-context-engineering.git
cd dsgs-context-engineering

# Instalar
pip install -e .
```

## Uso

### Comandos CLI
```
/speckit.dsgs.context-analysis "Analizar calidad de este documento de requisitos" mode=enhanced
/speckit.dsgs.cognitive-template "Cómo mejorar el rendimiento" template=verification
/speckit.dsgs.context-optimization "Optimizar este requisito" optimization_goals=clarity,relevance
/speckit.dsgs.architect "Diseñar arquitectura del sistema de comercio electrónico"
/speckit.dsgs.git-skill operation=status
/speckit.dsgs.temp-workspace operation=create-workspace
```

### Python API
```python
from clean_skills.context_analysis import execute as context_analysis_execute

# Modo Estándar
result = context_analysis_execute({
    'context': 'Diseñar función de inicio de sesión de usuario',
    'mode': 'standard'
})

# Modo Mejorado
result = context_analysis_execute({
    'context': 'Diseñar función segura de inicio de sesión de usuario',
    'mode': 'enhanced'
})
```

## Buenas Prácticas de Seguridad de IA

1. **Antes de Generación de IA**: Siempre crear espacio de trabajo temporal primero
2. **Validar Contenido**: Usar mecanismo de confirmación para verificar contenido generado por IA
3. **Limpieza Regular**: Monitorear conteo de archivos temporales
4. **Limpiar Espacio**: Limpiar área temporal tras completar tarea

---
*Autor: pTree Dr. Zhang*  
*Organización: Laboratorio de Personalidad de IA 2025*  
*Contacto: 3061176@qq.com*  
*Sitio Web: https://AgentPsy.com*