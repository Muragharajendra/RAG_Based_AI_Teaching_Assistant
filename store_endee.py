import requests
import os
import json
from endee import Endee, Precision

ENDEE_BASE_URL = "http://127.0.0.1:8080/api/v1"
INDEX_NAME = "chunks_data"
EMBEDDING_MODEL = "bge-m3"   

def create_embedding(text_list):
    r = requests.post("http://localhost:11434/api/embed", json={
        "model": EMBEDDING_MODEL,
        "input": text_list
    })
    return r.json()["embeddings"]



client = Endee()
client.set_base_url(ENDEE_BASE_URL)

try:
    client.create_index(
        name=INDEX_NAME,
        dimension=1024,
        space_type="cosine",
        precision=Precision.INT8D
    )
    print(f"Created index {INDEX_NAME}")
except Exception as e:
    print(f"Note on create_index: {e}")


index = client.get_index(name=INDEX_NAME)

if os.path.exists("json"):
    jsons = os.listdir("json")
else:
    print("Warning: 'json' directory not found.")
    jsons = []

chunk_id = 0

for json_file in jsons:
    if not json_file.endswith(".json"):
        continue
        
    with open(f"json/{json_file}") as f:
        content = json.load(f)

    print(f"Creating Embeddings for {json_file}")

    if "chunks" not in content or not content["chunks"]:
        continue

    texts = [c["text"] for c in content["chunks"]]
    embeddings = create_embedding(texts)

    vectors_to_insert = []

    for i, chunk in enumerate(content["chunks"]):
        vectors_to_insert.append({
            "id": str(chunk_id),
            "vector": embeddings[i],
            "meta": {
                "text": chunk["text"],   # store text inside meta
                "number": chunk.get("number"),
                "title": chunk.get("title"),
                "chunk_index": i,
                "source_file": json_file,
                "start": chunk.get("start"),
                "end": chunk.get("end"),
            }
        })
        chunk_id += 1

    if vectors_to_insert:
        index.upsert(vectors_to_insert)

print("✅ Stored successfully into Endee!")
print("Total stored chunks:", chunk_id)
