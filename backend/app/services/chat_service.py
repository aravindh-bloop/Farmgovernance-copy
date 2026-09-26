"""
Chat Service interfacing FastAPI route with the AI Engine RAG pipeline.
"""
from typing import Dict, Any, List, Optional
from ai_engine.rag.rag_pipeline import RAGPipeline

class ChatService:
    def __init__(self):
        self.rag_pipeline = RAGPipeline()

    def process_chat(self, query: str, language: str = "en", history: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
        return self.rag_pipeline.process_query(query=query, language=language, history=history)

chat_service = ChatService()
