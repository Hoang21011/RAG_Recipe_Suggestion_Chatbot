import chromadb

client = chromadb.PersistentClient(path = "./chroma_db_final")
collection = client.get_collection('recipes')

print(collection.count())