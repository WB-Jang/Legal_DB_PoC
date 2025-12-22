# Legal DB PoC

법률 데이터베이스 개념 증명 프로젝트입니다. RAG(Retrieval-Augmented Generation)와 LLM을 사용한 법률 문서 검색 시스템입니다.

## 필수 조건

- Docker
- Visual Studio Code with Dev Containers extension
- Poetry

## 로컬 환경 설정

### 1. Dev Container로 실행하기 (권장)

VS Code에서 Dev Container를 사용하여 환경을 자동으로 설정할 수 있습니다:

1. 이 저장소를 클론합니다
2. VS Code에서 프로젝트를 엽니다
3. Command Palette (Ctrl+Shift+P / Cmd+Shift+P)를 열고 "Dev Containers: Reopen in Container"를 선택합니다
4. 컨테이너가 빌드되고 모든 종속성이 자동으로 설치됩니다

### 2. Docker Compose로 실행하기 (권장)

```bash
# 컨테이너 빌드 및 시작
docker-compose up -d

# 컨테이너에 접속
docker-compose exec legal-db-poc bash

# 컨테이너 중지
docker-compose down
```

### 3. Docker로 직접 실행하기

```bash
# Docker 이미지 빌드
docker build -t legal-db-poc .

# 컨테이너 실행
docker run -it -v $(pwd):/workspace -p 8082:8082 legal-db-poc
```

### 4. Poetry로 로컬 설치

```bash
# Poetry 설치 (아직 설치하지 않은 경우)
curl -sSL https://install.python-poetry.org | python3 -

# 종속성 설치
poetry install

# 가상 환경 활성화
poetry shell
```

## 애플리케이션 실행

이 프로젝트는 여러 서버 구성 요소가 필요합니다:

### 1. Embedding 서버 (포트 8081)

외부 LLM 서버를 사용하여 텍스트 임베딩을 생성합니다. 
llama-server를 사용하는 경우:

```bash
llama-server -m "path/to/bge-m3-FP16.gguf" --embedding -t 8 -c 4092 -b 2048 -ub 2048 -np 1 --host 0.0.0.0 --port 8081
```

### 2. LLM Generation 서버 (포트 8080)

키워드 추출을 위한 LLM 서버:

```bash
llama-server -m "path/to/model.gguf" --top-p 0.9 --repeat-penalty 1.15 --host 127.0.0.1 --port 8080
```

### 3. Rerank API 서버 (포트 8082)

프로젝트 내부에서 실행:

```bash
# Poetry 환경에서
poetry run uvicorn app.rerank_api:app --host 0.0.0.0 --port 8082

# 또는 Docker 컨테이너에서
uvicorn app.rerank_api:app --host 0.0.0.0 --port 8082
```

### 4. Legal Agent 실행

```bash
# Poetry 환경에서
poetry run python app/legal_agent.py

# 또는 Docker 컨테이너에서
python app/legal_agent.py
```

## 프로젝트 구조

```
.
├── app/
│   ├── _faiss.py              # FAISS 벡터 데이터베이스 관리
│   ├── llm_keyword_extractor.py  # LLM 키워드 추출기
│   ├── rerank_api.py          # Reranking API 서버
│   ├── legal_agent.py         # 메인 법률 검색 에이전트
│   ├── Tools.py               # 유틸리티 함수
│   └── document_parsing.py    # 문서 파싱
├── 0.documents/               # PDF 문서 저장
├── 0.faiss_db/                # FAISS 인덱스 저장
├── .devcontainer/             # Dev Container 설정
│   └── devcontainer.json
├── Dockerfile                 # Docker 설정
├── docker-compose.yml         # Docker Compose 설정
├── pyproject.toml            # Poetry 종속성
├── poetry.lock               # Poetry 잠금 파일
└── .gitignore                # Git 무시 파일

```

## 주요 기능

1. **문서 파싱**: PDF 법률 문서를 구조화된 형식으로 파싱
2. **벡터 데이터베이스**: FAISS를 사용한 효율적인 유사도 검색
3. **키워드 추출**: LLM을 사용한 사용자 쿼리에서 키워드 추출
4. **Reranking**: BGE-Reranker를 사용한 검색 결과 재순위화
5. **LangGraph**: 워크플로우 관리를 위한 상태 그래프

## 개발

### 코드 포맷팅

```bash
poetry run black app/
```

### 린팅

```bash
poetry run flake8 app/
```

### 타입 체킹

```bash
poetry run mypy app/
```

## 참고 사항

- LLM 서버는 사용자가 외부에서 localhost를 통해 직접 관리해야 합니다
- 모델 파일(`.gguf`, `.bin` 등)은 `.gitignore`에 포함되어 있어 Git에 커밋되지 않습니다
- FAISS 인덱스 파일도 Git에서 제외됩니다 (필요시 로컬에서 생성)

## 알려진 문제

코드를 실행하기 전에 다음 수정이 필요합니다:

1. **app/legal_agent.py (29번째 줄)**:
   ```python
   # 수정 전
   req = {'user_input': input)
   
   # 수정 후
   req = {'user_input': input}
   ```

2. **app/llm_keyword_extractor.py (5번째 줄)**:
   ```python
   # 수정 전
   from typing import literal, Dict, Ant
   
   # 수정 후
   from typing import Literal, Dict, Any
   ```

3. **app/llm_keyword_extractor.py (38번째 줄)**:
   - `state` 변수가 정의되지 않았습니다. 함수 매개변수로 추가해야 합니다:
   ```python
   # 수정 후
   def keywords_extractor(state: AgentState):
   ```

## 라이선스

이 프로젝트는 개념 증명(PoC)입니다.
