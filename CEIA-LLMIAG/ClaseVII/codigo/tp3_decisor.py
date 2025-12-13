"""
TP3 - Nodo Decisor
==================

Determina qué CV(s) usar basado en la query del usuario.

Autor: TP3 - Clase VII - CEIA LLMIAG
"""

import os
import json
from typing import Dict, List
from groq import Groq
from dotenv import load_dotenv

# Cargar .env desde la raíz del proyecto
env_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', '.env')
load_dotenv(env_path)
# También intentar cargar desde directorio actual
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODELO_GROQ = "llama-3.1-8b-instant"

# Mapeo de nombres a índices de CVs
CVS_DISPONIBLES = {
    "alumno": {
        "indice": "cv-alumno-tp3",
        "persona": "María González",
        "alias": ["maría", "maria", "gonzález", "gonzalez", "alumno", "alumna"]
    },
    "pedro": {
        "indice": "cv-pedro-tp3",
        "persona": "Pedro Martínez",
        "alias": ["pedro", "martínez", "martinez"]
    },
    "ana": {
        "indice": "cv-ana-tp3",
        "persona": "Ana Rodríguez",
        "alias": ["ana", "rodríguez", "rodriguez"]
    }
}


class DecisorCV:
    """Clase que decide qué CV(s) usar basado en la query."""
    
    def __init__(self, llm_client: Groq = None):
        """
        Inicializa el decisor.
        
        Args:
            llm_client: Cliente de Groq (opcional, se crea si no se proporciona)
        """
        if llm_client is None:
            if not GROQ_API_KEY:
                raise ValueError("GROQ_API_KEY no está configurada en .env")
            self.llm_client = Groq(api_key=GROQ_API_KEY)
        else:
            self.llm_client = llm_client
        
        self.modelo = MODELO_GROQ
    
    def decidir(self, query: str) -> Dict[str, any]:
        """
        Determina qué CV(s) usar basado en la query.
        
        Args:
            query: Pregunta del usuario
        
        Returns:
            Dict con:
                - 'cvs': Lista de nombres de CVs a consultar
                - 'razon': Explicación de la decisión
                - 'personas': Lista de nombres de personas
        """
        # Primero, intentar detección simple por nombres
        query_lower = query.lower()
        cvs_detectados = []
        
        for cv_nombre, cv_info in CVS_DISPONIBLES.items():
            # Buscar nombre de persona o alias
            if any(alias in query_lower for alias in cv_info["alias"]):
                cvs_detectados.append(cv_nombre)
        
        # Si no se detectó ningún nombre específico, usar LLM para análisis más profundo
        if not cvs_detectados:
            decision_llm = self._decidir_con_llm(query)
            if decision_llm:
                return decision_llm
            # Si LLM no encuentra nada, usar CV del alumno por defecto
            return {
                "cvs": ["alumno"],
                "razon": "Query genérica, usando CV del alumno que presenta",
                "personas": [CVS_DISPONIBLES["alumno"]["persona"]]
            }
        
        # Si se detectaron nombres, usar esos CVs
        personas = [CVS_DISPONIBLES[cv]["persona"] for cv in cvs_detectados]
        razon = f"Query menciona a: {', '.join(personas)}"
        
        return {
            "cvs": cvs_detectados,
            "razon": razon,
            "personas": personas
        }
    
    def _decidir_con_llm(self, query: str) -> Dict[str, any]:
        """
        Usa LLM para decidir qué CV usar (análisis más profundo).
        
        Args:
            query: Pregunta del usuario
        
        Returns:
            Dict con decisión o None si no puede determinar
        """
        prompt = f"""Analiza la siguiente pregunta y determina:
1. ¿Menciona el nombre de alguna persona específica?
2. ¿Qué CV(s) debería consultar?

CVs disponibles:
- María González (alumno): Científica de Datos, especializada en NLP
- Pedro Martínez: Ingeniero de Software, especializado en backend y microservicios
- Ana Rodríguez: MLOps Engineer, especializada en deployment de modelos ML

Si la pregunta es genérica (ej: "¿Cuál es mi experiencia?", "¿Qué habilidades tengo?"), 
usa el CV del alumno (María González).

Pregunta: {query}

Responde SOLO con un JSON válido en este formato:
{{
    "cvs": ["alumno"],
    "razon": "explicación breve"
}}

Si menciona múltiples personas, inclúyelas todas en el array "cvs".
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
                temperature=0.1,
                max_tokens=200
            )
            
            respuesta_texto = respuesta.choices[0].message.content.strip()
            
            # Limpiar respuesta (puede venir con markdown)
            if "```json" in respuesta_texto:
                respuesta_texto = respuesta_texto.split("```json")[1].split("```")[0].strip()
            elif "```" in respuesta_texto:
                respuesta_texto = respuesta_texto.split("```")[1].split("```")[0].strip()
            
            decision = json.loads(respuesta_texto)
            
            # Validar que los CVs existen
            cvs_validos = []
            for cv in decision.get("cvs", []):
                if cv in CVS_DISPONIBLES:
                    cvs_validos.append(cv)
            
            if not cvs_validos:
                return None
            
            personas = [CVS_DISPONIBLES[cv]["persona"] for cv in cvs_validos]
            
            return {
                "cvs": cvs_validos,
                "razon": decision.get("razon", "Decisión basada en análisis de query"),
                "personas": personas
            }
            
        except Exception as e:
            print(f"⚠️ Error en decisión con LLM: {e}")
            return None
    
    def obtener_indices_pinecone(self, cvs: List[str]) -> List[str]:
        """
        Obtiene los nombres de índices de Pinecone para los CVs especificados.
        
        Args:
            cvs: Lista de nombres de CVs
        
        Returns:
            Lista de nombres de índices
        """
        indices = []
        for cv in cvs:
            if cv in CVS_DISPONIBLES:
                indices.append(CVS_DISPONIBLES[cv]["indice"])
        return indices


def main():
    """Función de prueba del decisor."""
    print("=" * 60)
    print("TP3 - Prueba del Nodo Decisor")
    print("=" * 60)
    
    decisor = DecisorCV()
    
    queries_prueba = [
        "¿Cuál es mi experiencia en Python?",
        "¿Qué habilidades tiene Pedro?",
        "¿Cuál es la experiencia de Ana en MLOps?",
        "¿Qué proyectos ha hecho María?",
        "Compara las habilidades de Pedro y Ana"
    ]
    
    for query in queries_prueba:
        print(f"\n📝 Query: {query}")
        decision = decisor.decidir(query)
        print(f"   ✅ CVs a usar: {decision['cvs']}")
        print(f"   📋 Personas: {', '.join(decision['personas'])}")
        print(f"   💭 Razón: {decision['razon']}")
        print(f"   🔍 Índices Pinecone: {decisor.obtener_indices_pinecone(decision['cvs'])}")


if __name__ == "__main__":
    main()

