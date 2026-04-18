from abc import ABC, abstractmethod

class TextToSpeechClient(ABC):
    """
    Contrato para o serviço de geração de áudio a partir de texto.
    """

    @abstractmethod
    async def generate_audio(self, text: str) -> str:
        """
        Gera um arquivo de áudio a partir do texto e retorna o caminho ou URL para acesso.
        """
        pass