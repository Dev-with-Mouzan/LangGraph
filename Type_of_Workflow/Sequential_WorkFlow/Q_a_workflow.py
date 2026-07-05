from langchain_ollama import ChatOllama
from langgraph.graph import START, END, StateGraph
from typing import TypedDict

class Q_A_Workflow(TypedDict):
    question: str
    answer: str


def answer_question(state: Q_A_Workflow) -> Q_A_Workflow:
    """A function to answer a question using ChatOllama."""
    question = state["question"]
    
    # Initialize the ChatOllama model
    model = ChatOllama(model="llama3.2:1b")
    
    # Get the answer from the model
    response = model.invoke(question)
    
    return {
        "question": question,
        "answer": response.content
    }


graph = StateGraph(Q_A_Workflow)

graph.add_node("answer_question", answer_question)

graph.add_edge(START, "answer_question")
graph.add_edge("answer_question", END)

app = graph.compile()

result = app.invoke({"question": input("Enter your question: ")})

print(f"Answer: {result['answer']}")