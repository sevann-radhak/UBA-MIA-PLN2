# Instrucciones Rápidas - TP2 y TP3

## 🚀 Inicio Rápido

### Configuración Inicial (Solo una vez)

1. **Crear archivo `.env`** en la raíz del proyecto:
```env
PINECONE_API_KEY=tu_api_key
PINECONE_ENVIRONMENT=us-east-1-aws
GROQ_API_KEY=tu_api_key
```

2. **Instalar dependencias**:
```bash
pip install -r CEIA-LLMIAG/ClaseVI/codigo/requirements.txt
```

---

## 📋 TP2: Chatbot RAG con CV

### Pasos para Ejecutar

```bash
cd CEIA-LLMIAG/ClaseVI/codigo

# 1. Cargar CV a Pinecone
python tp2_cargar_cv.py

# 2. Ejecutar chatbot
streamlit run tp2_chatbot.py
```

### Verificar que Funciona

- Abrir `http://localhost:8501`
- Hacer pregunta: "¿Cuál es mi experiencia en Python?"
- Debe responder con información del CV

---

## 🤖 TP3: Agentes con Múltiples CVs

### Pasos para Ejecutar

```bash
cd CEIA-LLMIAG/ClaseVII/codigo

# 1. Verificar sistema
python tp3_verificar.py

# 2. Cargar CVs a Pinecone
python tp3_cargar_cvs.py

# 3. Ejecutar interfaz
streamlit run tp3_interfaz.py
```

### Verificar que Funciona

**Prueba 1 - Query Genérica**:
- Pregunta: "¿Cuál es mi experiencia en Python?"
- Debe usar CV del alumno (María)

**Prueba 2 - Query con Nombre**:
- Pregunta: "¿Qué habilidades tiene Pedro?"
- Debe usar CV de Pedro

**Prueba 3 - Query Comparativa**:
- Pregunta: "Compara las habilidades de Pedro y Ana"
- Debe usar ambos CVs

---

## ✅ Checklist Antes de Entregar

### TP2
- [ ] Código funciona
- [ ] Video grabado (OBS)
- [ ] Links preparados
- [ ] Enviado al formulario

### TP3
- [ ] Código funciona
- [ ] Documentación completa
- [ ] Video/presentación preparada
- [ ] Links preparados
- [ ] Enviado al formulario

---

## 📅 Fecha Límite

**Sábado 13 de diciembre de 2025**

---

## 🆘 Problemas Comunes

**Error: "API key no configurada"**
→ Verificar archivo `.env` existe y tiene las keys

**Error: "Index not found"**
→ Ejecutar script de carga primero (tp2_cargar_cv.py o tp3_cargar_cvs.py)

**Error: "Module not found"**
→ Verificar que estás en el directorio correcto
→ Instalar dependencias: `pip install -r requirements.txt`

---

## 📚 Documentación Completa

- **TP2**: `CEIA-LLMIAG/ClaseVI/codigo/README_TP2.md`
- **TP3**: `CEIA-LLMIAG/ClaseVII/codigo/README_TP3.md`
- **Plan Maestro**: `CEIA-LLMIAG/PLAN_MAESTRO_ENTREGABLES.md`
- **Guía Entrega**: `CEIA-LLMIAG/GUIA_ENTREGA_FINAL.md`



