from dataclasses import dataclass

@dataclass
class UserProfile:
    """
    Representa o perfil do aluno no sistema para guiar a personalização cognitiva.
    """
    user_id: str
    age_group: str
    region: str
    learning_preference: str