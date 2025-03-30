import logging
import tiktoken
from typing import List, Dict, Any  # Import Dict and Any
from haystack import Pipeline
from haystack.components.generators import OpenAIGenerator
from haystack.utils import Secret
from haystack.components.retrievers.in_memory import InMemoryBM25Retriever
from haystack.components.builders.prompt_builder import PromptBuilder
from haystack import component
from config import Config

@component
class TokenLogger:
    @component.output_types(replies=List[str], meta=List[Dict[str, Any]])  # Use Dict[str, Any] here
    def run(self, replies: List[str], meta: List[Dict[str, Any]]):
        # Log token usage and cost from the meta information
        if meta:
            usage_info = meta[0].get("usage")  # e.g. OpenAI usage stats in meta[0]
            input_token_count = usage_info.get("prompt_tokens")
            output_token_count = usage_info.get("completion_tokens")
            model = meta[0].get("model")
            input_cost = input_token_count*Config.PROMPT_COST
            output_cost = output_token_count*Config.OUTPUT_COST
            print(f"[Logging] Model {model}")
            print(f"[Logging] Input Token Count {input_token_count}, Output Token Count {output_token_count}")
            print(f"[Logging] Input Token Cost {input_cost}$, Output Token Cost {output_cost}$")
        # Pass through the data unchanged
        return {"replies": replies, "meta": meta}

class LenientPromptBuilder(PromptBuilder):
    """
    Custom PromptBuilder that ignores extra input validation.
    """
    def validate_inputs(self, **kwargs):
        return

    def build_prompt(self, **inputs):
        allowed_keys = set(self.template_variables) if hasattr(self, "template_variables") else set()
        filtered_inputs = {k: v for k, v in inputs.items() if k in allowed_keys}
        return super().build_prompt(**filtered_inputs)

def create_pipeline(prompt_template: str, api_key: str, document_store, model_name: str):
    retriever = InMemoryBM25Retriever(document_store=document_store)
    prompt_builder = LenientPromptBuilder(template=prompt_template)
    llm = OpenAIGenerator(api_key=Secret.from_token(api_key), model=model_name)
    token_logger = TokenLogger()

    pipeline = Pipeline()
    pipeline.add_component("retriever", retriever)
    pipeline.add_component("prompt_builder", prompt_builder)
    pipeline.add_component("llm", llm)
    pipeline.add_component("token_logger", token_logger)

    pipeline.connect("retriever", "prompt_builder.documents")
    pipeline.connect("prompt_builder", "llm.prompt")
    pipeline.connect("llm.replies", "token_logger.replies")
    pipeline.connect("llm.meta", "token_logger.meta")

    return pipeline
