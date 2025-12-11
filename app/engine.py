import asyncio
import time
from app import tools, storage

MAX_STEPS = 500


async def maybe_await(x):
    if asyncio.iscoroutine(x):
        return await x
    return x


def safe_eval(cond: str, state: dict) -> bool:
    try:
        return bool(eval(cond, {"__builtins__": {}}, {"state": state}))
    except Exception:
        return False


async def run_graph(graph, run_state):
    steps = 0
    current = graph.start_node

    storage.push_log(run_state.run_id, f"run started: {time.strftime('%Y-%m-%d %H:%M:%S')}")

    while current and steps < MAX_STEPS:
        steps += 1
        run_state.current_node = current
        storage.push_log(run_state.run_id, f"node start: {current}")

        node = graph.nodes[current]
        fn = tools.resolve(node.func)
        if not fn:
            storage.push_log(run_state.run_id, f"unknown tool: {node.func}")
            break

        result = await maybe_await(fn(run_state.state, node.params or {}))
        if isinstance(result, dict):
            run_state.state.update(result)

        storage.push_log(run_state.run_id, f"node done: {current}")

        # choose next: first edge whose condition (if present) is true, otherwise first edge
        nexts = graph.edges.get(current, [])
        chosen = None
        for cand in nexts:
            cand_node = graph.nodes[cand]
            cond = cand_node.condition
            if not cond:
                chosen = cand
                break
            if safe_eval(cond, run_state.state):
                chosen = cand
                break

        current = chosen

    run_state.finished = True
    storage.push_log(run_state.run_id, "run finished")
