from abc import ABC, abstractmethod

class SpeechToTextClient(ABC):
    """
    Contrato para o serviço de transcrição de áudio em texto.
    """

    @abstractmethod
    async def transcribe(self, audio_path: str) -> str:
        """
        Transcreve o arquivo de áudio presente no caminho informado para uma string de texto.
        """
        pass