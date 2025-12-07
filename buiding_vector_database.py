import pandas as pd
import chromadb
import google.generativeai as genai
from dotenv import load_dotenv
import numpy as np
from tqdm import tqdm
import time
import os

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

EMBED_MODEL = "text-embedding-004"

# Init ChromaDB (new API)
chroma_client = chromadb.PersistentClient(path="./chroma_db_final")
collection = chroma_client.get_or_create_collection("recipes")


# ----------------------------------------------------
# SAFE EMBEDDING FUNCTION (Prevent 500 Internal Error)
# ----------------------------------------------------
def embed_text(text: str):
    max_len = 5000
    parts = [text[i:i + max_len] for i in range(0, len(text), max_len)]
    vectors = []

    for part in parts:
        retry = 0
        while retry < 5:
            try:
                res = genai.embed_content(
                    model=EMBED_MODEL,
                    content=part
                )
                vectors.append(res["embedding"])
                break
            except Exception as e:
                retry += 1
                print(f"[WARN] Retry {retry}/5 due to: {e}")
                time.sleep(1)

        if retry == 5:
            raise RuntimeError("Failed to embed after 5 retries")

    return list(np.mean(vectors, axis=0))


print("Loading recipes.csv...")
df = pd.read_csv("data/cleaned_recipes.csv")


print("Generating embeddings...")
ids, docs, embs = [], [], []
batch_size = 50
total_saved = 0

# Check which recipes are already embedded
existing_ids = collection.get()["ids"]
already_embedded = set(int(id) for id in existing_ids) if existing_ids else set()
print(f"[INFO] Found {len(already_embedded)} already embedded recipes")

# tqdm loop for progress monitoring
for idx, row in tqdm(df.iterrows(), total=len(df), desc="Embedding recipes"):
    # Skip if already embedded
    if idx in already_embedded:
        continue
    
    try:
        text = f"""
Title: {row['recipe_title']}
Category: {row['category']}
Subcategory: {row['subcategory']}

Description:
{row['description']}

Ingredients:
{row['ingredients']}

Directions:
{row['directions']}
"""

        vec = embed_text(text)

        ids.append(str(idx))
        docs.append(text)
        embs.append(vec)

        # Save batch to DB when reaching batch size
        if len(ids) >= batch_size:
            collection.add(
                ids=ids,
                documents=docs,
                embeddings=embs
            )
            total_saved += len(ids)
            print(f"[INFO] Batch saved. Total recipes in DB: {total_saved}")
            ids, docs, embs = [], [], []

    except Exception as e:
        print(f"[ERROR] Failed to embed recipe {idx}: {e}")
        continue

# Save remaining batch
if len(ids) > 0:
    try:
        collection.add(
            ids=ids,
            documents=docs,
            embeddings=embs
        )
        total_saved += len(ids)
        print(f"[INFO] Final batch saved. Total recipes in DB: {total_saved}")
    except Exception as e:
        print(f"[ERROR] Failed to save final batch: {e}")

print(f"DONE! Total embeddings saved → ./chroma_db_final ({total_saved} recipes)")
