# Guía de Implementación: Trabajos Prácticos PLN II

## Contexto

Estamos finalizando la materia **Procesamiento del Lenguaje Natural II** (UBA - Maestría en IA). Necesitamos completar los trabajos prácticos pendientes.

## Estado Actual

- **TP1 (TinyGPT)**: Fecha pasada, consultar si es necesario
- **TP2 (Chatbot RAG)**: ✅ Implementado, falta entregar (video + formulario)
- **TP3 (Agentes múltiples CVs)**: 🟡 En desarrollo, necesita implementación completa

## Objetivo Principal

Completar TP2 y TP3 para finalizar la materia. TP1 solo si los docentes lo requieren.

## Principios de Implementación

### 1. Trabajo Incremental y Modular
- **Nunca implementar todo de una vez**
- Dividir en bloques pequeños y funcionales
- Probar cada bloque antes de continuar
- Hacer commits pequeños y frecuentes

### 2. Mantener Ownership del Código
- **Entender cada componente** antes de implementarlo
- No copiar código sin entenderlo
- Documentar decisiones y razones
- Si usas código generado por IA, asegúrate de entenderlo completamente

### 3. Testing Continuo
- Probar cada función individualmente
- Probar integraciones paso a paso
- No esperar al final para probar
- Documentar problemas y soluciones

### 4. Documentación Mientras Desarrollas
- Documentar decisiones técnicas
- Documentar problemas encontrados
- Documentar soluciones implementadas
- Mantener README actualizado

## Estructura de Trabajo para TP3

### Fase 1: Nodo Decisor (Bloque 1)
**Archivo**: `CEIA-LLMIAG/ClaseVII/codigo/tp3_decisor.py`

**Objetivo**: Implementar función que determina qué CV usar basado en la query.

**Pasos**:
1. Crear función que recibe query
2. Usar LLM para analizar query
3. Determinar si menciona nombre específico
4. Retornar decisión (qué CV usar)

**Criterio de éxito**: 
- Función retorna decisión correcta para queries de prueba
- Maneja queries genéricas (CV del alumno)
- Maneja queries con nombres específicos

### Fase 2: Herramientas RAG (Bloque 2)
**Archivo**: `CEIA-LLMIAG/ClaseVII/codigo/tp3_rag_tools.py`

**Objetivo**: Crear herramientas RAG para cada CV.

**Pasos**:
1. Cargar múltiples CVs a Pinecone (índices separados o con metadata)
2. Crear clase RAGTool para cada CV
3. Implementar método buscar_contexto()
4. Probar búsqueda en cada CV

**Criterio de éxito**:
- Cada CV tiene su herramienta RAG funcionando
- Búsquedas retornan contexto relevante
- Contextos son diferentes para diferentes CVs

### Fase 3: Agente Principal (Bloque 3)
**Archivo**: `CEIA-LLMIAG/ClaseVII/codigo/tp3_agente.py`

**Objetivo**: Integrar decisor + herramientas RAG + LLM.

**Pasos**:
1. Crear clase AgenteCV
2. Integrar nodo decisor
3. Integrar herramientas RAG
4. Implementar flujo ReAct básico
5. Probar con queries de ejemplo

**Criterio de éxito**:
- Agente procesa queries correctamente
- Usa CV correcto según decisión
- Genera respuestas con contexto relevante
- Maneja queries genéricas y específicas

### Fase 4: Interfaz (Bloque 4)
**Archivo**: `CEIA-LLMIAG/ClaseVII/codigo/tp3_interfaz.py`

**Objetivo**: Crear interfaz para interactuar con el agente.

**Pasos**:
1. Crear interfaz Streamlit básica
2. Integrar con agente
3. Mostrar respuestas
4. Opcional: Mostrar proceso de decisión

**Criterio de éxito**:
- Interfaz funciona correctamente
- Usuario puede hacer queries
- Respuestas se muestran correctamente

### Fase 5: Testing y Refinamiento (Bloque 5)
**Objetivo**: Probar sistema completo y refinar.

