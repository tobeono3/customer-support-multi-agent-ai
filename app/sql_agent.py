from sqlalchemy import text
from .db import engine

SCHEMA = """
customers(id, name, email, plan, country, joined_date)
tickets(id, customer_id, created_at, subject, status, priority, resolution)
"""

def customer_lookup(name: str | None = None, email: str | None = None):
    sql = "SELECT id, name, email, plan, country, joined_date FROM customers WHERE 1=1"
    params = {}
    if name:
        sql += " AND lower(name) LIKE :name"
        params["name"] = f"%{name.lower()}%"
    if email:
        sql += " AND lower(email) = :email"
        params["email"] = email.lower()
    sql += " ORDER BY name LIMIT 10"
    with engine.connect() as conn:
        rows = [dict(r._mapping) for r in conn.execute(text(sql), params)]
    return rows

def ticket_lookup(customer_id: int | None = None, limit: int = 20):
    sql = "SELECT id, customer_id, created_at, subject, status, priority, resolution FROM tickets"
    params = {"limit": limit}
    if customer_id is not None:
        sql += " WHERE customer_id = :customer_id"
        params["customer_id"] = customer_id
    sql += " ORDER BY created_at DESC LIMIT :limit"
    with engine.connect() as conn:
        return [dict(r._mapping) for r in conn.execute(text(sql), params)]

def structured_customer_context(query: str):
    import re
    email = next(iter(re.findall(r"[\w.+-]+@[\w-]+\.[\w.-]+", query)), None)
    name = None
    quoted = re.findall(r"[\"']([^\"']+)[\"']", query)
    if quoted:
        name = quoted[0]
    else:
        m = re.search(r"(?:customer|profile|for)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)", query)
        if m:
            name = m.group(1)
    customers = customer_lookup(name=name, email=email)
    if not customers:
        # fallback: retrieve all lightweight profiles so the LLM can match spelling/context
        customers = customer_lookup()
    tickets = []
    for c in customers[:5]:
        tickets.extend(ticket_lookup(c["id"], 20))
    return {"schema": SCHEMA, "customers": customers, "tickets": tickets}
