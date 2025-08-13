from pydantic import BaseModel
from typing import List, Optional
from app.models.gto_action import GtoAction
from enum import Enum

class Street(str, Enum):
    PRE_FLOP = "pre-flop"
    POST_FLOP = "post-flop"
    TURN = "turn"
    RIVER = "river"

class Opponent(BaseModel):
    position: str
    hole_cards: List[str]


class Scenario(BaseModel):
    id: str
    category: str
    position: str  # Hero's position
    stack_size: int
    hole_cards: List[str]  # Hero's hole cards
    opponents: List[Opponent]
    gto_actions: List[GtoAction]
    correct_action: GtoAction
    stage: str
    flop: Optional[List[str]] = None
    turn: Optional[str] = None
    river: Optional[str] = None