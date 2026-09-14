# # itertative workflow for practice in which get a topic from user explain by ollama model return if score is abovethen 50 then end otherwise repeat

# from langgraph.graph import StateGraph, START, END
# from langchain_ollama import ChatOllama
# from typing import TypedDict, Literal

# llm =ChatOllama(model="llama3.2:1b")

# class Agent_state(TypedDict):
#     Question: str
#     Answer: str
#     score: int
#     atempt:int
#     route:str

# def Ansere_genrator(state:Agent_state)->Agent_state:
#     """A function to generate an answer using ChatOllama."""
#     question = state["Question"]
#     return {"Question":question,
#             "Answer":llm.invoke(question).content,
#             "atempt":state["atempt"]+1,}


# def review_answere(state:Agent_state)->Agent_state:
#     ans=state["Answer"]
#     if len(ans)>100:
#         state["score"] += 1

#     else:
#         state["score"] += 10

#     return {"score":state["score"]}

# def check_condition(state:Agent_state)->Literal["improve","done"]:
#     if state["score"] > 5:
#         return "done"
#     else:
#         return "improve"
    

# def improver(state:Agent_state)->Agent_state:
#     ans=state["Answer"]
#     prompt=f"Improve this answer: {ans} and keep the lenght under 100 words"
#     return {"Answer":llm.invoke(prompt).content}


    

# graph=StateGraph(Agent_state)

# graph.add_node("Ansere_genrator",Ansere_genrator)
# graph.add_node("review_answere",review_answere)
# graph.add_node("check_condition",check_condition)
# graph.add_node("improve",improver)

# graph.add_edge(START,"Ansere_genrator")
# graph.add_edge("Ansere_genrator","review_answere")
# graph.add_conditional_edges("review_answere",check_condition)

# graph.add_edge("improve","Ansere_genrator")
# graph.add_edge("done",END)


# app=graph.compile()

# result=app.invoke({"Question":"what is the simple way to learn RAG","score":0,"atempt":0})
# print(result)

from langgraph.graph import (
    StateGraph,
    START,
    END
)

from typing import TypedDict, Literal
from langchain_ollama import ChatOllama



class AgentState(TypedDict):

    question:str
    answer:str
    score:int
    attempts:int



llm = ChatOllama(
    model="llama3.2:1b",
    temperature=0
)



# 1. Generate Answer

def generate_answer(
    state:AgentState
):

    response = llm.invoke(
        f"""
        Answer this question:

        {state['question']}

        Keep it simple.
        """
    )


    return {
        "answer":response.content,
        "attempts":state["attempts"]+1
    }





# 2. Review Answer

def review_answer(
    state:AgentState
):

    answer = state["answer"]


    if len(answer) < 200:

        score = 1

    else:

        score = 10


    return {
        "score":score
    }




# 3. Decision

def check_quality(
    state:AgentState
) -> Literal["improve","finish"]:


    if state["score"] < 5:
        return "improve"

    return "finish"




# Build graph


graph = StateGraph(
    AgentState
)


graph.add_node(
    "generate",
    generate_answer
)


graph.add_node(
    "review",
    review_answer
)



graph.add_edge(
    START,
    "generate"
)



graph.add_edge(
    "generate",
    "review"
)



graph.add_conditional_edges(
    "review",
    check_quality,
    {
        "improve":"generate",
        "finish":END
    }
)



app = graph.compile()



result = app.invoke(
    {
        "question":"Explain RAG",
        "answer":"",
        "score":0,
        "attempts":0
    }
)


print(result)
    