<p align="center">
  <img src="https://img.shields.io/badge/LangGraph-Course-6366f1?style=for-the-badge&logo=langchain&logoColor=white" alt="LangGraph Course"/>
  <img src="https://img.shields.io/badge/Python-3.10+-3776ab?style=for-the-badge&logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/LangChain-0.2+-blueviolet?style=for-the-badge&logo=chainlink&logoColor=white" alt="LangChain"/>
  <img src="https://img.shields.io/badge/Status-Active-22c55e?style=for-the-badge" alt="Status"/>
</p>

<h1 align="center">🔗 LangGraph - From Zero to Hero</h1>

<p align="center">
  <strong>A comprehensive, hands-on learning repository covering LangGraph from fundamentals to advanced agentic AI patterns.</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/github/stars/your-username/LangGraph?style=social" alt="Stars"/>
  <img src="https://img.shields.io/github/forks/your-username/LangGraph?style=social" alt="Forks"/>
  <img src="https://img.shields.io/github/issues/your-username/LangGraph?style=social" alt="Issues"/>
</p>

---

## 📖 What is LangGraph?

LangGraph is an open-source framework by LangChain for building **reliable, stateful, and complex multi-actor AI agents**. It models agent workflows as graphs—nodes represent actions or LLM calls, and edges represent control flow (loops, branching, conditionals). This structure enables agents that can reason, act, and maintain memory over long-running interactions.

---

## 📚 Course Structure

| | Module | Topics |
|---|--------|--------|
| 0️⃣ | **01 - Introduction to LangGraph** | What is LangGraph, LangChain vs LangGraph, Applications |
| 1️⃣ | **02 - Agentic AI** | What is Agentic AI, Why Agents are Popular |
| 2️⃣ | **03 - LangGraph Components** | Graph, Node, Edges, State, Tools, Supervisor, Orchestrator, Memory, LLM Workflow |
| 3️⃣ | **04 - Types of Workflows** | Sequential, Parallel, Conditional, Iterative |
| 4️⃣ | **05 - Reducers** | What is a Reducer, Why Reducers Matter |
| 5️⃣ | **06 - Persistence** | Threads, Thread IDs, Checkpointers (SQLite, Redis, PostgreSQL, Memory Saver) |
| 6️⃣ | **07 - Memory** | What is Memory, Types of Memory |
| 7️⃣ | **08 - Human-in-the-Loop** | HITL Concepts, Risk Analyzer Example |
| 8️⃣ | **09 - Types of RAG** | Self-RAG (SRAG), Corrective-RAG (CRAG) |
| 9️⃣ | **10 - Project** | End-to-End ChatBot with SQLite + FastAPI + Streamlit |

---

## ⚡ Workflow Types

The repository covers four core workflow patterns in LangGraph:

### ➡️ Sequential Workflow
Linear chain of nodes where output feeds into the next step.

- BMI Calculator
- Upper Case Transform
- Q&A Workflow
- Prompt Chaining

### 🔀 Parallel Workflow
Multiple nodes execute simultaneously for independent tasks.

- Resume Analyzer
- LinkedIn Post Generator
- Math Functions

### 🔀 Conditional Workflow
Branching logic based on state or input conditions.

- Intent Detection
- Customer Review Triage
- Organization Response
- Quadratic Equation Solver

### 🔁 Iterative Workflow
Loops that repeat until a condition is met.

- Code Review
- X (Twitter) Post Generator

---

## 🧠 Key Concepts

| Concept | Description |
|---------|-------------|
| 🔷 **StateGraph** | Define your workflow as a directed graph with typed state |
| 🟦 **Nodes** | Individual computation steps (LLM calls, tool usage, transformations) |
| 🟩 **Edges** | Control flow between nodes (direct, conditional, or dynamic) |
| 🟣 **State Persistence** | Resume conversations across sessions with checkpointers |
| 🟠 **Human-in-the-Loop** | Pause execution for human review and approval |
| 🔴 **Reducers** | Control how state updates merge across parallel branches |

---

## 💬 Project: ChatBot with SQLite + FastAPI

A production-style chatbot built with:

| Component | Technology |
|-----------|------------|
| 🔗 Framework | LangGraph |
| 🗄️ Database | SQLite |
| 🦙 LLM | Ollama (llama3.2:1b) |
| ⚡ API | FastAPI |
| 🖥️ UI | Streamlit |

### Architecture

```
┌─────────────┐     ┌──────────┐     ┌──────────┐     ┌────────────┐
│  Streamlit  │────▶│  FastAPI │────▶│ LangGraph│────▶│  Ollama    │
│     UI      │◀────│  Server  │◀────│  Graph   │◀────│   LLM      │
└─────────────┘     └──────────┘     └────┬─────┘     └────────────┘
                                          │
                                     ┌────▼─────┐
                                     │  SQLite  │
                                     │    DB    │
                                     └──────────┘
```

---

## ⏳ Prerequisites

- Python 3.10+
- pip or conda
- Ollama (for local LLM inference)

---

## 🚀 Installation

```bash
# Clone the repository
git clone https://github.com/Dev-with-Mouzan/LangGraph.git
cd LangGraph

# Install dependencies
pip install langgraph langchain langchain-core langchain-community langchain-ollama
pip install fastapi uvicorn streamlit
```

---

## ▶️ Running the Project

```bash
# Start the chatbot
cd 10-Project/ChatBot_sqlite_fasapi
python main.py

# Or run notebooks interactively
jupyter notebook 01-Intro_LangGraph/What_is_LangGraph.ipynb
```

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| 🔗 Framework | LangGraph |
| 🦙 LLM | Ollama (llama3.2:1b) |
| 🗄️ Persistence | SQLite, Redis, PostgreSQL |
| ⚡ API | FastAPI |
| 🖥️ UI | Streamlit |
| 🐍 Language | Python |


---

<p align="center">
  ✅ <strong>Built as a learning path from LangGraph basics to building production-ready agentic AI systems.</strong>
</p>

<p align="center">
  Made with ❤️ for the AI community
</p>
