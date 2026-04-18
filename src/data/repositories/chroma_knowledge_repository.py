import chromadb
from typing import List
from src.domain.interfaces.repositories.knowledge_repository import KnowledgeRepository


class ChromaKnowledgeRepository(KnowledgeRepository):
    """
    Implementação do repositório de conhecimento utilizando ChromaDB para persistência local.
    """

    def __init__(self, persist_directory: str = "chroma_db"):
        self.client = chromadb.PersistentClient(path=persist_directory)
        self.collection = self.client.get_or_create_collection(name="microsoft_learn_modules")

    async def search_relevant_context(self, module_id: str, query: str, limit: int = 3) -> List[str]:
        results = self.collection.query(
            query_texts=[query],
            n_results=limit,
            where={"module_id": module_id}
        )

        if not results["documents"] or not results["documents"][0]:
            return []

        return results["documents"][0]