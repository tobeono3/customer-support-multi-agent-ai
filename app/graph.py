from typing import TypedDict, Any
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from .config import OPENAI_MODEL
from .sql_agent import structured_customer_context
from .rag import retrieve_policy

class State(TypedDict, total=False):
    query: str
    route: str
    evidence: Any
    answer: str

def get_llm():
    return ChatOpenAI(model=OPENAI_MODEL, temperature=0)

def router(state: State):
    q = state["query"]
    llm = get_llm()
    msg = llm.invoke([
        SystemMessage(content="Classify the support question as exactly one of: structured, policy, both. Use structured for customer profiles/tickets, policy for company policy/document questions, both when both are needed. Return only the label."),
        HumanMessage(content=q)
    ])
    route = msg.content.strip().lower()
    if route not in {"structured", "policy", "both"}:
        route = "policy"
    return {"route": route}

def retrieve(state: State):
    route = state["route"]
    evidence = {}
    if route in {"structured", "both"}:
        evidence["structured"] = structured_customer_context(state["query"])
    if route in {"policy", "both"}:
        evidence["policy"] = retrieve_policy(state["query"])
    return {"evidence": evidence}

def synthesize(state: State):
    llm = get_llm()
    prompt = f"""You are a customer support assistant. Answer the user's question using ONLY the retrieved evidence below. Do not invent customer data or policy terms. If evidence is insufficient, say so. Be concise but useful. Cite document sources as [source: filename, page: N] when using policy evidence. For customer data, summarize the relevant profile and ticket history clearly.\n\nUSER QUESTION:\n{state['query']}\n\nRETRIEVED EVIDENCE:\n{state.get('evidence', {})}"""
    msg = llm.invoke([SystemMessage(content="Ground every factual claim in the supplied evidence."), HumanMessage(content=prompt)])
    return {"answer": msg.content}

def build_graph():
    g = StateGraph(State)
    g.add_node("router", router)
    g.add_node("retrieve", retrieve)
    g.add_node("synthesize", synthesize)
    g.set_entry_point("router")
    g.add_edge("router", "retrieve")
    g.add_edge("retrieve", "synthesize")
    g.add_edge("synthesize", END)
    return g.compile()

def ask(query: str):
    return build_graph().invoke({"query": query})
