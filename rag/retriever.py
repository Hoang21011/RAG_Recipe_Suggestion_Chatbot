# rag/retriever.py
import chromadb
import numpy as np
from rag.embedder import Embedder

class Retriever:
    def __init__(self, db_path="./chroma_db", top_k=5):
        self.embedder = Embedder()
        self.client = chromadb.PersistentClient(path=db_path)
        self.collection = self.client.get_collection("recipes")
        self.top_k = top_k

    def search(self, query: str):
        expanded_queries = self.embedder.expand_query(query)
        all_docs = []
        all_scores = []

        # Step 1 — multi-query expansion retrieval
        for q in expanded_queries:
            vec = self.embedder.embed(q)
            result = self.collection.query(
                query_embeddings=[vec],
                n_results=self.top_k
            )
            docs = result["documents"][0]
            scores = result["distances"][0]
            all_docs.extend(docs)
            all_scores.extend(scores)

        # Step 2 — reranking using embedding cosine similarity
        query_vec = np.array(self.embedder.embed(query))
        reranked = []

        for doc, sim in zip(all_docs, all_scores):
            doc_vec = np.array(self.embedder.embed(doc))
            score = np.dot(query_vec, doc_vec) / (
                np.linalg.norm(query_vec) * np.linalg.norm(doc_vec)
            )
            reranked.append((doc, score))

        # Sort by similarity
        reranked.sort(key=lambda x: x[1], reverse=True)

        # Return top unique docs
        seen = set()
        final_docs = []
        for doc, _ in reranked:
            if doc not in seen:
                final_docs.append(doc)
                seen.add(doc)
            if len(final_docs) == self.top_k:
                break

        return final_docs
