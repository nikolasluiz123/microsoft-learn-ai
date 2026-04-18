from src.api.dtos.adaptation_dto import AdaptationRequest, AdaptationResponse, AdaptedContentDTO, MediaDTO, TransparencyLogDTO
from src.domain.entities.user_profile import UserProfile
from src.domain.entities.lesson_context import LessonContext
from src.domain.use_cases.adapt_lesson_use_case import AdaptLessonUseCase

class AdaptationController:
    """
    Controlador para gerenciar as requisições de adaptação de conteúdo.
    """

    def __init__(self, use_case: AdaptLessonUseCase):
        self.use_case = use_case

    async def handle_adaptation(self, request: AdaptationRequest, audio_path: str = None) -> AdaptationResponse:
        """
        Processa a requisição e aciona o Caso de Uso passando o caminho do arquivo de áudio.
        """
        profile = UserProfile(
            user_id=request.profile.user_id,
            age_group=request.profile.age_group,
            region=request.profile.region,
            learning_preference=request.profile.learning_preference
        )

        lesson = LessonContext(
            module_id=request.lesson.module_id,
            module_title=request.lesson.module_title,
            technical_level=request.lesson.technical_level,
            raw_query=request.lesson.raw_query
        )

        result = await self.use_case.execute(
            profile=profile,
            lesson=lesson,
            audio_path=audio_path
        )

        return AdaptationResponse(
            adapted_content=AdaptedContentDTO(title=result.title, text=result.text),
            media=MediaDTO(audio_url=result.audio_url),
            transparency_log=TransparencyLogDTO(sources_used=result.sources_used)
        )