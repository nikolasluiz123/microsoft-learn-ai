from fastapi import FastAPI

app = FastAPI(
    title="Microsoft Learn AI Adaptation API",
    description="API para adaptação cognitiva de conteúdos do Microsoft Learn",
    version="1.0.0"
)

@app.get("/health")
def health_check():
    """
    Endpoint para verificação de integridade da API.
    """
    return {"status": "ok"}