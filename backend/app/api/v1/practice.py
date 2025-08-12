from fastapi import APIRouter, HTTPException
from typing import List
from app.models.attempt import Attempt
from app.models.scenario import Scenario, Street
from app.models.gto_action import GtoAction

router = APIRouter()

# Enhanced Mock Data with EV and Explanations
mock_scenarios = [
    Scenario(
        id="1",
        category="cash_game",
        position="Button",
        stack_size=100,
        hole_cards=["As", "Ks"],
        community_cards=[],
        street=Street.PRE_FLOP,
        gto_actions=[
            GtoAction(action="Fold", ev=-0.5, explanation="Folding is a significant EV loss with a premium hand like AKs."),
            GtoAction(action="Call", ev=8.0, explanation="Calling is profitable, but raising is optimal to isolate and build a pot."),
            GtoAction(action="Raise", ev=10.0, explanation="Raising is the highest EV play, maximizing value and applying pressure.")
        ],
        correct_action=GtoAction(action="Raise", ev=10.0, explanation="Raising is the highest EV play, maximizing value and applying pressure.")
    ),
    Scenario(
        id="2",
        category="cash_game",
        position="Big Blind",
        stack_size=100,
        hole_cards=["7h", "2d"],
        community_cards=[],
        street=Street.PRE_FLOP,
        gto_actions=[
            GtoAction(action="Fold", ev=0, explanation="Folding is the correct play with the worst hand in poker pre-flop."),
            GtoAction(action="Check", ev=-4.5, explanation="Checking is an option, but folding is better to avoid difficult post-flop spots.")
        ],
        correct_action=GtoAction(action="Fold", ev=0, explanation="Folding is the correct play with the worst hand in poker pre-flop.")
    )
]

@router.get("/practice/scenarios", response_model=List[Scenario])
def get_scenarios(category: str, street: Street = None):
    scenarios = [s for s in mock_scenarios if s.category == category]
    if street:
        scenarios = [s for s in scenarios if s.street == street]
    return scenarios

@router.post("/practice/attempt")
def post_attempt(attempt: Attempt):
    scenario = next((s for s in mock_scenarios if s.id == attempt.scenario_id), None)
    if not scenario:
        raise HTTPException(status_code=404, detail="Scenario not found")

    chosen_action = next((a for a in scenario.gto_actions if a.action == attempt.action), None)
    if not chosen_action:
        raise HTTPException(status_code=400, detail="Invalid action")

    is_correct = chosen_action.action == scenario.correct_action.action
    ev_difference = chosen_action.ev - scenario.correct_action.ev

    # Find an alternative line to suggest
    alternative_lines = [a for a in scenario.gto_actions if a.action != chosen_action.action]
    alternative_line = alternative_lines if alternative_lines else None


    return {
        "is_correct": is_correct,
        "chosen_action_ev": chosen_action.ev,
        "correct_action": scenario.correct_action,
        "ev_difference": ev_difference,
        "explanation": chosen_action.explanation or ("Correct!" if is_correct else "Incorrect."),
        "alternative_line": alternative_line
    }