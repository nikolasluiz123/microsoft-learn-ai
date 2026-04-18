from pydantic import BaseModel

class ErrorResponseDTO(BaseModel):
    """
    Objeto de transferência de dados para padronização de respostas de erro da API.
    """
    error_code: int
    error_type: str
    message: str