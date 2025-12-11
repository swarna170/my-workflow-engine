from pydantic import BaseModel
from typing import Dict, Any, List, Optional

class NodeSpec(BaseModel):
    id: str
    func: str
    params: Optional[Dict[str, Any]] = None
    condition: Optional[str] = None

class GraphSpec(BaseModel):
    id: Optional[str] = None
    nodes: Dict[str, NodeSpec]
    edges: Dict[str, List[str]]
    start_node: str

class RunState(BaseModel):
    run_id: str
    graph_id: str
    state: Dict[str, Any] = {}
    log: List[str] = []
    current_node: Optional[str] = None
    finished: bool = False

class RunRequest(BaseModel):
    graph_id: str
    initial_state: Optional[Dict[str, Any]] = None
