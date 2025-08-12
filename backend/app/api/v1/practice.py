from fastapi import APIRouter
from typing import List
from app.models.scenario import Scenario

router = APIRouter()

mock_scenarios = [
    Scenario(
        id="1",
        category="cash_game",
        position="Button",
        stack_size=100,
        hole_cards=["As", "Ks"],
        community_cards=[],
        action_options=["Fold", "Call", "Raise"]
    ),
    Scenario(
        id="2",
        category="cash_game",
        position="Big Blind",
        stack_size=100,
        hole_cards=["7h", "2d"],
        community_cards=[],
        action_options=["Fold", "Check"]
    )
]

@router.get("/practice/scenarios/{category}", response_model=List[Scenario])
def get_scenarios_by_category(category: str):
    # In the future, this will fetch from the database
    return [s for s in mock_scenarios if s.category == category]