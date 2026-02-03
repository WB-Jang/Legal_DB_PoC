from __future__ import annotations
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from typing import Literal, Dict, Any
from pydantic import BaseModel
from functools import lru_cache

import json as json
import ast 
from state_types import AgentState

# 먼저 Local LLM 모델을 Local sever에 띄워야 합니다
# C:\Users\1598505\OneDrive - Standard Chartered Bank\5.Python\AI\0.llama.cpp_b6295>llama-server.exe -m "C:/Users/1598505/OneDrive - Standard Chartered Bank/5.Python/AI/0.models/EXAONE-3.5-7.8B-Instruct-Q4_K_M.gguf" -t 8 -tb 8 -c 4096 --top-p 0.9 --repeat-penalty 1.15  --host 127.0.0.1 --port 8083
# C:\Users\1598505\OneDrive - Standard Chartered Bank\5.Python\AI\0.llama.cpp_b6295>llama-server.exe -m "C:/Users/1598505/OneDrive - Standard Chartered Bank/5.Python/AI/0.models/Qwen2.5-VL-7B-Instruct-Q4_K_M.gguf" -t 8 -tb 8 -c 8192 --top-p 0.9 --repeat-penalty 1.15  --host 127.0.0.1 --port 8080
BASE_URL = "http://127.0.0.1:8080/v1" #qwen

llm = ChatOpenAI(
    model="Qwen2.5-VL-7B-Instruct-Q4_K_M",
    api_key="sk-local-any",
    base_url=BASE_URL,
    temperature = 0.0,
    # max_token=1024
)

prompt = ChatPromptTemplate.from_messages([
    ("system", """
        당신의 임무는 ‘긴 문장으로 이루어진 질문’을 분석하여,
        해당 질문에 정확하게 답변하기 위해 반드시 필요한 핵심 키워드를 선정하는 것이다.

        핵심 키워드의 정의:
        - 질문에 대한 답변의 정확도를 결정짓는 필수 정보.
        - 해당 키워드의 내용만 주어진다면, 질문에 정확히 답할 수 있어야 한다.
        - 질문의 주변적 맥락이나 서술적 표현은 제외하고,
        논리적 필수 요소만 추출한다.

        키워드는 다음 기준을 모두 충족해야 한다:
        1) 질문의 목적을 충족하는 데 **직접적으로 필요**한 요소인가?
        2) 다른 정보 없이, 이 키워드의 정보만 있어도 **정확한 답변이 가능한가?**
        3) 질문의 결론을 결정짓는 **조건·대상·관계·행위**에 해당하는가?
        4) 일반명사가 아니라 가능한 한 **구체적**이어야 한다.

        출력 형식:
         ["키워드1", "키워드2", "키워드3", ...]
        
    """),
    ("human",  "[질문]\n{user_query}\n")
])


prompt_subquery = ChatPromptTemplate.from_messages([
    ("system", """
        역할: 너는 "규제/리스크 질문 분해 전문가(Question Decomposer for Regulatory Risk)"이다.

        입력으로 주어지는 질문은 은행 여신, 신용리스크, 규제비율, 감독규정, 내부 규정 등과 관련된 복잡한 한국어 질문이다. 너의 임무는 이 질문에 정확히 답하기 위해 반드시 알아야 하는 정보를, 짧고 단순한 하위 질문들로 분해하는 것이다.

        [원칙]
        1. 각 하위 질문은 하나의 정보만 묻는다.
        - 예: "감독규정에서 LTV 상한은 몇 %인가?" (O)
        - 예: "감독규정과 내부규정의 차이와 우선순위는 무엇인가?" (X, 두 개로 쪼갤 것) 2. 하위 질문만 읽어도 의미를 이해할 수 있도록 문맥을 포함한다.
        - "이 경우" 같은 대명사는 피하고, "중소기업 운전자금 대출"처럼 구체적으로 작성한다.
        3. 최종 질문에 답하는 데 필요하지 않은 주변 논점은 과감히 버린다.
        4. 하위 질문들은 실제 실무자가 검토 순서대로 나열된 것처럼,
        자연스러운 처리 순서를 반영하도록 정렬한다.
        5. 각 하위 질문은 1~2문장 이내로 작성한다.

        [출력 형식]
        JSON 배열만 출력하라. 예시는 다음과 같다.

        [
        "하위 질문 1 ...",
        "하위 질문 2 ..."
        ]
        
    """),
    ("human",  "[질문]\n{user_query}\n")
])

# chain = prompt | llm | StrOutputParser()
chain = prompt_subquery | llm | StrOutputParser()

def keywords_extractor(state: AgentState)->AgentState:
    print('extractor 실행 시작')
    print(type(state.rank))
    print(state.rank)
    print(type(state.rerank))
    print(state.rerank)
    try:
        generation = chain.invoke({"user_query": state.user_input})
        l = ast.literal_eval(generation)
        state.keywords = l
    except Exception:
        print('extractor failure')
    return state #현재까지 업데이트 된 state를 다음 노드로 넘기기 위해서는 return state가 필수적
    

