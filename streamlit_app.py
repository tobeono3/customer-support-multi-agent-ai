import streamlit as st
from app.db import seed_db
from app.rag import build_vector_store
from app.graph import ask
from app.config import POLICY_DIR

st.set_page_config(page_title="Customer Support Multi-Agent AI", page_icon="🤖", layout="wide")
seed_db()

st.title("🤖 Customer Support Multi-Agent AI")
st.caption("LangGraph router • SQL customer agent • PDF policy agent • MCP tools")

with st.sidebar:
    st.header("Knowledge Base")
    st.write(f"Policy directory: `{POLICY_DIR}`")
    if st.button("Index / refresh policy PDFs"):
        try:
            _, added = build_vector_store()
            st.success(f"Indexed {added} new chunks.")
        except Exception as e:
            st.error(str(e))
    st.divider()
    st.markdown("**Try:**")
    st.code("What is the refund policy?")
    st.code("Give me an overview of customer Ema's profile and support tickets.")
    st.code("What refund rules apply to Ema's duplicate charge?")

if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

query = st.chat_input("Ask about a customer or company policy...")
if query:
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)
    with st.chat_message("assistant"):
        with st.spinner("Routing to the right agent..."):
            try:
                result = ask(query)
                answer = result["answer"]
                st.markdown(answer)
            except Exception as e:
                answer = f"I couldn't complete the request: {e}"
                st.error(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})
