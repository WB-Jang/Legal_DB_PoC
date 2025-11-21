from app._faiss import faiss_vector_db
import requests

db = faiss_vector_db(
    save_dir="../0.faiss_db",
    save_idx="privacy_idx.index",
    save_nm="privacy_store.json"
)

def rerank_by_api(query):
    search_results = db._search_db(query, k=30)
    candidate_texts = [r[0] for r in search_results]
    api_url = "http://127.0.0.1:8081/v1/rerank"
    
    payload = {
        "query": query,
        "candidates": candidate_texts
    }
    r = requests.post(api_url, json=payload, timeout=30)
    results = r.json()["results"]  # [{"text": ..., "score": ...}, ...]
    # 점수 내림차순 정렬
    return sorted(results, key=lambda x: x["score"], reverse=True)

query = "은행의 리스크 관리가 뭔가요?"
reranked_results = rerank_by_api(query)

for res in reranked_results:
    print(f"문장: {res['text']}\n서버Rerank 점수: {res['score']}")
