import json
from google import genai
from google.genai import types
from pydantic import BaseModel
from src.domain.entities.user_profile import UserProfile
from src.domain.interfaces.client.llm_client import LLMClient
from src.domain.exceptions.base_exceptions import IntegrationException


class GeminiResponseSchema(BaseModel):
    """
    Schema tipado exigido pela nova SDK do Google GenAI para forçar a saída JSON.
    """
    adapted_text: str


class GeminiLLMClient(LLMClient):
    """
    Cliente para comunicação com o modelo Gemini via Google GenAI SDK (Vertex AI Backend).
    """

    def __init__(self, project_id: str, location: str = "us-central1",
                 prompt_file_path: str = "src/data/prompts/adaptation_prompt.txt"):
        try:
            self.client = genai.Client(vertexai=True, project=project_id, location=location)
            self.model_name = "gemini-2.5-flash-lite"

            with open(prompt_file_path, "r", encoding="utf-8") as file:
                self.base_prompt = file.read()

        except Exception as e:
            raise IntegrationException(f"Failed to initialize Gemini Client: {str(e)}")

    async def generate_adaptation(self, profile: UserProfile, context: str, query: str) -> str:
        prompt = self.base_prompt.format(
            age_group=profile.age_group,
            region=profile.region,
            learning_preference=profile.learning_preference,
            context=context,
            query=query
        )

        try:
            response = await self.client.aio.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.3,
                    response_mime_type="application/json",
                    response_schema=GeminiResponseSchema,
                )
            )

            response_data = json.loads(response.text)

            return response_data["adapted_text"]
        except Exception as e:
            raise IntegrationException(f"Error communicating with Gemini API: {str(e)}")