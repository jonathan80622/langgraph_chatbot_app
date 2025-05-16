
import os
from langchain_community.tools.tavily_search import TavilySearchResults

# Initialize and configure any external tools here
def get_search_tool(api_key: str = None, max_results: int = 2):
    key = api_key or os.getenv("TAVILY_API_KEY")
    return TavilySearchResults(max_results=max_results, tavily_api_key=key)

import os
from langchain_openai import ChatOpenAI
from langchain_core.tools import Tool
from langgraph.graph import StateGraph, START
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.graph.message import add_messages

# State definition
type_State = list  # messages list

# Prepare memory saver
memory = MemorySaver()

# Import and bind tools dynamically
from tools import get_search_tool
search_tool = get_search_tool()
tools = [search_tool]
tool_node = ToolNode(tools=tools)
llm_with_tools = llm.bind_tools(tools)

# Graph builder
def build_graph(openai_api_key, tavily_api_key, llm):
    from langgraph.graph import StateGraph
    from typing import TypedDict, Annotated
    class State(TypedDict):
        messages: Annotated[list, add_messages]

    graph_builder = StateGraph(State)

    # Chatbot node
def chatbot(state: State):
    return {"messages": [llm_with_tools.invoke(state["messages"]) ]}

    # Add nodes and edges
    graph_builder.add_node("chatbot", chatbot)
    graph_builder.add_node("tools", tool_node)
    graph_builder.add_conditional_edges("chatbot", tools_condition)
    graph_builder.add_edge(START, "chatbot")
    graph_builder.add_edge("tools", "chatbot")

    # Compile with memory
    return graph_builder.compile(checkpointer=memory)

# Expose the built graph
graph = build_graph()
