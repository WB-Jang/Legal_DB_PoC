from _faiss import faiss_vector_db
from llm_keyword_extractor import AgentState
import requests

db = faiss_vector_db(
    save_dir="../0.faiss_db",
    save_idx="privacy_idx.index",
    save_nm="privacy_store.json"
)

def rerank_by_api(state: AgentState):
    candidate_texts = []
    for key in state.keywords:
        search_results = db._search_db(key, k=3)
        candidate_texts.append(search_results)
    print('1st ranking result : ',candidate_texts)
    
    api_url = "http://127.0.0.1:8082/v1/rerank"
    
    payload = {
        "query": state.user_input,
        "candidates": candidate_texts
    }
    r = requests.post(api_url, json=payload, timeout=30)
    results = r.json()["results"]  # [{"text": ..., "score": ...}, ...]
   
    return sorted(results, key=lambda x: x["score"], reverse=True)


