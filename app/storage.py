from typing import Dict
from app.models import GraphSpec, RunState
import uuid
import asyncio

# In-memory stores
GRAPHS: Dict[str, GraphSpec] = {}
RUNS: Dict[str, RunState] = {}
RUN_QUEUES: Dict[str, asyncio.Queue] = {}  # run_id -> queue of log strings


def save_graph(spec: GraphSpec) -> str:
    graph_id = spec.id or str(uuid.uuid4())
    spec.id = graph_id
    GRAPHS[graph_id] = spec
    return graph_id


def get_graph(graph_id: str) -> GraphSpec | None:
    return GRAPHS.get(graph_id)


def create_run(graph_id: str, initial_state: dict) -> RunState:
    run_id = str(uuid.uuid4())
    run = RunState(run_id=run_id, graph_id=graph_id, state=initial_state or {})
    RUNS[run_id] = run
    RUN_QUEUES[run_id] = asyncio.Queue()
    return run


def get_run(run_id: str) -> RunState | None:
    return RUNS.get(run_id)


def _append_log(run: RunState, message: str) -> None:
    # RunState.log is a list; just append
    run.log.append(message)


def push_log(run_id: str, message: str) -> None:
   
    run = RUNS.get(run_id)
    if run:
        _append_log(run, message)

    q = RUN_QUEUES.get(run_id)
    if q:
        try:
            q.put_nowait(message)
        except Exception:
            # if queue is full or closed, just ignore
            pass
