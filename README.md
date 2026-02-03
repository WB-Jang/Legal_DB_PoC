# Legal_Intelligent_DB(PoC)

프로젝트 환경

```
CPU :
RAM :
GPU : N/A
VRAM : N/A
폐쇄망 환경
```
## 주요 기능
- 유저의 질문과 연관이 높은 법령 내 조문들을 검색하고 요약하여 핵심 사항을 빠르게 전달함

## 주요 특징
- 사내 폐쇄망 환경에서 작동도록 구성
- 부족한 리소스로 인하여 7~8b 사이즈의 모델을 프롬프트 엔지니어링 최적화하여 사용
- 금융 도메인에 파인튜닝 된 Question Decompostion 모델과 Embedding 모델 사용 가능(본 Github 내 다른 repository 참조)
- 

## Tech Stack

## 작동 방식
### 현재까지는 Docker가 아닌 bash 내 python 명령어를 통하여 실행하도록 구성
```bash
python legal_agent.py
```
### 추후 배포 단계까지 완성할 예정이며, Docker와 Poetry를 활용할 예정
