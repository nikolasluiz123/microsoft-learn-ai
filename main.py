from fastapi import FastAPI
from src.container import Container
from src.api.routers.adaptation_router import router as adaptation_router
from src.api.middlewares.error_handler import custom_exception_handler

container = Container()

app = FastAPI(
    title="Microsoft Learn AI Adaptation API",
    version="1.0.0"
)

app.container = container

app.add_exception_handler(Exception, custom_exception_handler)
app.include_router(adaptation_router)

@app.get("/health")
def health_check():
    return {"status": "ok"}