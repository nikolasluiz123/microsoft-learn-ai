from dataclasses import dataclass

@dataclass
class LessonContext:
    """
    Representa os metadados da lição que está sendo acessada no Microsoft Learn.
    """
    module_id: str
    module_title: str
    technical_level: str
    raw_query: str