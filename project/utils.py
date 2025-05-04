import logging
from config import Config

class ConversationManager:
    """
    Keeps recent messages per‑customer in memory (last 10 by default).
    Replace with Redis or DB for multi‑process / multi‑replica setups.
    """
    def __init__(self):
        self.histories = {}

    def add_message(self, customer_id: str, role: str, content: str, max_history: int = 10):
        self.histories.setdefault(customer_id, []).append({"role": role, "content": content})
        self.histories[customer_id] = self.histories[customer_id][-max_history:]

    def get_history(self, customer_id: str):
        return self.histories.get(customer_id, [])

    def delete_history(self, customer_id: str):
        return self.histories.pop(customer_id, None)

# ------------------------------------------------------------------------

def safe_float_water_requirement(weight):
    """
    Converts weight (kg) → daily water requirement (L).
    """
    try:
        return round(float(weight) * 32.5 / 1000, 1)
    except (ValueError, TypeError):
        return "Unknown"

# ------------------------------------------------------------------------

def log_openai_usage(response):
    """
    Logs token usage + estimated USD cost.
    Compatible with openai‑python ≥1.0 (ChatCompletion object).
    """
    try:
        usage = response.usage
        prompt_t     = usage.prompt_tokens or 0
        completion_t = usage.completion_tokens or 0
        model        = response.model or "<unknown>"

        cost_in  = prompt_t     * Config.PROMPT_COST
        cost_out = completion_t * Config.OUTPUT_COST

        logging.info(
            "[OpenAI] %s | prompt %d  completion %d  →  $%.6f in  $%.6f out",
            model, prompt_t, completion_t, cost_in, cost_out
        )
    except AttributeError:
        logging.warning("No usage information found in OpenAI response")
