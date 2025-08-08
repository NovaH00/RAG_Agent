from pydantic import BaseModel, Field
from typing import Optional
import os

class ModelConfig(BaseModel):
    model_name: str = Field(
        default="jan-nano-128k",
        description="The name of the language model"
    )
    api_key: str = Field(
        default="NONE",
        description="The api key to use for the model"
    )
    max_retries: int = Field(
        default=4,
        description="The maximum number of retries when generating"
    )
    temperature: float = Field(
        default=0,
        description="The temperature used to generate the reponse"
    )
    base_url: str = Field(
        default="http://localhost:1234/v1"
    )
class Configuration(BaseModel):
    """The configuration for the agent."""
    
    # Global model override - if set, all models will use this
    global_model_name: Optional[str] = Field(
        default=None,
        description="If set, all models will use this model name instead of their individual defaults"
    )
    
    GENERATE_QUERY_MODEL: ModelConfig = Field(
        default_factory=lambda: ModelConfig(
            temperature=0.6
        )
    )
    
    REFLECTION_MODEL: ModelConfig = Field(
        default_factory=lambda: ModelConfig(
            temperature=0.6
        )
    )
    
    ANSWER_MODEL: ModelConfig = Field(
        default_factory=lambda: ModelConfig(
            temperature=0.6
        )
    )
    
    max_number_of_queries: int = Field(
        default=3,
        description="The maximum number of search queries to generate."
    )

    max_search_loops: int = Field(
        default=3,
        description="The maximum number of research loops to perform.",
    )
    
    def model_post_init(self, __context) -> None:
        """Apply global model name if specified."""
        if self.global_model_name:
            self.GENERATE_QUERY_MODEL.model_name = self.global_model_name
            self.REFLECTION_MODEL.model_name = self.global_model_name
            self.ANSWER_MODEL.model_name = self.global_model_name

    
    
    

