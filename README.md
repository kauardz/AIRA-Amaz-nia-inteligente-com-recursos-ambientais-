🌱 AIRA – Agente Inteligente sobre Amazônia e Desmatamento

AIRA é um agente baseado em FastAPI + LangChain + Gemini + MapBiomas, criado para analisar alertas de desmatamento, gerar resumos inteligentes e oferecer um chat interativo sobre a Amazônia e temas relacionados.

⚙️ Funcionalidades

✅ Buscar alertas de desmatamento no MapBiomas Alerta (últimos N dias)
✅ Gerar análises automáticas com Gemini (Google Generative AI)
✅ Chat interativo sobre desmatamento, Amazônia e biomas
✅ API em FastAPI, com documentação automática (/docs)
✅ Retorno em formato JSON, pronto para integrar em sistemas

📦 Instalação
1. Clone o repositório
git clone https://github.com/kauardz/aira.git
cd aira

2. Crie um ambiente virtual (recomendado)
python -m venv venv
venv\Scripts\activate   # Windows
source venv/bin/activate  # Linux/Mac

3. Instale as dependências
pip install -r requirements.txt

🔑 Configuração

Crie um arquivo .env na raiz do projeto e adicione suas chaves:

GEMINI_API_KEY=your_gemini_api_key
MAPBIOMAS_TOKEN=your_mapbiomas_token


GEMINI_API_KEY → sua chave de API do Google Gemini

MAPBIOMAS_TOKEN → token de acesso à API do MapBiomas Alerta

🚀 Executando a API

Inicie o servidor com:

uvicorn aira:app --reload


Se o uvicorn não for reconhecido no Windows, use:

python -m uvicorn aira:app --reload

🌍 Endpoints principais
➤ Raiz /

Retorna status da API.

Exemplo de resposta:

{
  "message": "🌱 AIRA API rodando com sucesso!",
  "docs": "Acesse /docs para explorar os endpoints interativos",
  "author": "Agente AIRA"
}

➤ Documentação automática

Swagger UI → http://127.0.0.1:8000/docs

Redoc → http://127.0.0.1:8000/redoc

➤ Alertas do MapBiomas /alertas?dias=7

Busca alertas de desmatamento dos últimos N dias.

Exemplo:

GET http://127.0.0.1:8000/alertas?dias=7


Resposta:

[
  {
    "id": "abc123",
    "geomAreaHa": 25.6,
    "date": "2025-09-20",
    "biome": "Amazônia",
    "municipality": "Altamira",
    "state": "PA"
  }
]

🛠 Tecnologias utilizadas

FastAPI

Uvicorn

LangChain

Google Gemini

MapBiomas Alerta

📌 Próximos passos

 Adicionar exportação de alertas em CSV/Excel

 Suporte a múltiplos biomas

 Melhorar análise de tendências históricas

👤 Autor
Feito por Kaua Damasceno Rodrigues
💡 Inspirado na preservação da Amazônia 🌳

