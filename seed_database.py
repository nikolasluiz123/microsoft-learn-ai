import json
import chromadb
from loguru import logger


def popular_banco_vetorial(caminho_json: str, diretorio_chroma: str = "chroma_db"):
    """
    Lê os dados extraídos do Microsoft Learn e os insere no ChromaDB.
    """
    logger.info("Iniciando a carga de dados no ChromaDB...")

    client = chromadb.PersistentClient(path=diretorio_chroma)
    collection = client.get_or_create_collection(name="microsoft_learn_modules")

    try:
        with open(caminho_json, 'r', encoding='utf-8') as f:
            dados_curso = json.load(f)
    except FileNotFoundError:
        logger.error(f"Arquivo {caminho_json} não encontrado. Crie o arquivo com os dados extraídos.")
        return

    ids = []
    documents = []
    metadatas = []

    for item in dados_curso:
        ids.append(item["id"])
        documents.append(item["text"])
        metadatas.append({
            "module_id": item["module_id"],
            "title": item["title"]
        })

    logger.info(f"Gerando embeddings e inserindo {len(documents)} blocos de texto...")

    collection.upsert(
        ids=ids,
        documents=documents,
        metadatas=metadatas
    )

    logger.success("Carga finalizada com sucesso! O ChromaDB está pronto para responder buscas.")


if __name__ == "__main__":
    popular_banco_vetorial(caminho_json="data.json")