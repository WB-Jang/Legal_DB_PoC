from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import List
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

# 단, 다음의 명령어로 rerank_api가 실행되고 있어야 함
# uvicorn rerank_api:app --host 0.0.0.0 --port 8082

app = FastAPI()

model_path = r"C:\\Users\\1598505\\OneDrive - Standard Chartered Bank\\5.Python\\AI\\0.models\\bge-rerank-v2-m3" #폴더 경로까지만 입력해도 괜찮음
import os 
print('현재 경로 : ', os.getcwd())
if os.path.exists(model_path):
    print('경로 존재')
else:
    print('경로 없음')

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

