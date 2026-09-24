"""
Chat Service interfacing FastAPI route with the AI Engine RAG pipeline.
"""
from typing import Dict, Any
from ai_engine.rag.rag_pipeline import RAGPipeline

class ChatService:
    def __init__(self):
        self.rag_pipeline = RAGPipeline()

    def process_chat(self, query: str, language: str = "en") -> Dict[str, Any]:
        return self.rag_pipeline.process_query(query=query, language=language)

chat_service = ChatService()
