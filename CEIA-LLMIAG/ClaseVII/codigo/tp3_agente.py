"""
TP3 - Agente Principal
======================

Agente que integra nodo decisor + herramientas RAG + LLM para responder
preguntas sobre múltiples CVs.

Autor: TP3 - Clase VII - CEIA LLMIAG
"""

import os
import sys
from typing import Dict, List, Any, Optional
from groq import Groq
from dotenv import load_dotenv

# Cargar .env desde la raíz del proyecto
env_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', '.env')
load_dotenv(env_path)
# También intentar cargar desde directorio actual
load_dotenv()

# Agregar directorio actual al path para imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tp3_decisor import DecisorCV
from tp3_rag_tools import RAGToolsManager

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODELO_GROQ = "llama-3.1-8b-instant"


class AgenteCV:
    """Agente que procesa queries sobre múltiples CVs usando ReAct pattern."""
    
    def __init__(self, llm_client: Groq = None):
        """
        Inicializa el agente.
        
        Args:
            llm_client: Cliente de Groq (opcional)
        """
        if llm_client is None:
            if not GROQ_API_KEY:
                raise ValueError("GROQ_API_KEY no está configurada en .env")
            self.llm_client = Groq(api_key=GROQ_API_KEY)
        else:
            self.llm_client = llm_client
        
        self.modelo = MODELO_GROQ
        self.decisor = DecisorCV(self.llm_client)
        self.rag_manager = RAGToolsManager()
    
    def procesar_query(self, query: str, max_iteraciones: int = 3, top_k: int = 3) -> Dict[str, Any]:
        """
        Procesa una query usando patrón ReAct.
        
        Args:
            query: Pregunta del usuario
            max_iteraciones: Máximo de iteraciones (para futuras extensiones)
            top_k: Número de chunks a recuperar por CV
        
        Returns:
            Dict con:
                - 'respuesta': Respuesta final
                - 'cvs_usados': CVs consultados
                - 'personas': Nombres de personas
                - 'razon': Razón de la decisión
        """
        # Paso 1: Decidir qué CV usar
        decision = self.decisor.decidir(query)
        cvs_a_consultar = decision['cvs']
        
        # Paso 2: Buscar contexto en CV(s) seleccionado(s)
        contextos = self.rag_manager.buscar_en_multiples_cvs(
            query,
            cvs_a_consultar,
            top_k=top_k
        )
        
        # Paso 3: Construir prompt con contexto
        prompt = self._construir_prompt(query, contextos, decision)
        
        # Paso 4: Generar respuesta con LLM
        respuesta = self._generar_respuesta(prompt)
        
        return {
            "respuesta": respuesta,
            "cvs_usados": cvs_a_consultar,
            "personas": decision['personas'],
            "razon": decision['razon'],
            "contextos_encontrados": len([c for c in contextos.values() if c])
        }
    
    def _construir_prompt(self, query: str, contextos: Dict[str, str], decision: Dict[str, Any]) -> str:
        """
        Construye el prompt para el LLM con el contexto de RAG.
        
        Args:
            query: Pregunta del usuario
            contextos: Dict con contexto de cada CV
            decision: Decisión del nodo decisor
        
        Returns:
            Prompt completo
        """
        # Construir sección de contexto
        contexto_texto = ""
        
        for cv_name, contexto in contextos.items():
            if contexto:
                tool = self.rag_manager.obtener_tool(cv_name)
                if tool:
                    persona = tool.persona
                    contexto_texto += f"\n\n--- CONTEXTO DE {persona.upper()} ---\n{contexto}"
        
        # Determinar persona de referencia
        if len(decision['personas']) == 1:
            persona_ref = decision['personas'][0]
            instruccion_persona = f"Responde como si fueras {persona_ref}."
        else:
            personas_str = " y ".join(decision['personas'])
            instruccion_persona = f"Responde comparando información de {personas_str}."
        
        prompt = f"""Eres un asistente que responde preguntas sobre currículums vitae.

{instruccion_persona}

CONTEXTO RECUPERADO DE LOS CVs:
{contexto_texto}

INSTRUCCIONES:
- Responde la pregunta del usuario basándote ÚNICAMENTE en el contexto proporcionado
- Si la información no está en el contexto, di que no tienes esa información
- Sé claro, conciso y profesional
- Si se consultan múltiples personas, compara o integra la información según corresponda
- Usa el contexto relevante para dar una respuesta completa

PREGUNTA DEL USUARIO: {query}

RESPUESTA:"""
        
        return prompt
    
    def _generar_respuesta(self, prompt: str) -> str:
        """
        Genera respuesta usando el LLM.
        
        Args:
            prompt: Prompt completo
        
        Returns:
            Respuesta del LLM
        """
        try:
            respuesta = self.llm_client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                model=self.modelo,
                temperature=0.7,
                max_tokens=1000
            )
            
            return respuesta.choices[0].message.content.strip()
            
        except Exception as e:
            return f"Error al generar respuesta: {str(e)}"
    
    def procesar_query_con_detalles(self, query: str, top_k: int = 3) -> Dict[str, Any]:
        """
        Procesa query y retorna información detallada del proceso.
        
        Args:
            query: Pregunta del usuario
            top_k: Número de chunks a recuperar
        
        Returns:
            Dict con respuesta y detalles del proceso
        """
        # Decisión
        decision = self.decisor.decidir(query)
        cvs_a_consultar = decision['cvs']
        
        # Buscar contexto detallado
        chunks_detallados = {}
        for cv_name in cvs_a_consultar:
            tool = self.rag_manager.obtener_tool(cv_name)
            if tool:
                chunks = tool.buscar_contexto_detallado(query, top_k=top_k)
                chunks_detallados[cv_name] = chunks
        
        # Construir contexto simple para respuesta
        contextos = {}
        for cv_name, chunks in chunks_detallados.items():
            textos = [chunk['texto'] for chunk in chunks]
            contextos[cv_name] = '\n\n'.join(textos)
        
        # Generar respuesta
        prompt = self._construir_prompt(query, contextos, decision)
        respuesta = self._generar_respuesta(prompt)
        
        return {
            "respuesta": respuesta,
            "cvs_usados": cvs_a_consultar,
            "personas": decision['personas'],
            "razon": decision['razon'],
            "chunks_detallados": chunks_detallados,
            "num_chunks": sum(len(chunks) for chunks in chunks_detallados.values())
        }


def main():
    """Función de prueba del agente."""
    print("=" * 60)
    print("TP3 - Prueba del Agente Principal")
    print("=" * 60)
    
    agente = AgenteCV()
    
    queries_prueba = [
        "¿Cuál es mi experiencia en Python?",
        "¿Qué habilidades tiene Pedro en backend?",
        "¿Cuál es la experiencia de Ana en MLOps?",
        "Compara las habilidades de Pedro y Ana en Python"
    ]
    
    for query in queries_prueba:
        print(f"\n{'='*60}")
        print(f"📝 Query: {query}")
        print('='*60)
        
        resultado = agente.procesar_query(query, top_k=2)
        
        print(f"\n✅ CVs usados: {resultado['cvs_usados']}")
        print(f"👥 Personas: {', '.join(resultado['personas'])}")
        print(f"💭 Razón: {resultado['razon']}")
        print(f"📚 Chunks encontrados: {resultado['contextos_encontrados']}")
        print(f"\n🤖 Respuesta:\n{resultado['respuesta']}")


if __name__ == "__main__":
    main()

