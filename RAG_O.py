# RAG.py
from rag.retriever import Retriever
from rag.generator import Generator
from rag.memory import DBMemory

class RecipeRAG:
    def __init__(self):
        self.retriever = Retriever()
        self.generator = Generator()
        self.memory = DBMemory()

    def chat(self, query, user_id: int = None, filters: dict = None):
        """
        If user_id provided, include their combined history & search history into the prompt.
        Also persist new conversation turns and searches.
        """
        # record user query in memory/db
        if user_id:
            self.memory.append_turn(user_id, "user", query)
            # optionally append a search history stub here — actual snippet comes from retriever results
        # retrieval
        candidates = self.retriever.search(query)
        # Create a little snippet for search history
        snippet = candidates[0][:400] if candidates else None
        if user_id:
            self.memory.append_search(user_id, query, snippet)
        # build context including user memory
        user_context = self.memory.combined_context(user_id) if user_id else ""
        reply = self.generator.generate(query, candidates, user_context)
        # store assistant reply
        if user_id:
            self.memory.append_turn(user_id, "assistant", reply)
        return reply