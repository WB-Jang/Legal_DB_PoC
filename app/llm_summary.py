from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from state_types import AgentState
# 먼저 Local LLM 모델을 Local sever에 띄워야 합니다
# C:\Users\1598505\OneDrive - Standard Chartered Bank\5.Python\AI\0.llama.cpp_b6295>llama-server.exe -m "C:/Users/1598505/OneDrive - Standard Chartered Bank/5.Python/AI/0.models/qwen2.5-7b-instruct-q4_k_m.gguf" -t 8 -tb 8 -c 8192 --top-p 0.9 --repeat-penalty 1.15  --host 127.0.0.1 --port 8083

BASE_URL = "http://127.0.0.1:8083/v1" #qwen2.5-7b

query ="""
    Summarize the document and point out what`s most important in it
    """
llm = ChatOpenAI(
    model="phi2.Q5",
    api_key="sk-local-any",
    base_url=BASE_URL,
    temperature = 0.7,
    # max_token=1024
)

prompt = ChatPromptTemplate.from_messages([
    ("system", """
        당신은 한국의 법령, 감독규정, 규제 문서 등을 전문적으로 다루는 법률 요약 전문가이다.
        당신의 임무는 "입력된 법률 조항"의 내용을 정확하게 요약하되,
        반드시 출처(법령명, 조문 번호, 항·호)를 명확하게 명시하는 것이다.

        요약 시 준수해야 하는 원칙:
        1. 원문의 의미를 변형하거나 확대·축소 해석하지 않는다.
        2. 법령명, 조문 번호, 항·호 등 출처 정보를 반드시 포함한다.
        3. 출처 형식은 다음 중 하나로 표준화한다:
            - 「법령명」 제00조 제0항 제0호
            - 「감독규정명」 제00조 (필요 시 항/호 포함)
        4. 생략하거나 재해석이 발생할 여지가 있는 표현은 배제하고, 법률 문장의 구조적 의미만 보존한다.
        5. 저자의 의견·추론·판단은 절대 포함하지 않는다.
        6. 여러 조항이 함께 입력되면 각 조항별로 별도의 요약 블록을 생성한다.

        출력 포맷 (고정):
        [
        {{
            "출처": "법령명 + 조문번호(항/호)",
            "요약": "출처를 기반으로 한 정확한 요약",
            "핵심요지": ["핵심 포인트 1", "핵심 포인트 2", ...]
        }}
        ]

    """),
    ("human",  "[질문]\n{user_query}\n\n[문서 내용]\n{context}")
])

chain = prompt | llm | StrOutputParser()

def llm_summary(state: AgentState):
    
    
    documents = state.result
    for i in range(len(documents)):
        document = []
        document.append(documents[i])
        print(f'요약 모델에 들어가는 {i} 번째 context input : {document}')
        generation = chain.invoke({"context": document,"user_query": query})
        print(generation)

    

