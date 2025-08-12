from pydantic import BaseModel
from typing import Optional

class GtoAction(BaseModel):
    action: str
    ev: float
    explanation: Optional[str] = None