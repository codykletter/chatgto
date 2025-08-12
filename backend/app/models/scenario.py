from pydantic import BaseModel
from typing import List
from app.models.gto_action import GtoAction

class Scenario(BaseModel):
    id: str
    category: str
    position: str
    stack_size: int
    hole_cards: List[str]
    community_cards: List[str]
    gto_actions: List[GtoAction]
    correct_action: GtoAction