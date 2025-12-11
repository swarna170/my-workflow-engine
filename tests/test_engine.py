from app.models import GraphSpec, NodeSpec
from app.storage import save_graph, create_run
from app.engine import run_graph
import asyncio

def test_simple_run():
    graph = GraphSpec(
        nodes={
            "start": NodeSpec(id="start", func="increment_counter"),
            "end": NodeSpec(id="end", func="noop", condition="state.get(\"counter\",0) >= 1")
        },
        edges={"start": ["end"], "end": []},
        start_node="start"
    )
    gid = save_graph(graph)
    run = create_run(gid, {})
    asyncio.get_event_loop().run_until_complete(run_graph(graph, run))
    assert run.state.get("counter", 0) >= 1
    assert run.finished
