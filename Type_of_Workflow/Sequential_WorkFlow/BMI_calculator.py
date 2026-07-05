from langgraph.graph import StateGraph, START,END
from typing import TypedDict

class BMI_calcul(TypedDict):
    weight: float
    height: float
    result: float 


def cal_BMI(bmi:BMI_calcul):
    h=bmi['height']
    w=bmi['weight']

    result=w/h

    return {"height":h,
            "weigjt":w,
            "result":result}


graph=StateGraph(BMI_calcul)

graph.add_node("main_fun",cal_BMI)

graph.add_edge(START,"main_fun")
graph.add_edge("main_fun",END)

app=graph.compile()

w=float(input("Enter Your Original Weight like 67.45 kg: "))
h=float(input("Enter you height in Cm like 60 cm: "))

repsonse=app.invoke({"weight":w,"height":h})
r=repsonse["result"]

if r < 18.5:
    print(f" your BMI is {r} and you are under weight")

elif r >18.5 and r < 24.9:
    print(f"Your BMI is {r} you are healthy")

else: 
    print(f"you are over weight {r}")