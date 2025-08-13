from typing import Literal
from qdrant.client import Client
from IPython.display import Image, display

from langchain_openai import ChatOpenAI
from langgraph.types import Command, Send, interrupt
from langgraph.graph import StateGraph
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.messages import SystemMessage, HumanMessage
from .config import Configuration

from .state import (
    MainState
)

from .schemas import (
    SearchQueryList,
    Reflection,
    Answer
)

from .prompts import (
    query_writer_instructions, 
    reflection_instructions,
    answer_instructions
)

from .utils import (
    get_search_topic
)


class Agent:
    def __init__(self, qdrant_service: Client, config: Configuration = Configuration(), checkpointer=None):
        self._config = config
        self._qdrant_service = qdrant_service
        
        self._workflow = StateGraph(MainState)
        
        self._workflow.add_node(
            "GENERATE_QUERY", 
            self.GENERATE_QUERY, 
            destinations={
                "SEARCH": "initialize searching"
            }
        )
        
        self._workflow.add_node(
            "SEARCH", 
            self.SEARCH,
            destinations={
                "REFLECTION": "search results"
            }
        )
        
        self._workflow.add_node(
            "REFLECTION", 
            self.REFLECTION,
            destinations={
                "SEARCH": "not sufficient",
                "ANSWER": "sufficient"
            }
            
        )
        
        self._workflow.add_node(
            "ANSWER", 
            self.ANSWER
        )
        
        
        self._workflow.set_entry_point("GENERATE_QUERY")
        self._workflow.set_finish_point("ANSWER")
        
        if checkpointer:
            self.graph = self._workflow.compile(checkpointer)
        else:
            self.graph = self._workflow.compile(checkpointer=InMemorySaver())
        
    def GENERATE_QUERY(self, state: MainState) -> Command[Literal["SEARCH"]]:
        formatted_instruction = query_writer_instructions.format(
            max_number_queries=self._config.max_number_of_queries,
            search_topic=get_search_topic(state["messages"])
        )
        
        llm = ChatOpenAI(
            model=self._config.GENERATE_QUERY_MODEL.model_name,
            api_key=self._config.GENERATE_QUERY_MODEL.api_key,
            max_retries=self._config.GENERATE_QUERY_MODEL.max_retries,
            temperature=self._config.GENERATE_QUERY_MODEL.temperature,
            base_url=self._config.GENERATE_QUERY_MODEL.base_url
        ).with_structured_output(SearchQueryList)
        
        
        response: SearchQueryList = llm.invoke(formatted_instruction)
        
        return Command(
            update={
                "search_query": response.query,
                "search_loop_count": 0
            },
            goto="SEARCH"
        )
    
    def SEARCH(self, state: MainState) -> Command[Literal["REFLECTION"]]:
        search_query: list[str] = state["search_query"]
        search_result: list[str] = [] 
        for query in search_query:
            print("Searching: ", query)
            result = [item["text"] for item in self._qdrant_service.search(query)]
            search_result.extend(result)
        
        
        return Command(
            update={
                "search_result": search_result
            },
            goto="REFLECTION"
        )
    
    def REFLECTION(self, state: MainState) -> Command[Literal["SEARCH", "ANSWER"]]:
        formatted_instruction = reflection_instructions.format(
            max_number_queries=self._config.max_number_of_queries,
            search_topic=get_search_topic(state["messages"]),
            search_result="".join(state["search_result"])
        )
        
        llm = ChatOpenAI(
            model=self._config.REFLECTION_MODEL.model_name,
            api_key=self._config.REFLECTION_MODEL.api_key,
            max_retries=self._config.REFLECTION_MODEL.max_retries,
            temperature=self._config.REFLECTION_MODEL.temperature,
            base_url=self._config.REFLECTION_MODEL.base_url
        ).with_structured_output(Reflection)
        
        
        response: Reflection = llm.invoke(formatted_instruction)
        
        if not response.is_sufficient and state["search_loop_count"] <= self._config.max_search_loops:
            return Command(
                update={
                    "search_query": response.follow_up_queries,
                    "search_loop_count": 1
                },
                goto="SEARCH"
            )
        
        return Command(
            goto="ANSWER"
        )
    
    def ANSWER(self, state: MainState) -> Command[Literal["__end__"]]: 
        formatted_instruction = answer_instructions.format(
            search_topic=get_search_topic(state["messages"]),
            search_result="".join(state["search_result"])
        )
        
        # Tạo danh sách messages với system instruction nếu có
        messages = []
        if state.get("system_instruction"):
            messages.append(SystemMessage(content=state["system_instruction"]))
        messages.append(HumanMessage(content=formatted_instruction))
        
        llm = ChatOpenAI(
            model=self._config.ANSWER_MODEL.model_name,
            api_key=self._config.ANSWER_MODEL.api_key,
            max_retries=self._config.ANSWER_MODEL.max_retries,
            temperature=self._config.ANSWER_MODEL.temperature,
            base_url=self._config.ANSWER_MODEL.base_url
        )
        
        response = llm.invoke(messages)
        
        return Command(
            update={
                "messages": response
            },
            goto="__end__"
        )
        
    
    def get_graph_visualization(self, image_path: str = "./workflow.png") -> None:
        """Generate an .png image of the current graph workflow

        Args:
            image_path (str, optional): The path to save the image. Defaults to "./workflow.png".
        """
        try:
            png_bytes = self.graph.get_graph(xray=True).draw_mermaid_png(max_retries=5, retry_delay=2)

            # Display the image
            display(Image(png_bytes))

            # Save the image to a file
            with open(image_path, "wb") as f:
                f.write(png_bytes)

        except Exception as e:
            print(f"An error occurred: {e}")
        
