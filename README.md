# LLMAPP09 - End-to-End LLMOps CI/CD Workshop

LLMAPP09 is a multi-service text-analysis application used to demonstrate an end-to-end LLMOps workflow. It combines a FastAPI backend, a Flask frontend, Ollama Cloud model routing, Langfuse observability, automated evaluation, container security scanning, Docker Hub publishing, and Kubernetes manifests.

## Architecture

| Component | Technology | Port | Purpose |
|---|---|---:|---|
| `llm-multiroute` | FastAPI | 8080 | Routes classify, sentiment, summarize, and intent requests to Ollama models |
| `llm-frontend-python` | Flask | 5000 | Browser interface and backend proxy |
| `promptfoo-tests` | Promptfoo | - | Endpoint and response-structure evaluations |
| `deepeval-tests` | DeepEval | - | LLM-as-a-judge quality evaluations |
| Langfuse | Cloud service | - | Generation tracing and token observability |

## Required accounts

- GitHub: repository and GitHub Actions
- Ollama Cloud: hosted model inference
- Docker Hub: container image registry
- OpenAI Platform: DeepEval judge model
- Langfuse Cloud: optional observability

Never commit API keys or access tokens. Local credentials belong in `.env`, which is excluded by `.gitignore`. GitHub credentials belong in repository Actions secrets.

## Local configuration

Copy the template and populate your own values:

```powershell
Copy-Item .env.example .env
```

Required or supported variables:

```dotenv
OLLAMA_API_KEY=
OLLAMA_BASE_URL=https://ollama.com
OPENAI_API_KEY=
LANGFUSE_PUBLIC_KEY=
LANGFUSE_SECRET_KEY=
LANGFUSE_BASE_URL=https://us.cloud.langfuse.com
DOCKERHUB_USERNAME=andrewtan1987
IMAGE_TAG=latest
```

The configured route models are:

| Task | Default model |
|---|---|
| Classification | `gemma4:31b` |
| Sentiment | `glm-5.2` |
| Summarization | `mistral-large-3:675b` |
| Intent detection | `minimax-m3` |

## Run with Docker Compose

Docker Desktop must have a working Linux container engine.

```powershell
docker compose up --build -d
docker compose ps
```

Open <http://localhost:5000>. The backend API and Swagger documentation are available at <http://localhost:8080/docs>.

Stop the stack with:

```powershell
docker compose down
```

## Run directly with Python

When Docker or WSL is unavailable, run the services in separate terminals.

Backend:

```powershell
cd llm-multiroute
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m uvicorn app.main:app --host 127.0.0.1 --port 8080
```

Frontend:

```powershell
cd llm-frontend-python
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

## Tests and evaluations

Backend lint and unit tests:

```powershell
cd llm-multiroute
ruff check .
pytest tests -v
```

Promptfoo evaluations require the backend on port 8080 and Node.js 22 or newer:

```powershell
cd promptfoo-tests
npm run eval
```

DeepEval requires both the backend and a valid `OPENAI_API_KEY`:

```powershell
cd deepeval-tests
pip install -r requirements.txt
deepeval test run test_classify.py test_sentiment.py test_summarize.py test_intent.py -v
```

## GitHub Actions configuration

Add these under **Settings > Secrets and variables > Actions > Repository secrets**:

| Secret | Purpose |
|---|---|
| `OLLAMA_API_KEY` | Ollama Cloud authentication |
| `OLLAMA_BASE_URL` | Ollama endpoint, normally `https://ollama.com` |
| `OPENAI_API_KEY` | DeepEval judge model |
| `DOCKERHUB_TOKEN` | Docker Hub read/write access token |

The workflows use the Docker Hub account `andrewtan1987`. Each workflow runs a preflight check that confirms required secret names are populated without displaying their values.

Four pipelines are included:

- `LLM Multiroute CI`: lint, unit tests, image build, Trivy scan, and registry push
- `LLM Frontend Python CI`: lint, image build, Trivy scan, and registry push
- `PromptFoo Tests`: four endpoint evaluation suites
- `DeepEval Tests`: LLM quality evaluation suites

Trivy HIGH or CRITICAL findings intentionally block container publication. SARIF results are uploaded to **Security > Code scanning** for remediation; the security gate is not bypassed.

## Kubernetes

Kubernetes manifests are located under each service's `k8s` directory. Replace `<dockerhub-username>` with the intended image owner and create Kubernetes Secrets before deployment.

```powershell
kubectl apply -f llm-multiroute/k8s/deployment.yaml
kubectl apply -f llm-frontend-python/k8s/deployment.yaml
```

Minikube deployment is a reference exercise and requires a working Kubernetes cluster.

## Troubleshooting

- `402 Payment Required` from Ollama: restore Ollama Cloud credits or quota.
- Docker named-pipe connection failure: start Docker Desktop and confirm its Linux engine is available.
- Evaluation preflight failure: add the named GitHub repository secret.
- Trivy gate failure: review the uploaded findings under GitHub **Security > Code scanning**.
- Never place real credentials in `.env.example`, workflow YAML, source code, commits, issues, or screenshots.
