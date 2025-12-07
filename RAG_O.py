# RAG.py
from rag.retriever import Retriever
from rag.generator import Generator
from rag.memory import Memory

class RecipeRAG:
    def __init__(self):
        self.retriever = Retriever()
        self.generator = Generator()
        self.memory = Memory()

    def chat(self, query):
        docs = self.retriever.search(query)
        memory_str = self.memory.get()

        reply = self.generator.generate(query, docs, memory_str)

        self.memory.add("user", query)
        self.memory.add("assistant", reply)

        return reply

    def generate_recipe(self, ingredients):
        return self.generator.generate_recipe_from_ingredients(ingredients)
