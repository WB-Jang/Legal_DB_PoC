# Quick Start Guide

이 가이드는 Legal DB PoC 프로젝트를 빠르게 시작하기 위한 단계별 지침입니다.

## 사전 준비

1. **필수 소프트웨어 설치**
   - Docker Desktop
   - Visual Studio Code (Dev Container 사용 시)
   - Poetry (로컬 실행 시)

2. **저장소 클론**
   ```bash
   git clone https://github.com/WB-Jang/Legal_DB_PoC.git
   cd Legal_DB_PoC
   ```

## 방법 1: Dev Container 사용 (가장 간단)

1. VS Code에서 프로젝트 폴더 열기
2. 왼쪽 하단의 초록색 버튼 클릭 또는 `Ctrl+Shift+P` (Mac: `Cmd+Shift+P`)
3. "Dev Containers: Reopen in Container" 선택
4. 컨테이너가 자동으로 빌드되고 종속성이 설치됩니다

## 방법 2: Docker Compose 사용

```bash
# 컨테이너 시작
docker-compose up -d

# 컨테이너 접속
docker-compose exec legal-db-poc bash

# 컨테이너 내부에서 작업 수행
```

## 방법 3: Poetry로 로컬 실행

```bash
# Poetry 설치 (처음 한 번만)
curl -sSL https://install.python-poetry.org | python3 -

# 종속성 설치
poetry install

# 가상 환경 활성화
poetry shell
```

## 코드 수정

**중요**: 실행하기 전에 다음 코드를 수정해야 합니다:

### 1. `app/legal_agent.py` 수정

```python
# 29번째 줄
req = {'user_input': input}  # 괄호 수정
```

### 2. `app/llm_keyword_extractor.py` 수정

```python
# 5번째 줄
from typing import Literal, Dict, Any  # literal -> Literal, Ant -> Any

# 35번째 줄 (함수 정의 수정)
def keywords_extractor(state: AgentState):  # state 매개변수 추가
    print('extractor 실행')
    try:
        generation = chain.invoke({"user_query": state.user_input})
        l = ast.literal_eval(generation)
        state.keywords = l
    except Exception:
        print('extractor failure')
    return {"keywords": l}
```

## 외부 서버 실행

### 1. Embedding 서버 (포트 8081)
```bash
llama-server -m "path/to/bge-m3-FP16.gguf" --embedding -t 8 -c 4092 -b 2048 -ub 2048 -np 1 --host 0.0.0.0 --port 8081
```

### 2. LLM Generation 서버 (포트 8080)
```bash
llama-server -m "path/to/model.gguf" --top-p 0.9 --repeat-penalty 1.15 --host 127.0.0.1 --port 8080
```

### 3. Rerank API 서버 (포트 8082)
```bash
# 간편 실행
./scripts/start_rerank_api.sh

# 또는
poetry run uvicorn app.rerank_api:app --host 0.0.0.0 --port 8082
```

## 애플리케이션 실행

```bash
# Poetry 환경에서
poetry run python app/legal_agent.py

# 또는 Docker 컨테이너에서
python app/legal_agent.py
```

## 문제 해결

### Docker 빌드 오류
```bash
# 캐시 없이 다시 빌드
docker-compose build --no-cache
```

### Poetry 종속성 오류
```bash
# 캐시 클리어 및 재설치
poetry cache clear pypi --all
poetry install
```

### 포트 충돌
```bash
# 사용 중인 포트 확인
netstat -an | grep 8080
netstat -an | grep 8081
netstat -an | grep 8082

# 또는 (Mac/Linux)
lsof -i :8080
lsof -i :8081
lsof -i :8082
```

## 다음 단계

1. PDF 문서를 `0.documents/` 폴더에 추가
2. FAISS 인덱스 생성 (`document_parsing.py` 실행)
3. Legal Agent 실행하여 테스트

## 도움말

자세한 내용은 [README.md](README.md)를 참조하세요.
