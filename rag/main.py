# main.py

import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from haystack import Pipeline, Document
from haystack.utils import Secret
from haystack.document_stores.in_memory import InMemoryDocumentStore
from haystack.components.retrievers.in_memory import InMemoryBM25Retriever
from haystack.components.builders.answer_builder import AnswerBuilder
from haystack.components.builders.prompt_builder import PromptBuilder
# Comment out the OpenAIGenerator import
from haystack.components.generators import OpenAIGenerator

# Read the API key from environment variables
api_key = os.environ.get('OPENAI_API_KEY')
if not api_key:
    raise ValueError("No OPENAI_API_KEY found in environment variables.")

# Write documents to InMemoryDocumentStore
document_store = InMemoryDocumentStore()
document_store.write_documents([
    Document(content="My name is Jean and I live in Paris."),
    Document(content="My name is Mark and I live in Berlin."),
    Document(content="My name is Giorgio and I live in Rome.")
])

# Build a RAG pipeline
prompt_template = """
Given these documents, answer the question.
Documents:
{% for doc in documents %}
    {{ doc.content }}
{% endfor %}
Question: {{question}}
Answer:
"""

retriever = InMemoryBM25Retriever(document_store=document_store)
prompt_builder = PromptBuilder(template=prompt_template)

# Define the custom LLM generator
from haystack import component
import requests
from typing import Tuple, Dict, Any

@component
class CustomLLMGenerator:
    outgoing_edges = 1  # Number of output edges

    def __init__(self, api_url):
        self.api_url = api_url

    # Explicitly accept 'prompt' as a parameter with type annotation
    def run(self, prompt: str) -> Tuple[Dict[str, Any], str]:
        if not prompt:
            return {"error": "No prompt provided"}, "output_1"
        try:
            response = requests.post(
                self.api_url,
                json={"prompt": prompt}
            )
            response.raise_for_status()
            data = response.json()
            generated_text = data.get("generated_text", "")
            return {"replies": [generated_text]}, "output_1"
        except Exception as e:
            return {"error": str(e)}, "output_1"

# Initialize your custom generator
#llm_api_url = "http://localhost:8500/generate"
#llm = CustomLLMGenerator(api_url=llm_api_url)
llm = OpenAIGenerator(api_key=Secret.from_token(api_key))


rag_pipeline = Pipeline()
rag_pipeline.add_component("retriever", retriever)
rag_pipeline.add_component("prompt_builder", prompt_builder)
rag_pipeline.add_component("llm", llm)
rag_pipeline.connect("retriever", "prompt_builder.documents")
rag_pipeline.connect("prompt_builder", "llm")

# Define FastAPI app
app = FastAPI()

class QuestionRequest(BaseModel):
    question: str

@app.post("/ask")
def ask_question(request: QuestionRequest):
    question = request.question
    results = rag_pipeline.run(
        {
            "retriever": {"query": question},
            "prompt_builder": {"question": question},
        }
    )
    return {"answer": results["llm"]["replies"]}
    # Check for errors
    # if "error" in results["llm"]:
    #     raise HTTPException(status_code=500, detail=results["llm"]["error"])
    # return {"answer": results["llm"]["replies"][0]}
