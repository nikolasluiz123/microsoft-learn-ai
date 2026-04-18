from pydantic import BaseModel
from typing import List

class UserProfileDTO(BaseModel):
    """Modelo de dados para o perfil do usuário."""
    user_id: str
    age_group: str
    region: str
    learning_preference: str

class LessonContextDTO(BaseModel):
    """Modelo de dados para o contexto da lição."""
    module_id: str
    module_title: str
    technical_level: str
    raw_query: str

class AdaptationRequest(BaseModel):
    """Modelo principal de requisição (sem campos de áudio, processados separadamente)."""
    profile: UserProfileDTO
    lesson: LessonContextDTO

class AdaptedContentDTO(BaseModel):
    title: str
    text: str

class MediaDTO(BaseModel):
    audio_url: str

class TransparencyLogDTO(BaseModel):
    sources_used: List[str]

class AdaptationResponse(BaseModel):
    """Modelo principal de resposta."""
    adapted_content: AdaptedContentDTO
    media: MediaDTO
    transparency_log: TransparencyLogDTO