# app/main.py
from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.responses import StreamingResponse, JSONResponse
from typing import Optional
import asyncio
import time

from app import storage, engine, models

app = FastAPI(title="Mini Workflow Engine (SSE-ready)")

# --- API endpoints ---------------------------------------------------------

@app.post("/graph/create")
async def create_graph(spec: models.GraphSpec):
    """
    Save a graph specification and return the generated graph_id.
    """
    graph_id = storage.save_graph(spec)
    return {"graph_id": graph_id}


@app.post("/graph/run")
async def run_graph(payload: models.RunRequest, background_tasks: BackgroundTasks):
    """
    Start a graph run in the background and return the run_id immediately.
    """
    graph = storage.get_graph(payload.graph_id)
    if not graph:
        raise HTTPException(status_code=404, detail="graph_id not found")

    run_state = storage.create_run(graph.id, payload.initial_state or {})

    # start the async engine in the background (uvicorn will schedule this)
    background_tasks.add_task(engine.run_graph, graph, run_state)

    return {"run_id": run_state.run_id}


@app.get("/graph/state/{run_id}")
async def get_state(run_id: str):
    """
    Return the current RunState for run_id.
    """
    run = storage.get_run(run_id)
    if not run:
        raise HTTPException(status_code=404, detail="run_id not found")
    # Pydantic models are serializable, return as dict for clarity
    return JSONResponse(content=run.dict())


@app.get("/graph/stream/{run_id}")
async def stream_run_logs(run_id: str):
    """
    Server-Sent Events endpoint that streams log lines for the given run_id.
    - First sends existing logs (if any).
    - Then yields new log lines as they are pushed by the engine via storage.push_log.
    """

    async def event_generator():
        run = storage.get_run(run_id)
        if not run:
            # immediate single message then end
            yield "data: run_id not found\n\n"
            return

        # Send any existing logs first
        for msg in run.log:
            yield f"data: {msg}\n\n"

        # Then stream new messages from the run queue
        q = storage.RUN_QUEUES.get(run_id)
        if not q:
            return

        while True:
            try:
                msg = await q.get()
                yield f"data: {msg}\n\n"
                q.task_done()
                # stop streaming once run finished
                if msg == "run finished":
                    break
            except asyncio.CancelledError:
                break

    return StreamingResponse(event_generator(), media_type="text/event-stream")


# Optional health endpoint
@app.get("/health")
async def health():
    return {"status": "ok", "time": time.strftime("%Y-%m-%d %H:%M:%S")}
