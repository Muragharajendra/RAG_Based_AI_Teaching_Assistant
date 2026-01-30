import requests
from endee import Endee

ENDEE_BASE_URL = "http://127.0.0.1:8080/api/v1"
INDEX_NAME = "chunks_data"
EMBEDDING_MODEL = "bge-m3"

def create_embedding(text_list):
    r = requests.post("http://localhost:11434/api/embed", json={
        "model": EMBEDDING_MODEL,
        "input": text_list
    })
    return r.json()["embeddings"]

def run_query(query: str, top_k: int = 10):
    client = Endee()
    client.set_base_url(ENDEE_BASE_URL)
    index = client.get_index(name=INDEX_NAME)

    query_embedding = create_embedding([query])[0]

    results = index.query(vector=query_embedding, top_k=top_k)

    formatted_results = []
    for r in results:
        meta = r.get("meta", {})
        formatted_results.append({
            "id": r.get("id"),
            "score": r.get("score"),
            "text": meta.get("text"),
            "title": meta.get("title"),
            "number": meta.get("number"),
            "start": meta.get("start"),
            "end": meta.get("end"),
            "source_file": meta.get("source_file"),
        })

    return formatted_results

if __name__ == "__main__":
    q = input("Enter your question: ")
    res = run_query(q)
    print("\n✅ Results:\n", res)
