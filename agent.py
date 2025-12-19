import os
from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage, SystemMessage
from tools import check_eligibility, apply_for_scheme  # <--- Add this
# ---------------------------------------------------------
# SETUP OPENROUTER (Using Llama 3.3 70B Free)
# ---------------------------------------------------------
OPENROUTER_API_KEY = "YOUR_API_KEY" # <--- PASTE YOUR KEY HERE

llm = ChatOpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1",
    model="kwaipilot/kat-coder-pro:free", # <--- Very stable & free
    temperature=0,
)
# ---------------------------------------------------------

# 1. Define State
class AgentState(TypedDict):
    messages: list[BaseMessage]

# 2. Bind Tools
tools = [check_eligibility, apply_for_scheme] # <--- Add it to the list
llm_with_tools = llm.bind_tools(tools)

# 3. System Prompt
SYSTEM_PROMPT = """
You are a helpful government scheme assistant for Telugu speakers.
1. Speak ONLY in Telugu (తెలుగు).
2. First, use 'check_eligibility' to find valid schemes based on Age, Income, Occupation, and Gender.
3. If they are eligible, TELL them the scheme name and ASK if they want to apply.
4. If the user says "Yes" or "Apply", use the 'apply_for_scheme' tool to submit the application.
5. Provide the Application ID to the user in Telugu.
"""
# 4. Chatbot Node
def chatbot(state: AgentState):
    # We filter messages to ensure clean history for Llama
    messages = [SystemMessage(content=SYSTEM_PROMPT)] + state["messages"]
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}

# 5. Build Graph
graph_builder = StateGraph(AgentState)
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("tools", ToolNode(tools))

graph_builder.set_entry_point("chatbot")

# 6. Logic
def should_continue(state: AgentState):
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        return "tools"
    return END

graph_builder.add_conditional_edges("chatbot", should_continue, ["tools", END])
graph_builder.add_edge("tools", "chatbot")

agent_app = graph_builder.compile()