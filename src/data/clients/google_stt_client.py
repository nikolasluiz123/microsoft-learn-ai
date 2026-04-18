from google.cloud import speech
from src.domain.interfaces.client.speech_to_text_client import SpeechToTextClient
from src.domain.exceptions.base_exceptions import IntegrationException


class GoogleSTTClient(SpeechToTextClient):
    """
    Cliente para transcrição de áudio utilizando a API do Google Cloud Speech-to-Text.
    """

    def __init__(self):
        try:
            self.client = speech.SpeechAsyncClient()
        except Exception as e:
            raise IntegrationException(f"Failed to initialize Google STT Client: {str(e)}")

    async def transcribe(self, audio_path: str) -> str:
        """
        Lê o arquivo de áudio local e o transcreve utilizando a configuração MP3 da API.
        """
        try:
            with open(audio_path, "rb") as audio_file:
                audio_content = audio_file.read()

            audio = speech.RecognitionAudio(content=audio_content)

            config = speech.RecognitionConfig(
                encoding=speech.RecognitionConfig.AudioEncoding.MP3,
                sample_rate_hertz=16000,
                language_code="pt-BR"
            )

            response = await self.client.recognize(config=config, audio=audio)

            if not response.results:
                raise IntegrationException("A transcrição não retornou palavras reconhecíveis.")

            transcript = " ".join([result.alternatives[0].transcript for result in response.results])
            return transcript.strip()

        except IntegrationException:
            raise
        except Exception as e:
            raise IntegrationException(f"Error communicating with Google STT API: {str(e)}")