**Pasos**:
1. Probar queries genéricas
2. Probar queries con nombres específicos
3. Probar queries sobre múltiples personas
4. Probar queries complejas
5. Refinar prompts y lógica según resultados

**Criterio de éxito**:
- Todos los casos de prueba pasan
- Respuestas son relevantes y correctas
- Sistema maneja errores apropiadamente

## Reglas de Código

### Estilo y Estructura
- **Código en inglés**: Variables, funciones, clases, comentarios
- **Documentación mínima**: Código debe ser autoexplicativo
- **Funciones pequeñas**: Una responsabilidad por función
- **Nombres descriptivos**: Variables y funciones deben explicar su propósito

### Organización
- **Un archivo por componente principal**
- **Separar lógica de negocio de interfaz**
- **Usar clases cuando tenga sentido**
- **Mantener estructura clara y navegable**

### Manejo de Errores
- **Validar inputs**: Verificar que queries no estén vacías
- **Manejar errores de API**: Pinecone, Groq, etc.
- **Mensajes de error claros**: Para debugging
- **Fallbacks apropiados**: Si algo falla, manejar gracefully

### Configuración
- **Usar archivo .env**: Para API keys y configuración
- **No hardcodear valores**: Usar constantes o configuración
- **Documentar variables de entorno**: En README

## Checklist de Calidad

Antes de considerar un bloque "completo":

- [ ] Código funciona correctamente
- [ ] Código está probado con casos de ejemplo
- [ ] Código está documentado (si es necesario)
- [ ] Código sigue las reglas de estilo
- [ ] Código maneja errores apropiadamente
- [ ] Código está commiteado (commit pequeño y descriptivo)

## Recursos y Referencias

### Código de Ejemplo
- `CEIA-LLMIAG/ClaseVII/codigo/Agentes_desde_cero.ipynb` - ReAct manual
- `CEIA-LLMIAG/ClaseVII/codigo/Agentes_Langchain.ipynb` - Con LangChain
- `CEIA-LLMIAG/ClaseVII/codigo/Agentes_Complejo.ipynb` - Sistema complejo
- `CEIA-LLMIAG/ClaseVI/codigo/tp2_*.py` - Referencia de TP2

### Documentación
- `CEIA-LLMIAG/PLAN_MAESTRO_ENTREGABLES.md` - Plan completo
- `CEIA-LLMIAG/CLASE_VII_20_PORCIENTO.md` - Resumen Clase 7
- `CEIA-LLMIAG/ClaseVI/codigo/README_TP2.md` - Documentación TP2

## Flujo de Trabajo Recomendado

1. **Leer plan maestro** (`PLAN_MAESTRO_ENTREGABLES.md`)
2. **Verificar estado actual** (qué está hecho, qué falta)
3. **Elegir bloque a implementar** (empezar por el más simple)
4. **Implementar bloque** (código pequeño, probado, commiteado)
5. **Probar bloque** (casos de prueba)
6. **Documentar si es necesario**
7. **Pasar al siguiente bloque**
8. **Repetir hasta completar**

## Preguntas Frecuentes

**P: ¿Debo usar LangChain o implementación manual?**
R: Depende. Si quieres más control y entender mejor, manual. Si quieres rapidez y estructura, LangChain. Ambas son válidas.

**P: ¿Cuántos CVs necesito?**
R: Mínimo 2 (tu CV + otro). Idealmente 3-4 del grupo.

**P: ¿Qué hacer si TP2 no funciona?**
R: Resolver TP2 primero. TP3 depende de TP2.

**P: ¿Debo implementar TP1?**
R: Consultar con docentes primero. Fecha ya pasó.

## Recordatorios Importantes

- ⚠️ **TP2 debe funcionar antes de TP3**
- ⚠️ **Trabajar bloque por bloque, no todo junto**
- ⚠️ **Probar continuamente, no esperar al final**
- ⚠️ **Mantener ownership del código**
- ⚠️ **Documentar mientras desarrollas**
- ⚠️ **Commits pequeños y frecuentes**

---

*Esta regla guía la implementación de los trabajos prácticos. Consulta `PLAN_MAESTRO_ENTREGABLES.md` para detalles completos.*



