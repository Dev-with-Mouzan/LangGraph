from langgraph.graph import START, END, StateGraph
from typing import TypedDict

class upper_case(TypedDict):
    input: str
    message: str


def upper(state: upper_case)->upper_case:
    """A simple function to convert text to uppercase."""
    input_text = state["input"]
    return {
        "input": input_text,
        "message": f"The uppercase version of '{input_text}' is '{input_text.upper()}'."}


graph=StateGraph(upper_case)

graph.add_node("upper", upper)

graph.add_edge(START, "upper")
graph.add_edge("upper", END)

app=graph.compile()

result=app.invoke({"input": "hello world"})

print(result["message"])