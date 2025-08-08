from agent.agent import Agent
from langchain_core.messages import HumanMessage
from qdrant.client import qdrant_service
import asyncio
from agent.config import Configuration

agent = Agent(
  qdrant_service=qdrant_service,
  config=Configuration(global_model_name="jan-nano-128k")
)

res = agent.graph.invoke({
  "messages": HumanMessage(content="Vịnh Hạ Long ở đâu?")
})


print(res)  

