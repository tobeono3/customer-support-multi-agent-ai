from mcp.server.fastmcp import FastMCP
from app.db import init_db, seed_db
from app.sql_agent import structured_customer_context
from app.rag import retrieve_policy

mcp = FastMCP("customer-support-data")

@mcp.tool()
def search_customer_data(query: str) -> dict:
    """Search synthetic customer profiles and support tickets using natural language context."""
    return structured_customer_context(query)

@mcp.tool()
def search_policy_documents(query: str, k: int = 5) -> list[dict]:
    """Search indexed company policy PDFs and return relevant passages with source metadata."""
    return retrieve_policy(query, k)

if __name__ == "__main__":
    seed_db()
    mcp.run(transport="stdio")
