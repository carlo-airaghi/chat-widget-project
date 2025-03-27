# pipelines.py
from haystack import Pipeline
from haystack.components.generators import OpenAIGenerator
from haystack.utils import Secret
from haystack.components.retrievers.in_memory import InMemoryBM25Retriever
from haystack.components.builders.prompt_builder import PromptBuilder

class LenientPromptBuilder(PromptBuilder):
    """
    Custom PromptBuilder that ignores extra input validation.
    """
    def validate_inputs(self, **kwargs):
        # Override validation method to ignore extra inputs.
        return

    def build_prompt(self, **inputs):
        # Filter keys to only those used in the template so that missing values are ignored.
        allowed_keys = set(self.template_variables) if hasattr(self, "template_variables") else set()
        filtered_inputs = {k: v for k, v in inputs.items() if k in allowed_keys}
        return super().build_prompt(**filtered_inputs)

def create_pipeline(prompt_template: str, api_key: str, document_store, model_name: str):
    """
    Creates a Haystack pipeline with the given prompt template, API key, document store, and model name.
    """
    retriever = InMemoryBM25Retriever(document_store=document_store)
    prompt_builder = LenientPromptBuilder(template=prompt_template)
    llm = OpenAIGenerator(api_key=Secret.from_token(api_key), model=model_name)
    
    pipeline = Pipeline()
    pipeline.add_component("retriever", retriever)
    pipeline.add_component("prompt_builder", prompt_builder)
    pipeline.add_component("llm", llm)
    pipeline.connect("retriever", "prompt_builder.documents")
    pipeline.connect("prompt_builder", "llm")
    
    return pipeline