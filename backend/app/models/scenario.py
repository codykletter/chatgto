from pydantic import BaseModel
from typing import List

class Scenario(BaseModel):
    id: str
    category: str
    position: str
    stack_size: int
    hole_cards: List[str]
    community_cards: List[str]
    action_options: List[str]