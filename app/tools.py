import asyncio

TOOL_REGISTRY = {}

def register(name):
    def decorator(fn):
        TOOL_REGISTRY[name] = fn
        return fn
    return decorator

def resolve(name):
    return TOOL_REGISTRY.get(name)

@register("noop")
def noop(state, params):
    return {}

@register("increment_counter")
def increment_counter(state, params):
    state["counter"] = state.get("counter", 0) + 1
    return {"counter": state["counter"]}

@register("async_analyze")
async def async_analyze(state, params):
    state["analysis_runs"] = state.get("analysis_runs", 0) + 1
    await asyncio.sleep(1)
    runs = state["analysis_runs"]
    quality = min(1.0, 0.3 + 0.25 * runs)
    state["quality_score"] = quality
    return {"analysis_runs": runs, "quality_score": quality}
@register("split_text")
def split_text(state, params):
    text = state.get("text", "")
    chunk_size = params.get("chunk_size", 50)
    chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
    state["chunks"] = chunks
    return {"chunks": chunks}


@register("summarize_chunk")
def summarize_chunk(state, params):
    """
    Fake summarizer: take each chunk and keep first 20 characters.
    """
    summaries = [chunk[:20] + "..." for chunk in state.get("chunks", [])]
    state["summaries"] = summaries
    return {"summaries": summaries}


@register("merge_summaries")
def merge_summaries(state, params):
    merged = " ".join(state.get("summaries", []))
    state["merged"] = merged
    return {"merged": merged}


@register("refine_summary")
def refine_summary(state, params):
    """
    Fake refinement: Trim final summary to max 100 chars.
    """
    merged = state.get("merged", "")
    refined = merged[:100] + "..."
    state["final_summary"] = refined
    return {"final_summary": refined}
