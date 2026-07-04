from langgraph.graph import START, END, StateGraph
from typing import TypedDict

class Workflow(TypedDict):
    name: str
    age: int
    message: str
    


def greet(state: Workflow):
    """A simple function to greet a person with their name and age."""
    name = state["name"]
    age = state["age"]
    return {
        "name": name,
        "age": age,
        "message": f"Hello, {name}! You are {age} years old."}


# Create a state graph
graph = StateGraph(Workflow)

# Add Nodes 
graph.add_node("greet", greet)

# Add Edges
graph.add_edge(START, "greet")
graph.add_edge("greet", END)

work=graph.compile()


result=work.invoke({"name": "Alice", "age": 30})

print(result)