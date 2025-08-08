from typing import List
from pydantic import BaseModel, Field


class SearchQueryList(BaseModel):
    query: List[str] = Field(
        description="A list of search queries to be used for web research."
    )
    rationale: str = Field(
        description="A brief explanation of why these queries are relevant to the research topic."
    )


class Reflection(BaseModel):
    is_sufficient: bool = Field(
        description="Whether the provided summaries are sufficient to answer the user's question."
    )
    knowledge_gap: str = Field(
        description="A description of what information is missing"
    )
    follow_up_queries: List[str] = Field(
        description="A list of follow-up queries to address the knowledge gap. Omit if sufficient"
    )

class Answer(BaseModel):
    thought: str = Field(
        description="The agent's internal reasoning process and analysis of the information gathered to formulate the response."
    )
    response: str = Field(
        description="The final answer or response to the user's question, based on the gathered information and analysis."
    )