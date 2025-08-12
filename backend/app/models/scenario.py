from pydantic import BaseModel
from typing import List
from app.models.gto_action import GtoAction
from enum import Enum

class Street(str, Enum):
    PRE_FLOP = "pre-flop"
    POST_FLOP = "post-flop"
    TURN = "turn"
    RIVER = "river"

class Scenario(BaseModel):
    id: str
    category: str
    position: str
    stack_size: int
    hole_cards: List[str]
    community_cards: List[str]
    gto_actions: List[GtoAction]
    correct_action: GtoAction
    street: Street = Street.PRE_FLOP