from pydantic import BaseModel
from typing import Optional


class QueryRequest(BaseModel):
    user_input : Optional[str]