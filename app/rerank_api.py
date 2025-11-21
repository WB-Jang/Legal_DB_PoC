from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import List
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

# 단, 다음의 명령어로 rerank_api가 실행되고 있어야 함
# uvicorn rerank_api:app --host 0.0.0.0 --port 8082

app = FastAPI()

model_path = "BAAI/bge-reranker-v2-m3"
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForSequenceClassification.from_pretrained(model_path)

class RerankPayload(BaseModel):
    query: str
    candidates: List[str]

@app.post("/rerank")
async def rerank(payload: RerankPayload):
    query = payload.query
    candidates = payload.candidates
    
    pairs = [(query, candidate) for candidate in candidates]
    inputs = tokenizer(pairs, padding=True, truncation=True, return_tensors="pt")
    
    model.eval()
    with torch.no_grad():
        scores = model(**inputs).logits.squeeze(-1).cpu().numpy()
    
    # 결과를 text-score dict의 리스트로 반환
    results = [
        {"text": candidate, "score": float(score)}
        for candidate, score in zip(candidates, scores)
    ]
    results_sorted = sorted(results, key=lambda x: x["score"], reverse=True)

    return {"results": results_sorted}

