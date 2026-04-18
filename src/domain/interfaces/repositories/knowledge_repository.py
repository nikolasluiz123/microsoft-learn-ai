from abc import ABC, abstractmethod
from typing import List

class KnowledgeRepository(ABC):
    """
    Contrato para o banco de dados vetorial de conhecimento.
    """

    @abstractmethod
    async def search_relevant_context(self, module_id: str, query: str, limit: int = 3) -> List[str]:
        """
        Busca os parágrafos mais relevantes para uma dúvida dentro de um módulo específico.
        """
        pass