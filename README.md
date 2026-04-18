## Objetivo

Esse projeto tem um objetivo simples de experimentar um pouco do uso de RAG em sua forma mais trivial, eu peguei uma
pequena parte de um curso do Microsoft Learn e coloquei em um ChromaDB usando um script python simples que está (aqui)[seed_database.py].

Depois de inicializar o banco com uma parte do curso e configurar um endpoint simples que usa APIs do Google como: Text to Speech, Speech to Text e Vertex AI
já foi possível ter alguns resultados legais gerando áudios e explicações variadas conforme o que for passado na requisição.

O projeto é só um protótipo para testar um fluxo com algumas ferramentas Google, em um cenário real várias coisas
precisariam ser melhoradas, principalmente se for rodar isso remotamente.

## Limitações de Teste

Do jeito que o projeto está estruturado como um protótipo, será preciso instalar a ferramenta do gcloud, configurar um
projeto GCP próprio com as APIs necessárias ativas, autenticar no terminal e utilizar. A intenção não é que isso seja
uma ferramenta funcional, apenas um pequeno protótipo para possivelmente evoluir em um futuro distante.

## Cenários de Teste

```json
{
  "profile": {
    "user_id": "aluno_123",
    "age_group": "Criança/Adolescente (12 a 14 anos)",
    "region": "Brasil",
    "learning_preference": "Gosta de video games, analogias divertidas e explicações passo a passo bem simples."
  },
  "lesson": {
    "module_id": "mslearn-intro-ai",
    "module_title": "Introdução aos conceitos de IA",
    "technical_level": "Iniciante",
    "raw_query": "O que é esse tal de NLP e o que ele pode fazer na prática?"
  }
}
```

```json
{
  "profile": {
    "user_id": "dev_senior_88",
    "age_group": "Adulto (30 a 40 anos)",
    "region": "Brasil",
    "learning_preference": "Direto ao ponto, técnico, com foco em casos de uso corporativos e eficiência de infraestrutura."
  },
  "lesson": {
    "module_id": "mslearn-intro-ai",
    "module_title": "Introdução aos conceitos de IA",
    "technical_level": "Intermediário",
    "raw_query": "Pode me explicar a diferença entre LLMs e SLMs? Quando eu deveria optar por um ou por outro?"
  }
}
```

```json
{
  "profile": {
    "user_id": "dev_test_01",
    "age_group": "Adulto",
    "region": "Brasil",
    "learning_preference": "Explicações técnicas com foco em arquitetura de sistemas."
  },
  "lesson": {
    "module_id": "mslearn-intro-ai",
    "module_title": "Introdução aos conceitos de IA",
    "technical_level": "Intermediário",
    "raw_query": ""
  }
}
```