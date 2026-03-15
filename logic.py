import os
import json
import streamlit as st # <-- Add this line
from openai import OpenAI

from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.llms.openai import OpenAI as LlamaOpenAI
from llama_index.embeddings.openai import OpenAIEmbedding

# Securely pull the key from Streamlit Secrets
os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

# --- OpenAI client for triage ---
client = OpenAI()

# --- LlamaIndex settings for document Q&A ---
Settings.llm = LlamaOpenAI(model="gpt-4o-mini")
Settings.embed_model = OpenAIEmbedding(model="text-embedding-3-small")

# Build the document index once when the app starts
DATA_DIR = "data"

documents = SimpleDirectoryReader(DATA_DIR).load_data()
index = VectorStoreIndex.from_documents(documents)
query_engine = index.as_query_engine(similarity_top_k=3)


def analyze_hoa_ticket(resident_text: str) -> dict:
    """Classify a resident request into structured fields."""
    system_prompt = """
    You are an expert HOA Community Manager Assistant.
    Read the resident's request and analyze it.
    You MUST respond with a raw JSON object containing exactly these keys:
    - "category": choose one of: Maintenance, Plumbing, Security, Financial, Noise, General
    - "sentiment": choose one of: Positive, Neutral, Frustrated, Angry
    - "urgency": choose one of: Low, Medium, High, Emergency
    - "english_translation": translate to English if needed, otherwise summarize in one sentence
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": resident_text},
        ],
        response_format={"type": "json_object"},
    )

    return json.loads(response.choices[0].message.content)


def ask_documents(question: str) -> str:
    """Ask a question across all HOA PDFs."""
    response = query_engine.query(question)
    return str(response)

