Mini Workflow Engine – FastAPI Project
Overview

This project implements a Mini Workflow Engine using FastAPI.
It allows users to define a workflow as a directed graph, where each node runs a “tool” (function), updates state, and transitions to the next node based on conditions.

The engine supports:

Node execution with custom tools

Graph creation & storage

Stateful workflow execution

Conditional branching

Looping

Logging of all steps

(Optional) Live log streaming using SSE

Example workflows:
✔ Loop workflow
✔ Summarization workflow (splitting, summarizing, merging, refining)

Project Structure
my-workflow-engine/
│
├── app/
│   ├── main.py          → FastAPI endpoints
│   ├── engine.py        → Workflow execution loop
│   ├── models.py        → Pydantic models for Graph & Run
│   ├── storage.py       → In-memory storage for graphs & runs
│   ├── tools.py         → Registered workflow tools
│
├── example_workflows/
│   ├── loop_graph.json
│   ├── summarization_graph.json
│
├── requirements.txt
├── README.md

How to Run the Project
1. Clone the repository
git clone <your-github-repo-url>
cd my-workflow-engine

2. Create a virtual environment
python -m venv .venv
.\.venv\Scripts\activate       # Windows

3. Install dependencies
pip install -r requirements.txt

4. Start FastAPI server
uvicorn app.main:app --reload --port 8000

5. Open API docs
http://127.0.0.1:8000/docs


You can now:

Create graphs (POST /graph/create)

Run workflows (POST /graph/run)

Fetch run state (GET /graph/state/{run_id})

Watch logs live (GET /graph/stream/{run_id})

Example Workflow Included
1. Loop Workflow

Repeats increment → check until state["counter"] ≥ 3.

2. Summarization Workflow

Imitates a text-processing pipeline:

Split text into chunks

Summarize each chunk

Merge summaries

Refine final summary

Tools implemented:

split_text

summarize_chunk

merge_summaries

refine_summary

Final run output looks like:

{
  "final_summary": "...",
  "chunks": [...],
  "summaries": [...],
  "merged": "...",
  "finished": true
}

Features Supported by the Workflow Engine
✔ Graph Creation

Define nodes, edges, conditions.

✔ Tool Execution

Each node executes a registered function from tools.py.

✔ State Propagation

State transforms across nodes.

✔ Looping & Branching

Edges + conditions allow loops and conditional flows.

✔ Logging

Every node start & end is logged.

✔ Run Storage

Graph and run state are stored in memory.

✔ SSE Streaming (optional)

Live log updates via

GET /graph/stream/<run_id>

What I Would Improve With More Time
1. Persistent Storage

Currently memory-only. Would add SQLite/Postgres support.

2. Parallel Node Execution

Support for DAG parallelism.

3. Richer Toolset

Integrate real NLP, external API calls, async operations.

4. Visual Workflow Builder UI

Graph editor to design workflows visually.

5. Better Error Handling

Graceful failures & retries at node level.
