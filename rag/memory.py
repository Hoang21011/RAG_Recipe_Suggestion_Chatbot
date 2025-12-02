# rag/memory.py
class Memory:
    def __init__(self, max_turns=6):
        self.max_turns = max_turns
        self.history = []

    def add(self, role, content):
        self.history.append({"role": role, "content": content})
        if len(self.history) > self.max_turns:
            self.history.pop(0)

    def get(self):
        return "\n".join(f"{x['role']}: {x['content']}" for x in self.history)
