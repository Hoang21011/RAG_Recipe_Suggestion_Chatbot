# rag/embedder.py
import time
import numpy as np
import google.generativeai as genai

EMBED_MODEL = "text-embedding-004"

class Embedder:
    def __init__(self):
        self.model = EMBED_MODEL

    # Safe embedding with retry
    def embed(self, text: str):
        retry = 0
        while retry < 5:
            try:
                res = genai.embed_content(
                    model=self.model,
                    content=text
                )
                return res["embedding"]
            except Exception:
                retry += 1
                time.sleep(1)
        raise RuntimeError("Failed to embed after 5 retries.")

    # Query expansion → improves search quality
    def expand_query(self, query: str):
        expansion_prompt = f"""
Expand the following cooking-related query into 3 variations 
to improve semantic search. Return ONLY phrases separated by newline.

Query: "{query}"
"""

        model = genai.GenerativeModel("gemini-2.5-flash")
        res = model.generate_content(expansion_prompt).text.strip()
        return [query] + res.split("\n")

    # Improved chunking for long recipes
    def chunk_text(self, text: str, max_len=500):
        words = text.split()
        chunks = []
        current = []

        for w in words:
            current.append(w)
            if len(current) >= max_len:
                chunks.append(" ".join(current))
                current = []

        if current:
            chunks.append(" ".join(current))

        return chunks
