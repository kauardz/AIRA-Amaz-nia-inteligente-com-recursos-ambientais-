# -*- coding: utf-8 -*-
"""API AIRA - Amazônia e Desmatamento com FastAPI"""

import os
import requests
from datetime import date, timedelta
from dotenv import load_dotenv
from fastapi import FastAPI, Query
from pydantic import BaseModel
from langchain_google_genai import ChatGoogleGenerativeAI

# -----------------------------
# Configuração
# -----------------------------
load_dotenv()

GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY")
MAPBIOMAS_TOKEN = os.getenv("MAPBIOMAS_TOKEN")

if not GOOGLE_API_KEY:
    raise ValueError("❌ Defina GEMINI_API_KEY no arquivo .env")

if not MAPBIOMAS_TOKEN:
    raise ValueError("❌ Defina MAPBIOMAS_TOKEN no arquivo .env")

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.2,
    api_key=GOOGLE_API_KEY
)

MAPBIOMAS_URL = "https://plataforma.alerta.mapbiomas.org/api/v2/graphql"

# -----------------------------
# Funções MapBiomas
# -----------------------------
def get_alertas_mapbiomas(dias: int = 7) -> list[dict]:
    hoje = date.today()
    inicio = hoje - timedelta(days=dias)

    query = f"""
    {{
      alerts(startDate: "{inicio}", endDate: "{hoje}") {{
        id
        geomAreaHa
        date
        biome
        municipality
        state
        beforeImageUrl
        afterImageUrl
      }}
    }}
    """

    headers = {
        "Authorization": f"Bearer {MAPBIOMAS_TOKEN}",
        "Content-Type": "application/json"
    }

    r = requests.post(MAPBIOMAS_URL, headers=headers, json={"query": query})
    r.raise_for_status()
    return r.json().get("data", {}).get("alerts", [])

def formatar_alertas_texto(alertas: list[dict]) -> str:
    if not alertas:
        return "Nenhum alerta encontrado no período."
    return "\n".join([
        f"- {a['date']}: {a['geomAreaHa']} ha em {a.get('municipality','?')}/{a.get('state','?')} "
        f"({a.get('biome','?')})"
        for a in alertas
    ])

# -----------------------------
# Funções principais
# -----------------------------
def analisar_alertas(dias: int = 7) -> str:
    alertas = get_alertas_mapbiomas(dias)
    resumo = formatar_alertas_texto(alertas)

    prompt = f"""
    Seu nome é AIRA,
    Você é uma IA especializada em desmatamento.
    Analise os seguintes alertas do MapBiomas (últimos {dias} dias):

    {resumo}

    Resuma destacando:
    - Total de alertas e áreas críticas
    - Principais estados e biomas afetados
    - Qualquer tendência relevante
    """
    resposta = llm.invoke(prompt)
    return resposta.content

# -----------------------------
# API com FastAPI
# -----------------------------
app = FastAPI(title="AIRA API", description="Agente Inteligente sobre Amazônia e Desmatamento")

@app.get("/")
async def root():
    return {
        "message": "🌱 AIRA API rodando com sucesso!",
        "docs": "Acesse /docs para explorar os endpoints interativos",
        "author": "Agente AIRA"
    }

# Armazena histórico do chat em memória (simples)
chat_historico = [
    {"role": "system", "content": "Você é AIRA, IA especializada em Amazônia e desmatamento."}
]

class ChatRequest(BaseModel):
    pergunta: str

@app.get("/analise-alertas")
def endpoint_analise_alertas(dias: int = Query(7, description="Número de dias para análise")):
    """Analisar alertas de desmatamento recentes"""
    try:
        resultado = analisar_alertas(dias)
        return {"dias": dias, "analise": resultado}
    except Exception as e:
        return {"erro": str(e)}

@app.post("/chat")
def endpoint_chat(req: ChatRequest):
    """Chat interativo com memória"""
    global chat_historico

    # Adiciona pergunta no histórico
    chat_historico.append({"role": "user", "content": req.pergunta})

    # Gera resposta com base no histórico
    resposta = llm.invoke(chat_historico)

    # Adiciona resposta no histórico
    chat_historico.append({"role": "assistant", "content": resposta.content})

    return {"pergunta": req.pergunta, "resposta": resposta.content}

@app.get("/")
def root():
    return {"mensagem": "🌱 API AIRA - Amazônia e Desmatamento está rodando!"}
