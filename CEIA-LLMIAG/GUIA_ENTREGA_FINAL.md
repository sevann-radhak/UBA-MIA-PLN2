# Guía de Entrega Final - PLN II

## Estado de Entregables

### ✅ TP2: Chatbot RAG con CVs

**Estado**: Implementado y listo para entregar

**Archivos**:
- `CEIA-LLMIAG/ClaseVI/codigo/tp2_cargar_cv.py` - Script para cargar CV
- `CEIA-LLMIAG/ClaseVI/codigo/tp2_chatbot.py` - Chatbot con interfaz Streamlit
- `CEIA-LLMIAG/ClaseVI/codigo/README_TP2.md` - Documentación

**Pendiente para entrega**:
1. ✅ Código funcionando
2. ❌ Video de demostración (grabar con OBS)
3. ❌ Enviar links al formulario

**Cómo probar TP2**:
```bash
cd CEIA-LLMIAG/ClaseVI/codigo

# Paso 1: Cargar CV a Pinecone
python tp2_cargar_cv.py

# Paso 2: Ejecutar chatbot
streamlit run tp2_chatbot.py
```

**Qué mostrar en el video**:
- Cargar CV a Pinecone
- Hacer preguntas sobre el CV
- Mostrar respuestas del chatbot
- Mostrar interfaz Streamlit

---

### ✅ TP3: Agentes con Múltiples CVs

**Estado**: Implementado y listo para entregar

**Archivos**:
- `CEIA-LLMIAG/ClaseVII/codigo/tp3_cargar_cvs.py` - Cargar múltiples CVs
- `CEIA-LLMIAG/ClaseVII/codigo/tp3_decisor.py` - Nodo decisor
- `CEIA-LLMIAG/ClaseVII/codigo/tp3_rag_tools.py` - Herramientas RAG
- `CEIA-LLMIAG/ClaseVII/codigo/tp3_agente.py` - Agente principal
- `CEIA-LLMIAG/ClaseVII/codigo/tp3_interfaz.py` - Interfaz Streamlit
- `CEIA-LLMIAG/ClaseVII/codigo/README_TP3.md` - Documentación completa
- `CEIA-LLMIAG/ClaseVII/codigo/tp3_diagrama.md` - Diagrama de flujo
- `CEIA-LLMIAG/ClaseVII/codigo/cvs/` - CVs (alumno, pedro, ana)

**Pendiente para entrega**:
1. ✅ Código funcionando
2. ✅ Documentación completa
3. ❌ Video/presentación (grabar con OBS)
4. ❌ Enviar links al formulario

**Cómo probar TP3**:
```bash
cd CEIA-LLMIAG/ClaseVII/codigo

# Paso 1: Verificar sistema
python tp3_verificar.py

# Paso 2: Cargar CVs a Pinecone
python tp3_cargar_cvs.py

# Paso 3: Ejecutar interfaz
streamlit run tp3_interfaz.py
```

**Qué mostrar en el video/presentación**:
- Flujo del agente (decisor → RAG → respuesta)
- Query genérica → CV del alumno
- Query con nombre específico → CV correcto
- Query comparativa → Múltiples CVs
- Mostrar detalles del proceso (opcional)

---

## Checklist de Entrega

### TP2

- [ ] Código funcionando correctamente
- [ ] Video de demostración grabado (3-5 minutos)
- [ ] Video subido a YouTube o guardado en repo
- [ ] Repositorio actualizado con código
- [ ] README_TP2.md completo
- [ ] Links preparados (repositorio + video)
- [ ] Enviado al formulario de entrega

### TP3

- [ ] Código funcionando correctamente
- [ ] Todos los componentes implementados
- [ ] Nodo decisor funcionando
- [ ] Herramientas RAG funcionando
- [ ] Agente principal funcionando
- [ ] Interfaz funcionando
- [ ] Documentación completa (README_TP3.md)
- [ ] Diagrama de flujo (tp3_diagrama.md)
- [ ] Video/presentación preparada
- [ ] Repositorio actualizado
- [ ] Links preparados (repositorio + video/presentación)
- [ ] Enviado al formulario de entrega

---

## Cómo Probar Todo

### Verificación Rápida

```bash
# Verificar TP2
cd CEIA-LLMIAG/ClaseVI/codigo
python tp2_cargar_cv.py
streamlit run tp2_chatbot.py

# Verificar TP3
cd CEIA-LLMIAG/ClaseVII/codigo
python tp3_verificar.py
python tp3_cargar_cvs.py
streamlit run tp3_interfaz.py
```

### Pruebas de TP3

**Prueba 1: Query Genérica**
```
Query: "¿Cuál es mi experiencia en Python?"
Esperado: Responde con CV del alumno (María)
```

**Prueba 2: Query con Nombre**
```
Query: "¿Qué habilidades tiene Pedro?"
Esperado: Responde con CV de Pedro
```

**Prueba 3: Query Comparativa**
```
Query: "Compara las habilidades de Pedro y Ana"
Esperado: Responde comparando ambos CVs
```

---

## Estructura del Repositorio para Entrega

```
CEIA-LLMIAG/
├── ClaseVI/
│   └── codigo/
│       ├── tp2_cargar_cv.py
│       ├── tp2_chatbot.py
│       ├── README_TP2.md
│       └── cv.txt
│
├── ClaseVII/
│   └── codigo/
│       ├── tp3_cargar_cvs.py
│       ├── tp3_decisor.py
│       ├── tp3_rag_tools.py
│       ├── tp3_agente.py
│       ├── tp3_interfaz.py
│       ├── tp3_verificar.py
│       ├── tp3_diagrama.md
│       ├── README_TP3.md
│       └── cvs/
│           ├── cv_alumno.txt
│           ├── cv_pedro.txt
│           └── cv_ana.txt
│
├── PLAN_MAESTRO_ENTREGABLES.md
└── GUIA_ENTREGA_FINAL.md (este archivo)
```

---

## Formato de Entrega

### Formulario de Entrega

**Links requeridos**:
1. **Repositorio**: Link a GitHub (o similar) con código
2. **Video**: Link a YouTube o video en repo

**Formato sugerido**:
- Repositorio: `https://github.com/tu-usuario/tu-repo`
- Video: `https://youtube.com/watch?v=...` o link en repo

### Contenido del Video

**TP2 (3-5 minutos)**:
1. Mostrar script de carga de CV
2. Ejecutar chatbot
3. Hacer 2-3 preguntas de ejemplo
4. Mostrar respuestas

**TP3 (5-7 minutos)**:
1. Mostrar flujo completo del agente
2. Query genérica → CV del alumno
3. Query con nombre → CV específico
4. Query comparativa → Múltiples CVs
5. Mostrar detalles del proceso (opcional)

---

## Fecha Límite

**Sábado 13 de diciembre de 2025**

**Razón**: Notas deben entregarse el martes 16 de diciembre

---

## Contacto

Si hay problemas o dudas:
- **Esp. Abraham Rodriguez**: abraham.rodz17@gmail.com
- **Esp. Ezequiel Guinsburg**: ezequiel.guinsburg@gmail.com

---

## Resumen de lo Implementado

### TP2 ✅
- Script para cargar CV a Pinecone
- Chatbot con RAG usando Groq
- Interfaz Streamlit funcional
- Documentación completa

### TP3 ✅
- Script para cargar múltiples CVs
- Nodo decisor que determina qué CV usar
- Herramientas RAG para cada CV
- Agente principal que integra todo
- Interfaz Streamlit con detalles del proceso
- Documentación completa y diagrama de flujo
- Script de verificación del sistema

**Todo está implementado y listo para probar y entregar.**



