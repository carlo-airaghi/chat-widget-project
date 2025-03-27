# utils.py
class ConversationManager:
    """
    Manages conversation histories in memory.
    """
    def __init__(self):
        self.histories = {}
    
    def safe_float_water_requirement(s):
        try:
            return round(float(s) * 32.5 /1000,1)
        except (ValueError, TypeError):
            return 'Unknown'  


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