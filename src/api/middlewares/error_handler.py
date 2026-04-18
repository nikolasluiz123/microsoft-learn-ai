from fastapi import Request
from fastapi.responses import JSONResponse
from loguru import logger
from src.domain.exceptions.base_exceptions import BusinessException, IntegrationException
from src.api.dtos.error_dto import ErrorResponseDTO


async def custom_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Intercepta exceções geradas na aplicação e formata a resposta HTTP e os logs internos
    de acordo com a criticidade e origem do erro.
    """
    if isinstance(exc, BusinessException):
        logger.warning(f"[BUSINESS] Path: {request.url.path} | Message: {exc.message}")
        logger.opt(exception=True).debug("Stack trace de erro de negócio:")

        dto = ErrorResponseDTO(
            error_code=exc.status_code,
            error_type=exc.__class__.__name__,
            message=exc.message
        )
        return JSONResponse(status_code=exc.status_code, content=dto.model_dump())

    if isinstance(exc, IntegrationException):
        logger.error(f"[INTEGRATION] Path: {request.url.path} | Message: {exc.message}")
        logger.opt(exception=True).error("Stack trace de erro de integração:")

        dto = ErrorResponseDTO(
            error_code=exc.status_code,
            error_type=exc.__class__.__name__,
            message=exc.message
        )
        return JSONResponse(status_code=exc.status_code, content=dto.model_dump())

    logger.critical(f"[UNEXPECTED] Path: {request.url.path} | Error: {str(exc)}")
    logger.opt(exception=True).critical("Stack trace de erro inesperado:")

    dto = ErrorResponseDTO(
        error_code=500,
        error_type="InternalServerError",
        message="Ocorreu um erro interno inesperado. Tente novamente mais tarde."
    )
    return JSONResponse(status_code=500, content=dto.model_dump())