from dataclasses import dataclass, field
from typing import List

@dataclass
class AdaptedLessonResult:
    title: str
    text: str
    audio_url: str
    sources_used: List[str] = field(default_factory=list)