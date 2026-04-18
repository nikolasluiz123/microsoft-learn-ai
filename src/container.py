from dependency_injector import containers, providers
from src.data.clients.google_tts_client import GoogleTTSClient
from src.data.clients.gemini_llm_client import GeminiLLMClient
from src.data.clients.google_stt_client import GoogleSTTClient
from src.data.repositories.chroma_knowledge_repository import ChromaKnowledgeRepository
from src.domain.use_cases.adapt_lesson_use_case import AdaptLessonUseCase
from src.api.controllers.adaptation_controller import AdaptationController

class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=["src.api.routers.adaptation_router"])

    knowledge_repository = providers.Singleton(ChromaKnowledgeRepository)
    llm_client = providers.Singleton(GeminiLLMClient, project_id="microsoft-learn-ai")
    tts_client = providers.Singleton(GoogleTTSClient)
    stt_client = providers.Singleton(GoogleSTTClient)

    adapt_lesson_use_case = providers.Factory(
        AdaptLessonUseCase,
        knowledge_repository=knowledge_repository,
        llm_client=llm_client,
        tts_client=tts_client,
        stt_client=stt_client
    )

    adaptation_controller = providers.Factory(
        AdaptationController,
        use_case=adapt_lesson_use_case
    )