"""
TP3 - Herramientas RAG para Múltiples CVs
==========================================

Crea herramientas RAG para cada CV, permitiendo búsqueda de contexto
en cada base de datos vectorial.

Autor: TP3 - Clase VII - CEIA LLMIAG
"""

import os
from typing import List, Dict, Any
from pinecone import Pinecone
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

# Cargar .env desde la raíz del proyecto
env_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', '.env')
load_dotenv(env_path)
# También intentar cargar desde directorio actual
load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
MODELO_EMBEDDINGS = "sentence-transformers/all-MiniLM-L6-v2"


class RAGTool:
    """Herramienta RAG para buscar contexto en un CV específico."""
    
    def __init__(self, cv_name: str, index_name: str, persona: str):
        """
        Inicializa la herramienta RAG.
        
        Args:
            cv_name: Nombre del CV (ej: "alumno", "pedro")
            index_name: Nombre del índice en Pinecone
            persona: Nombre de la persona del CV
        """
        if not PINECONE_API_KEY:
            raise ValueError("PINECONE_API_KEY no está configurada en .env")
        
        self.cv_name = cv_name
        self.index_name = index_name
        self.persona = persona
        
        # Inicializar Pinecone
        pc = Pinecone(api_key=PINECONE_API_KEY)
        self.index = pc.Index(index_name)
        
        # Inicializar modelo de embeddings
        self.embedding_model = SentenceTransformer(MODELO_EMBEDDINGS)
    
    def buscar_contexto(self, query: str, top_k: int = 3) -> str:
        """
        Busca contexto relevante en el CV.
        
        Args:
            query: Pregunta del usuario
            top_k: Número de chunks a recuperar
        
        Returns:
            Contexto relevante como string concatenado
        """
        # Generar embedding de query
        query_embedding = self.embedding_model.encode(query).tolist()
        
        # Buscar en Pinecone
        try:
            results = self.index.query(
                vector=query_embedding,
                top_k=top_k,
                include_metadata=True
            )
            
            # Extraer textos de chunks
            contextos = []
            for match in results['matches']:
                texto = match['metadata'].get('texto', '')
                if texto:
                    contextos.append(texto)
            
            # Concatenar contextos
            contexto_completo = '\n\n'.join(contextos)
            
            return contexto_completo
            
        except Exception as e:
            print(f"⚠️ Error al buscar en índice {self.index_name}: {e}")
            return ""
    
    def buscar_contexto_detallado(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """
        Busca contexto relevante y retorna información detallada.
        
        Args:
            query: Pregunta del usuario
            top_k: Número de chunks a recuperar
        
        Returns:
            Lista de dicts con información detallada de cada chunk
        """
        query_embedding = self.embedding_model.encode(query).tolist()
        
        try:
            results = self.index.query(
                vector=query_embedding,
                top_k=top_k,
                include_metadata=True
            )
            
            chunks_detallados = []
            for match in results['matches']:
                chunks_detallados.append({
                    "texto": match['metadata'].get('texto', ''),
                    "score": match['score'],
                    "chunk_numero": match['metadata'].get('chunk_numero', 0),
                    "persona": match['metadata'].get('persona', self.persona)
                })
            
            return chunks_detallados
            
        except Exception as e:
            print(f"⚠️ Error al buscar en índice {self.index_name}: {e}")
            return []


class RAGToolsManager:
    """Gestor de múltiples herramientas RAG."""
    
    def __init__(self):
        """Inicializa el gestor con todas las herramientas RAG."""
        self.tools = {}
        self._inicializar_tools()
    
    def _inicializar_tools(self):
        """Inicializa todas las herramientas RAG disponibles."""
        cvs_config = [
            {
                "cv_name": "alumno",
                "index_name": "cv-alumno-tp3",
                "persona": "María González"
            },
            {
                "cv_name": "pedro",
                "index_name": "cv-pedro-tp3",
                "persona": "Pedro Martínez"
            },
            {
                "cv_name": "ana",
                "index_name": "cv-ana-tp3",
                "persona": "Ana Rodríguez"
            }
        ]
        
        for config in cvs_config:
            try:
                tool = RAGTool(
                    cv_name=config["cv_name"],
                    index_name=config["index_name"],
                    persona=config["persona"]
                )
                self.tools[config["cv_name"]] = tool
                print(f"✅ Herramienta RAG inicializada: {config['persona']}")
            except Exception as e:
                print(f"⚠️ Error al inicializar herramienta para {config['cv_name']}: {e}")
    
    def obtener_tool(self, cv_name: str) -> RAGTool:
        """
        Obtiene una herramienta RAG específica.
        
        Args:
            cv_name: Nombre del CV
        
        Returns:
            RAGTool correspondiente
        """
        return self.tools.get(cv_name)
    
    def buscar_en_multiples_cvs(self, query: str, cv_names: List[str], top_k: int = 3) -> Dict[str, str]:
        """
        Busca contexto en múltiples CVs.
        
        Args:
            query: Pregunta del usuario
            cv_names: Lista de nombres de CVs a consultar
            top_k: Número de chunks por CV
        
        Returns:
            Dict con contexto de cada CV: {cv_name: contexto}
        """
        contextos = {}
        
        for cv_name in cv_names:
            tool = self.obtener_tool(cv_name)
            if tool:
                contexto = tool.buscar_contexto(query, top_k=top_k)
                contextos[cv_name] = contexto
            else:
                print(f"⚠️ No se encontró herramienta para CV: {cv_name}")
                contextos[cv_name] = ""
        
        return contextos


def main():
    """Función de prueba de las herramientas RAG."""
    print("=" * 60)
    print("TP3 - Prueba de Herramientas RAG")
    print("=" * 60)
    
    manager = RAGToolsManager()
    
    # Prueba con un CV
    print("\n📝 Prueba 1: Búsqueda en CV del alumno")
    tool_alumno = manager.obtener_tool("alumno")
    if tool_alumno:
        query = "¿Cuál es la experiencia en NLP?"
        contexto = tool_alumno.buscar_contexto(query, top_k=2)
        print(f"Query: {query}")
        print(f"Contexto encontrado:\n{contexto[:200]}...")
    
    # Prueba con múltiples CVs
    print("\n📝 Prueba 2: Búsqueda en múltiples CVs")
    query = "¿Qué experiencia tienen en Python?"
    contextos = manager.buscar_en_multiples_cvs(
        query,
        ["alumno", "pedro"],
        top_k=2
    )
    
    for cv_name, contexto in contextos.items():
        print(f"\nCV: {cv_name}")
        print(f"Contexto: {contexto[:150]}...")


if __name__ == "__main__":
    main()

