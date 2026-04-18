import os
import uuid
from google.cloud import texttospeech
from src.domain.interfaces.client.text_to_speech_client import TextToSpeechClient
from src.domain.exceptions.base_exceptions import IntegrationException


class GoogleTTSClient(TextToSpeechClient):
    """
    Cliente para geração de áudio utilizando a API do Google Cloud Text-to-Speech.
    Garante o processamento de textos longos através de fatiamento sequencial (Chunking).
    """

    def __init__(self, output_directory: str = "media/audio"):
        try:
            self.client = texttospeech.TextToSpeechAsyncClient()
            self.output_directory = output_directory
            os.makedirs(self.output_directory, exist_ok=True)
        except Exception as e:
            raise IntegrationException(f"Failed to initialize Google TTS Client: {str(e)}")

    def _split_text_into_chunks(self, text: str, max_bytes: int = 4500) -> list[str]:
        """
        Divide o texto em parágrafos para garantir que nenhuma chamada
        ultrapasse o limite rígido de 5000 bytes do Google TTS.
        """
        paragraphs = text.split('\n')
        chunks = []
        current_chunk = ""

        for p in paragraphs:
            # Verifica o peso em bytes reais (UTF-8), não apenas o número de caracteres
            if len((current_chunk + p).encode('utf-8')) < max_bytes:
                current_chunk += p + "\n"
            else:
                if current_chunk.strip():
                    chunks.append(current_chunk.strip())
                current_chunk = p + "\n"

        if current_chunk.strip():
            chunks.append(current_chunk.strip())

        return chunks

    async def generate_audio(self, text: str) -> str:
        """
        Gera um arquivo MP3 a partir do texto, contornando o limite de 5000 bytes,
        e retorna o caminho relativo do arquivo unificado.
        """
        try:
            chunks = self._split_text_into_chunks(text)

            audio_config = texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.MP3
            )
            voice = texttospeech.VoiceSelectionParams(
                language_code="pt-BR",
                name="pt-BR-Neural2-B"
            )

            file_name = f"{uuid.uuid4().hex}.mp3"
            file_path = os.path.join(self.output_directory, file_name)

            with open(file_path, "ab") as final_audio_file:
                for chunk in chunks:
                    if not chunk.strip():
                        continue

                    synthesis_input = texttospeech.SynthesisInput(text=chunk)

                    response = await self.client.synthesize_speech(
                        input=synthesis_input,
                        voice=voice,
                        audio_config=audio_config
                    )

                    final_audio_file.write(response.audio_content)

            return file_path

        except Exception as e:
            raise IntegrationException(f"Error generating long audio with Google TTS: {str(e)}")