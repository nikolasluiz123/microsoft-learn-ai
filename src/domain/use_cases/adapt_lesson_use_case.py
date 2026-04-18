from typing import Optional
from src.domain.entities.user_profile import UserProfile
from src.domain.entities.lesson_context import LessonContext
from src.domain.entities.adapted_lesson_result import AdaptedLessonResult
from src.domain.interfaces.client.llm_client import LLMClient
from src.domain.interfaces.client.speech_to_text_client import SpeechToTextClient
from src.domain.interfaces.client.text_to_speech_client import TextToSpeechClient
from src.domain.interfaces.repositories.knowledge_repository import KnowledgeRepository

class AdaptLessonUseCase:
    """
    Caso de uso responsável por orquestrar o fluxo de adaptação cognitiva de uma lição.
    """

    def __init__(
        self,
        knowledge_repository: KnowledgeRepository,
        llm_client: LLMClient,
        tts_client: TextToSpeechClient,
        stt_client: Optional[SpeechToTextClient] = None
    ):
        self.knowledge_repository = knowledge_repository
        self.llm_client = llm_client
        self.tts_client = tts_client
        self.stt_client = stt_client

    async def execute(
        self,
        profile: UserProfile,
        lesson: LessonContext,
        audio_path: Optional[str] = None
    ) -> AdaptedLessonResult:
        """
        Executa a pipeline de processamento: Transcrição -> Busca de Contexto -> Geração -> Áudio.
        """
        query = lesson.raw_query

        if audio_path and self.stt_client:
            query = await self.stt_client.transcribe(audio_path)

        context_paragraphs = await self.knowledge_repository.search_relevant_context(
            module_id=lesson.module_id,
            query=query,
            limit=3
        )

        full_context = "\n\n".join(context_paragraphs)

        adapted_text = await self.llm_client.generate_adaptation(
            profile=profile,
            context=full_context,
            query=query
        )

        audio_url = await self.tts_client.generate_audio(text=adapted_text)

        return AdaptedLessonResult(
            title=lesson.module_title,
            text=adapted_text,
            audio_url=audio_url,
            sources_used=[f"Módulo: {lesson.module_id}"]
        )