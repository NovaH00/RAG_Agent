from typing import TypedDict
from typing_extensions import Annotated, List, Optional, Dict, Any, Literal
import operator

from typing_extensions import Annotated
from langgraph.graph.message import add_messages


class MainState(TypedDict):
    messages: Annotated[list, add_messages]
    search_query: list[str]
    search_result: list[str]
    system_instruction: Optional[str]
    
    search_loop_count: Annotated[int, operator.add]