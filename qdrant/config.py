from pydantic import BaseModel, Field

class Setting(BaseModel):
    COLLECTION_NAME: str = Field(
        default="main_collection",
        description="Tên của collection đang sử dụng"
    )
    
    EMBEDDING_MODEL: str = Field(
        default="Qwen/Qwen3-Embedding-0.6B",
        description="Tên của model sử dụng để tạo embeddings"
    )
    
    CHUNK_SIZE: int = Field(
        default=256,
        description="Số token cho mỗi chunk"
    )
    
    CHUNK_OVERLAP: int = Field(
        default=25,
        description="Số token overlap trước, và sau (Padding)"
    )
    
    TOP_K: int = Field(
        default=2,
        description="Số lượng chunk nằm trong top được chọn"
    )
    
    