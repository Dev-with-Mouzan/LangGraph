from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import StateGraph, START, END
from langchain_ollama import ChatOllama
from typing import TypedDict, Annotated
from langchain_core.messages import HumanMessage, AIMessage
from operator import add
from langgraph.graph import START, END, StateGraph


llm = ChatOllama(
    model="llama3.2:1b",
)

class chatstate(TypedDict):
    mesage: Annotated[list, add]

def chat_node(state:chatstate)->chatstate:
    response = llm.invoke(state["mesage"])
    return {"mesage":[AIMessage(content=response.content)]}



graph = StateGraph(chatstate)

graph.add_node("chat", chat_node)

graph.add_edge(START, "chat")
graph.add_edge("chat", END)

config={
    "configurable":{
    "thread_id":"user1"
}}

while True:
    with SqliteSaver.from_conn_string("chat_bot.db") as connection_db:
        workflow = graph.compile(checkpointer=connection_db)
        user_mg=input("Enter your message: ")
        if user_mg=='quit':
            break
        else:
            result = workflow.invoke(
        {
            "mesage":[HumanMessage(content=user_mg)]
        },
        config=config    
    )

        print(result)

    
