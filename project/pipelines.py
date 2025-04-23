import tiktoken
import logging
from typing import List, Dict, Any

from haystack import Pipeline, component
from haystack.components.generators import OpenAIGenerator
from haystack.utils import Secret
from haystack.components.retrievers.in_memory import InMemoryBM25Retriever
from haystack.components.builders.prompt_builder import PromptBuilder

from config import Config

@component
class TokenLogger:
    @component.output_types(replies=List[str], meta=List[Dict[str, Any]])
    def run(self, replies: List[str], meta: List[Dict[str, Any]]):
        if meta:
            usage = meta[0].get("usage", {})
            inp = usage.get("prompt_tokens", 0)
            out = usage.get("completion_tokens", 0)
            model = meta[0].get("model", "<unknown>")
            cost_in  = inp * Config.PROMPT_COST
            cost_out = out * Config.OUTPUT_COST
            logging.info(f"[TokenLogger] Model: {model}")
            logging.info(
                f"[TokenLogger] tokens → in: {inp} @${Config.PROMPT_COST}/tok = ${cost_in:.6f}, "
                f"out: {out} @${Config.OUTPUT_COST}/tok = ${cost_out:.6f}"
            )
        return {"replies": replies, "meta": meta}

class LenientPromptBuilder(PromptBuilder):
    def validate_inputs(self, **kwargs):
        return
    def build_prompt(self, **inputs):
        allowed = set(getattr(self, "template_variables", []))
        filtered = {k: v for k, v in inputs.items() if k in allowed}
        return super().build_prompt(**filtered)

def create_pipeline(prompt_template: str, api_key: str, document_store, model_name: str):
    retriever     = InMemoryBM25Retriever(document_store=document_store)
    prompt_builder= LenientPromptBuilder(template=prompt_template)
    llm = OpenAIGenerator(
        api_key      = Secret.from_token(api_key),
        model        = model_name,
        api_base_url = Config.OPENAI_API_BASE_URL,    # ← point at DeepSeek
    )
    token_logger  = TokenLogger()

    pipe = Pipeline()
    pipe.add_component("retriever",      retriever)
    pipe.add_component("prompt_builder", prompt_builder)
    pipe.add_component("llm",            llm)
    pipe.add_component("token_logger",   token_logger)

    pipe.connect("retriever",      "prompt_builder.documents")
    pipe.connect("prompt_builder", "llm.prompt")
    pipe.connect("llm.replies",    "token_logger.replies")
    pipe.connect("llm.meta",       "token_logger.meta")

    return pipe
