from abc import ABC, abstractmethod
from src.domain.entities.user_profile import UserProfile

class LLMClient(ABC):
    """
    Contrato para o modelo de linguagem que fará a adaptação do conteúdo.
    """

    @abstractmethod
    async def generate_adaptation(self, profile: UserProfile, context: str, query: str) -> str:
        """
        Gera um texto explicativo adaptado ao perfil do usuário com base no contexto técnico.
        """
        pass