from datetime import datetime
from pydantic import BaseModel

class ModelCreate(BaseModel):
    name: str
    version: str
    
class ModelResponse(BaseModel):
    id: int
    name: str
    version: str
    created_at: datetime
    is_active: bool