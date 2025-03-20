import json
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class ConversationManager:
    """
    Manages conversation histories in memory.
    """
    def __init__(self):
        self.histories = {}

    def add_message(self, customer_id, role, message, max_history=10):
        if customer_id not in self.histories:
            self.histories[customer_id] = []
        self.histories[customer_id].append({"role": role, "content": message})
        # Keep only the most recent messages.
        self.histories[customer_id] = self.histories[customer_id][-max_history:]

    def get_history(self, customer_id):
        return self.histories.get(customer_id, [])

    def delete_history(self, customer_id):
        return self.histories.pop(customer_id, None)

def clean_json_string(s):
    """
    Rimuove eventuali marker markdown (es. triple backticks) dal JSON.
    """
    if s.startswith("```"):
        lines = s.splitlines()
        # Se il primo rigo inizia con ``` (eventualmente seguito da 'json'), rimuovilo.
        if lines[0].strip().startswith("```"):
            lines = lines[1:]
        # Se l'ultimo rigo contiene ``` rimuovilo.
        if lines and lines[-1].strip().startswith("```"):
            lines = lines[:-1]
        s = "\n".join(lines).strip()
    return s

def diet_check(diet_reply, target_kcal, target_proteins, target_grassi, target_carbs):
    """
    Controlla il JSON in output dalla pipeline.
    Restituisce:
      - exit_loop (bool): True se il ciclo deve essere interrotto.
      - result (dict): Il JSON parsato (o un default se l'output è vuoto/non valido).
    """
    # Se diet_reply è vuoto, ritorna subito una condizione di uscita con default.
    if not diet_reply or not diet_reply.strip():
        logger.info("diet_reply is empty; setting default response with richiesta_dieta false.")
        default_result = {
            "richiesta_dieta": False,
            "allergie_patologie": None,
            "dieta": {},
            "totali": {},
            "deviazioni_percentuali": {}
        }
        return True, default_result

    # Pulisci il JSON rimuovendo eventuali blocchi markdown.
    diet_reply_clean = clean_json_string(diet_reply)
    try:
        result = json.loads(diet_reply_clean)
        
        # Exit strategy: se la richiesta non riguarda la dieta oppure se non sono presenti informazioni su allergie/patologie.
        if not result.get("richiesta_dieta", True) or result.get("allergie_patologie") is None:
            logger.info("Exit condition met: richiesta_dieta is false or allergie_patologie is null.")
            return True, result

        deviations = result.get("deviazioni_percentuali", {})
        within_threshold = True
        for key, value in deviations.items():
            if isinstance(value, str) and value.endswith("%"):
                try:
                    percent = float(value.rstrip("%"))
                except Exception:
                    percent = 100.0
            else:
                try:
                    percent = float(value)
                except Exception:
                    percent = 100.0
            if percent > 5:
                within_threshold = False
                logger.info(f"Deviation for {key} too high: {percent}%")
                break

        if within_threshold:
            logger.info("All deviations are within the acceptable threshold.")
            return True, result
        else:
            return False, result

    except Exception as e:
        logger.error("Error in diet_check: %s", e, exc_info=True)
        return False, None
