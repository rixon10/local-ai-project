# Local AI Agent

A fully local AI assistant built with:

- Ollama
- Llama3
- Python
- ChromaDB
- Sentence Transformers
- Rich CLI

No Azure.
No cloud APIs.
No OpenAI tokens.

Everything runs locally on your machine.

---

# Features

## AI Chat

- Local Llama3 chat assistant
- Streaming responses
- Persistent chat memory

---

## Terminal UI

Built using Rich.

Features:
- Colored terminal output
- Panels
- Structured interface

---

## Commands

| Command | Description |
|---|---|
| `/help` | Show commands |
| `/clear` | Clear terminal |
| `/reset` | Reset memory |
| `/history` | Show conversation history |
| `/model` | Show active model |
| `/exit` | Exit assistant |
| `/ingest` | Load PDF into vector DB |

---

## Tools

### Calculator

Example:

```text
55 * 22
```

---

### File Reader

Example:

```text
Explain app/main.py
```

Reads local project files and explains them.

---

### Folder Analyzer

Example:

```text
analyze app
```

Analyzes entire projects recursively.

---

### PDF RAG System

Supports:
- PDF ingestion
- embeddings
- vector search
- semantic retrieval

Example:

```text
/ingest data/pdfs/neural.pdf
```

Then ask:

```text
What does the document say about neural networks?
```

---

# Project Structure

```text
local-ai/
│
├── app/
│   ├── main.py
│   ├── llm.py
│   ├── memory.py
│   ├── tools.py
│   ├── prompts.py
│   ├── commands.py
│   ├── rag.py
│   ├── agent.py
│   ├── tool_registry.py
│
├── data/
│   ├── chat_history.json
│   ├── chroma_db/
│   └── pdfs/
│
├── requirements.txt
├── README.md
```

---

# Installation

## 1. Clone Project

```powershell
git clone <your-repo-url>
cd local-ai
```

---

## 2. Create Virtual Environment

### Windows

```powershell
python -m venv .venv
.venv\Scripts\activate
```

### Linux / Mac

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

## 3. Install Dependencies

```powershell
pip install -r requirements.txt
```

---

# Install Ollama

Download Ollama:

https://ollama.com

Install model:

```powershell
ollama pull llama3
```

Test:

```powershell
ollama run llama3
```

---

# Run Application

```powershell
python app/main.py
```

---

# RAG Workflow

## Step 1 — Add PDF

Place PDFs inside:

```text
data/pdfs/
```

---

## Step 2 — Ingest PDF

```text
/ingest data/pdfs/neural.pdf
```

---

## Step 3 — Ask Questions

```text
What does the document say about neural networks?
```

---

# Architecture

```text
User
 ↓
CLI Assistant
 ↓
LLM Agent
 ↓
Tool Router
 ↓
Tools / RAG
 ↓
Ollama (Llama3)
 ↓
Response
```

---

# Current Capabilities

- Local AI assistant
- AI tool routing
- File analysis
- Folder analysis
- PDF chatbot
- Vector search
- Embeddings
- Semantic retrieval

---

# Future Improvements

Planned upgrades:

- Multi-step agents
- Autonomous workflows
- LangGraph integration
- MCP tools
- Web search
- Browser automation
- Voice assistant
- Streamlit UI
- FastAPI backend
- Multi-agent systems

---

# Tech Stack

| Component | Technology |
|---|---|
| LLM Runtime | Ollama |
| Model | Llama3 |
| Embeddings | all-MiniLM-L6-v2 |
| Vector DB | ChromaDB |
| CLI UI | Rich |
| Backend | Python |

---

# Important Notes

## First Run

The embedding model downloads automatically from Hugging Face during first execution.

This may take a few minutes.

---

## Windows Symlink Warning

Windows may show Hugging Face cache warnings.

These are harmless.

---

# License

MIT License