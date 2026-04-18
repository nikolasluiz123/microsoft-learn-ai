import os
import json
import uuid

import aiofiles
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from dependency_injector.wiring import inject, Provide
from pydantic import ValidationError
from src.container import Container
from src.api.dtos.adaptation_dto import AdaptationRequest, AdaptationResponse
from src.api.controllers.adaptation_controller import AdaptationController

router = APIRouter(
    prefix="/api/v1/adapt",
    tags=["Adaptation"]
)


@router.post("/lesson", response_model=AdaptationResponse)
@inject
async def adapt_lesson_endpoint(
        request_data: str = Form(...),
        audio_file: UploadFile = File(None),
        controller: AdaptationController = Depends(Provide[Container.adaptation_controller])
):
    """
    Recebe um payload JSON como texto via Form Data, além de um arquivo opcional em formato Multipart.
    """
    try:
        parsed_json = json.loads(request_data)
        request_dto = AdaptationRequest(**parsed_json)
    except (json.JSONDecodeError, ValidationError) as e:
        raise HTTPException(status_code=400, detail=f"Invalid JSON payload: {str(e)}")

    audio_path = None

    if audio_file:
        temp_dir = "audio_tests"
        os.makedirs(temp_dir, exist_ok=True)
        ext = audio_file.filename.split(".")[-1] if "." in audio_file.filename else "mp3"
        audio_path = os.path.join(temp_dir, f"{uuid.uuid4().hex}.{ext}")

        async with aiofiles.open(audio_path, 'wb') as out_file:
            content = await audio_file.read()
            await out_file.write(content)

    try:
        return await controller.handle_adaptation(request_dto, audio_path)
    finally:
        if audio_path and os.path.exists(audio_path):
            os.remove(audio_path)