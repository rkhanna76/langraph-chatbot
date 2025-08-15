"""
State definitions for the LangGraph Chatbot
"""

from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages


class State(TypedDict):
    """State definition for the chatbot graph"""
    messages: Annotated[list, add_messages]
