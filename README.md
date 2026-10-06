# Customer Support Multi-Agent AI

A submission-ready reference implementation for the Generative AI Multi-Agent System assessment. It supports natural-language questions over **structured customer/ticket data in SQLite** and **unstructured policy PDFs in a Chroma vector database**, with a LangGraph router and an MCP server.

## Architecture

```text
                         ┌──────────────────────┐
                         │      Streamlit UI     │
                         └──────────┬───────────┘
                                    │ natural language
                                    ▼
                         ┌──────────────────────┐
                         │   LangGraph Router    │
                         └───────┬───────┬──────┘
                                 │       │
                    structured  │       │ policy
                                 ▼       ▼
                    ┌──────────────┐  ┌───────────────┐
                    │  SQL Agent   │  │  PDF/RAG Agent│
                    │   SQLite     │  │ Chroma + PDFs │
                    └──────┬───────┘  └───────┬───────┘
                           └──────────┬────────┘
                                      ▼
                             ┌─────────────────┐
                             │ Answer Synthesis│
                             │      LLM        │
                             └─────────────────┘

MCP server exposes the same two retrieval capabilities as tools:
- search_customer_data
- search_policy_documents
```

This directly addresses the assessment requirements for natural-language structured queries, searchable unstructured documents, context-aware responses, and an MCP server.

## Features

- Multi-agent routing with LangGraph.
- Structured customer profiles and support-ticket history in SQLite/SQLAlchemy.
- PDF ingestion with PyPDFLoader and chunking.
- Persistent Chroma vector store with OpenAI embeddings.
- Grounded answer synthesis that is instructed not to invent facts.
- MCP server exposing customer and policy retrieval tools.
- Streamlit chat UI.
- Synthetic customer dataset for demonstration.

## Project Structure

```text
.
├── app/
│   ├── config.py
│   ├── db.py
│   ├── graph.py
│   ├── rag.py
│   └── sql_agent.py
├── data/
├── documents/
├── scripts/
│   ├── index_policies.py
│   └── seed.py
├── mcp_server.py
├── streamlit_app.py
├── requirements.txt
└── .env.example
```

## Setup

### 1. Clone and create an environment

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd customer-ai-multi-agent
python -m venv .venv

# macOS/Linux
source .venv/bin/activate

# Windows PowerShell
.venv\Scripts\Activate.ps1
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure the LLM

```bash
cp .env.example .env
```

Set `OPENAI_API_KEY` in `.env`. The default model is `gpt-4o-mini`; it can be changed with `OPENAI_MODEL`.

### 4. Seed the SQL database

```bash
python scripts/seed.py
```

The synthetic dataset contains customer profiles and support tickets, including a customer named **Ema Johnson** for the assessment example.

### 5. Add policy PDFs

Place one or more publicly available company policy PDFs in `documents/`.

For example, the assessment's requirement can be satisfied with a public refund-policy PDF such as PayPro Global's published refund policy. Source: https://docs.payproglobal.com/documents/legal/refundPolicy.pdf

For a real submission, download the public PDF into `documents/` and record its source URL and retrieval date in this README.

Then index it:

```bash
python scripts/index_policies.py
```

### 6. Run the UI

```bash
streamlit run streamlit_app.py
```

Open the displayed local URL in your browser.

## Example Queries

### Policy agent

> What is the current refund policy?

The router classifies the request as `policy`, retrieves relevant PDF chunks, and generates a grounded summary with source/page references.

### Structured SQL agent

> Give me a quick overview of customer Ema's profile and past support ticket details.

The router classifies the request as `structured`, retrieves Ema's profile and ticket history from SQLite, and summarizes it.

### Multi-source question

> What refund rules apply to Ema's duplicate charge?

The router can classify this as `both`, retrieve Ema's structured support history plus relevant policy passages, and synthesize an answer from both sources.

## MCP Server

Run the MCP server over stdio:

```bash
python mcp_server.py
```

Available tools:

- `search_customer_data(query)` — searches customer profiles and support tickets.
- `search_policy_documents(query, k=5)` — searches indexed policy PDFs.

The MCP server is intentionally separated from the Streamlit process so it can be connected to an MCP-compatible client independently.

## Demo Video

`DEMO_VIDEO_URL: https://drive.google.com/file/d/1FrqrL4kXPr0v-Xn6blE7YyjNu0bj96YW/view?usp=sharing
 

### Accuracy / grounding

The answer synthesizer receives retrieved evidence and is explicitly instructed to avoid unsupported claims. Policy responses include source/page markers when document evidence is used.

### Separation of concerns

- `sql_agent.py`: structured retrieval.
- `rag.py`: unstructured retrieval.
- `graph.py`: routing and synthesis.
- `mcp_server.py`: MCP tool interface.
- `streamlit_app.py`: UI.

 
