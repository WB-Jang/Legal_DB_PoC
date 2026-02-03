# Legal_Intelligent_DB(PoC)

프로젝트 환경

```
CPU :11th Gen Intel(R) Core(TM) i5-1145G7 @ 2.60GHz 1.50 GHz
RAM : 16GB
GPU : N/A
VRAM : N/A
폐쇄망 환경 : 시스템 구축에 필요한 라이브러리들은 .whl 파일을 통해 설치
```

## 주요 기능
- 유저의 질문과 연관이 높은 법령 내 조문들을 검색하고 요약하여 핵심 사항을 빠르게 전달함

## 주요 특징
- 법률 문서에 특화된 document_parsing.py : X장 XX조 단위로 파싱
- 부족한 리소스로 인하여 7~8b 사이즈의 모델을 프롬프트 엔지니어링 최적화하여 사용
- 금융 도메인에 파인튜닝 된 Question Decompostion 모델과 Embedding 모델 사용 가능(본 Github 내 다른 repository 참조)
- AI agent에 익숙하지 않은 유저들의 Black box에 대한 의구심과 걱정을 고려하여, 최종 답변까지 생성하는 RAG가 아니라, 관련 문서들을 요약하고 출처를 정확히 제공하는 Low level RAG system을 고안함
- ChromaDB 라이브러리가 사내 환경에 설치가 불가하여, faissDB로 대체 사용함
- 

## Reference 
1. RAG 시스템에서 document parsing은 의미론적 단위로 하는 것이 더 효과적
2. LoRA 방식으로 fine-tuning하는 것이 리소스 효율적
3. Retrival의 성능 향상을 위한 re-rank 방법론 채택
4. 다국어(특히나 아시아 언어) 성능에 우위를 보인다고 알려진 BGE-M3 임베딩 모델 사용

## Tech Stack
```
LangGraph, LangChain, 
```

## 작동 명령어
#### 현재까지는 Docker가 아닌 bash 내 python 명령어를 통하여 실행하도록 구성
```bash
python legal_agent.py
```

#### 추후 배포 단계까지 완성할 예정이며, Docker와 Poetry를 활용할 예정


