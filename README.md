# Legal_Intelligent_DB(PoC)

## 주요 기능
- 유저의 질문과 연관이 높은 법령 내 조문들을 검색하고 요약하여 핵심 사항을 빠르게 전달함

## 주요 특징
- 사내 폐쇄망 환경에서 작동도록 구성
- 부족한 리소스를 가정하여 7~8b 사이즈의 모델을 사용
## Tech Stack

## 작동 방식
### 현재까지는 Docker가 아닌 bash 내 python 명령어를 통하여 실행하도록 구성
```bash
python legal_agent.py
```
### 추후 배포 단계까지 완성할 예정이며, Docker와 Poetry를 활용할 예정
