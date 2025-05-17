
import streamlit as st
from langchain_openai import ChatOpenAI
from graph_setup import build_graph

st.set_page_config(page_title="LangGraph Chatbot", layout="wide")
st.title("🔍 LangGraph-powered Chatbot with API Key Input")

# --- API Key Input ---
with st.sidebar:
    st.header("🔐 API Configuration")
    openai_key = st.text_input("OpenAI API Key", type="password")
    tavily_key = st.text_input("Tavily API Key", type="password")
    use_keys = st.button("Use Keys")

# Store in session state when user submits
if use_keys:
    if openai_key:
        st.session_state["OPENAI_API_KEY"] = openai_key
    if tavily_key:
        st.session_state["TAVILY_API_KEY"] = tavily_key
    st.success("API keys updated.")

# Ensure keys are available
if not st.session_state.get("OPENAI_API_KEY") or not st.session_state.get("TAVILY_API_KEY"):
    st.warning("Please enter both OpenAI and Tavily API keys in the sidebar.")
    st.stop()

# --- Build LangGraph with keys ---
from langchain_openai import ChatOpenAI

def get_llm(api_key: str):
    return ChatOpenAI(model="gpt-4o", temperature=0, api_key=api_key)
llm = get_llm(st.session_state["OPENAI_API_KEY"])

graph = build_graph(
    openai_api_key=st.session_state["OPENAI_API_KEY"],
    tavily_api_key=st.session_state["TAVILY_API_KEY"],
    llm=llm
)

# --- Chat session state ---
if "messages" not in st.session_state:
    st.session_state["messages"] = []

for msg in st.session_state["messages"]:
    st.chat_message(msg["role"]).write(msg["content"])

if user_input := st.chat_input("You:"):
    st.session_state["messages"].append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)

    result = graph.invoke(
        {"messages": [("user", user_input)]},
        config={"configurable": {"thread_id": "1"}}
    )
    response = result["messages"][-1].content
    st.session_state["messages"].append({"role": "assistant", "content": response})
    st.chat_message("assistant").write(response)
