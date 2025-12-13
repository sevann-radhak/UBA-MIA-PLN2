"""
TP3 - Interfaz Streamlit para Agente de Múltiples CVs
======================================================

Interfaz web para interactuar con el agente que consulta múltiples CVs.

Autor: TP3 - Clase VII - CEIA LLMIAG
"""

import os
import sys
import streamlit as st
from dotenv import load_dotenv

# Cargar .env desde la raíz del proyecto
env_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', '.env')
load_dotenv(env_path)
# También intentar cargar desde directorio actual
load_dotenv()

# Agregar directorio actual al path para imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tp3_agente import AgenteCV

# ================================
# CONFIGURACIÓN
# ================================

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

# ================================
# INICIALIZACIÓN
# ================================

@st.cache_resource
def inicializar_agente():
    """Inicializa el agente (cached para Streamlit)."""
    try:
        agente = AgenteCV()
        return agente
    except Exception as e:
        st.error(f"Error al inicializar agente: {e}")
        return None


# ================================
# INTERFAZ STREAMLIT
# ================================

def main():
    """Función principal de la aplicación."""
    
    # Verificar API keys
    if not PINECONE_API_KEY or not GROQ_API_KEY:
        st.error("⚠️ API Keys no configuradas")
        st.info("💡 Configura PINECONE_API_KEY y GROQ_API_KEY en .env")
        st.stop()
    
    # Título
    st.title("🤖 Agente de Múltiples CVs - TP3")
    st.markdown("""
    **Sistema de Agentes con RAG para Consultar Múltiples Currículums**
    
    Este agente puede:
    - 🔍 Decidir qué CV consultar basado en tu pregunta
    - 📚 Buscar contexto relevante en múltiples CVs
    - 🧠 Generar respuestas usando información de los CVs
    - 👥 Comparar información entre diferentes personas
    """)
    
    # Inicializar agente
    agente = inicializar_agente()
    if agente is None:
        st.error("❌ No se pudo inicializar el agente")
        st.info("💡 Asegúrate de haber ejecutado tp3_cargar_cvs.py primero")
        st.stop()
    
    st.sidebar.success("✅ Agente inicializado")
    
    # Configuración en sidebar
    st.sidebar.title("⚙️ Configuración")
    
    top_k = st.sidebar.slider(
        "Número de chunks a recuperar por CV (k)",
        min_value=1,
        max_value=10,
        value=3,
        help="Más chunks = más contexto pero más tokens"
    )
    
    mostrar_detalles = st.sidebar.checkbox(
        "Mostrar detalles del proceso",
        value=False,
        help="Muestra información sobre decisión y chunks usados"
    )
    
    # Información sobre CVs disponibles
    with st.sidebar.expander("📋 CVs Disponibles"):
        st.markdown("""
        - **María González** (alumno): Científica de Datos, NLP
        - **Pedro Martínez**: Ingeniero de Software, Backend
        - **Ana Rodríguez**: MLOps Engineer
        """)
    
    # Inicializar historial de conversación
    if "historial" not in st.session_state:
        st.session_state.historial = []
    
    # Mostrar historial
    if st.session_state.historial:
        st.markdown("### 📜 Historial de Conversación")
        for i, mensaje in enumerate(st.session_state.historial):
            if mensaje["role"] == "user":
                st.markdown(f"**👤 Usuario:** {mensaje['content']}")
            else:
                with st.expander(f"🤖 Respuesta {i//2 + 1}"):
                    st.markdown(mensaje['content'])
                    if mostrar_detalles and "detalles" in mensaje:
                        detalles = mensaje['detalles']
                        st.caption(f"📚 CVs usados: {', '.join(detalles.get('cvs_usados', []))}")
                        st.caption(f"👥 Personas: {', '.join(detalles.get('personas', []))}")
                        st.caption(f"💭 Razón: {detalles.get('razon', 'N/A')}")
                        st.caption(f"📊 Chunks encontrados: {detalles.get('num_chunks', 0)}")
        st.markdown("---")
    
    # Input del usuario
    pregunta = st.text_input(
        "💬 Haz una pregunta sobre los CVs:",
        placeholder="Ejemplo: ¿Cuál es mi experiencia en Python?",
        key="pregunta_input"
    )
    
    # Botón para limpiar historial
    if st.sidebar.button("🗑️ Limpiar Historial"):
        st.session_state.historial = []
        st.rerun()
    
    # Ejemplos de preguntas
    with st.expander("💡 Ejemplos de Preguntas"):
        st.markdown("""
        **Preguntas genéricas (CV del alumno):**
        - ¿Cuál es mi experiencia en Python?
        - ¿Qué proyectos he realizado?
        - ¿Cuáles son mis habilidades técnicas?
        
        **Preguntas sobre personas específicas:**
        - ¿Qué experiencia tiene Pedro en backend?
        - ¿Cuál es la experiencia de Ana en MLOps?
        - ¿Qué habilidades tiene María en NLP?
        
        **Preguntas comparativas:**
        - Compara las habilidades de Pedro y Ana en Python
        - ¿Quién tiene más experiencia en cloud?
        """)
    
    # Procesar pregunta
    if pregunta:
        with st.spinner("🤔 Procesando pregunta..."):
            try:
                # Procesar con agente
                if mostrar_detalles:
                    resultado = agente.procesar_query_con_detalles(pregunta, top_k=top_k)
                    detalles = {
                        "cvs_usados": resultado['cvs_usados'],
                        "personas": resultado['personas'],
                        "razon": resultado['razon'],
                        "num_chunks": resultado['num_chunks']
                    }
                else:
                    resultado = agente.procesar_query(pregunta, top_k=top_k)
                    detalles = {
                        "cvs_usados": resultado['cvs_usados'],
                        "personas": resultado['personas'],
                        "razon": resultado['razon'],
                        "num_chunks": resultado['contextos_encontrados']
                    }
                
                respuesta = resultado['respuesta']
                
                # Guardar en historial
                st.session_state.historial.append({
                    "role": "user",
                    "content": pregunta
                })
                st.session_state.historial.append({
                    "role": "assistant",
                    "content": respuesta,
                    "detalles": detalles
                })
                
                # Mostrar respuesta
                st.markdown("### 🤖 Respuesta:")
                st.markdown(respuesta)
                
                # Mostrar detalles si está habilitado
                if mostrar_detalles:
                    with st.expander("🔍 Detalles del Proceso"):
                        st.markdown(f"**CVs consultados:** {', '.join(detalles['cvs_usados'])}")
                        st.markdown(f"**Personas:** {', '.join(detalles['personas'])}")
                        st.markdown(f"**Razón:** {detalles['razon']}")
                        st.markdown(f"**Chunks encontrados:** {detalles['num_chunks']}")
                        
                        if 'chunks_detallados' in resultado:
                            for cv_name, chunks in resultado['chunks_detallados'].items():
                                st.markdown(f"**Chunks de {cv_name}:**")
                                for i, chunk in enumerate(chunks[:2], 1):
                                    st.caption(f"Chunk {i} (Score: {chunk['score']:.3f}): {chunk['texto'][:100]}...")
                
                # Información adicional
                st.caption(f"📊 Modelo: llama-3.1-8b-instant | 📚 Top-K: {top_k}")
                
                # Recargar para mostrar historial actualizado
                st.rerun()
                
            except Exception as e:
                st.error(f"❌ Error al procesar pregunta: {str(e)}")
                st.info("💡 Verifica que los índices de Pinecone estén creados (ejecuta tp3_cargar_cvs.py)")
    
    # Información adicional
    with st.expander("📚 Información sobre el Sistema"):
        st.markdown("""
        **Arquitectura del Agente:**
        
        1. **Nodo Decisor**: Analiza la pregunta y determina qué CV(s) consultar
        2. **Herramientas RAG**: Buscan contexto relevante en cada CV usando embeddings
        3. **Agente Principal**: Integra decisión + contexto + LLM para generar respuesta
        
        **Flujo:**
        - Query → Decisor → CV(s) seleccionado(s)
        - Búsqueda vectorial en Pinecone → Contexto relevante
        - LLM con contexto → Respuesta final
        
        **Características:**
        - Consulta automática de CVs según la pregunta
        - Soporte para preguntas genéricas (CV del alumno)
        - Soporte para preguntas sobre personas específicas
        - Comparación entre múltiples personas
        """)
    
    st.markdown("---")
    st.markdown("**📖 TP3 - Clase VII - CEIA LLMIAG**")


if __name__ == "__main__":
    main()

