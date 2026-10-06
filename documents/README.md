The assessment permits any publicly available company policy documents. For the submission, add one or more public company policy PDFs here and document their source URLs in README.md.
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
                        │   LangGraph Router   │
                        └───────┬───────┬──────┘
                                │       │
                         structured    │ policy
                                │       │
                                ▼       ▼
                       ┌──────────────┐  ┌───────────────┐
                       │  SQL Agent   │  │  PDF/RAG Agent│
                       │   SQLite     │  │ Chroma + PDFs │
                       └──────┬───────┘  └───────┬───────┘
                              └──────────┬────────┘
                                         ▼
                               ┌─────────────────┐
                               │ Answer Synthesis│
                               │       LLM       │
                               └─────────────────┘

MCP server exposes the same two retrieval capabilities as tools:

- search_customer_data
- search_policy_documents
