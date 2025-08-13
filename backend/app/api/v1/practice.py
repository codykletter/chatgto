from fastapi import APIRouter, HTTPException
from typing import List
from pydantic import BaseModel
from app.models.attempt import Attempt
from app.models.scenario import Scenario, Opponent
from app.models.gto_action import GtoAction
from typing import Optional

router = APIRouter()

# --- API Response Models ---
class OpponentResponse(BaseModel):
    position: str

class Hero(BaseModel):
    position: str
    hole_cards: List[str]
    stack_size: int

class ScenarioResponse(BaseModel):
    id: str
    category: str
    stage: str
    hero: Hero
    opponents: List[OpponentResponse]
    gto_actions: List[GtoAction]
    flop: Optional[List[str]] = None
    turn: Optional[str] = None
    river: Optional[str] = None


mock_scenarios = {
    "preflop": Scenario(
        id="1",
        category="cash_game",
        position="Button",
        stack_size=100,
        hole_cards=["As", "Ks"],
        opponents=[
            Opponent(position="SB", hole_cards=["2c", "7d"]),
            Opponent(position="BB", hole_cards=["8h", "9h"]),
        ],
        gto_actions=[
            GtoAction(action="Fold", ev=-0.5, explanation="Folding is a significant EV loss with a premium hand like AKs."),
            GtoAction(action="Call", ev=8.0, explanation="Calling is profitable, but raising is optimal to isolate and build a pot."),
            GtoAction(action="Raise", ev=10.0, explanation="Raising is the highest EV play, maximizing value and applying pressure.")
        ],
        correct_action=GtoAction(action="Raise", ev=10.0, explanation="Raising is the highest EV play, maximizing value and applying pressure."),
        stage="preflop"
    ),
    "flop": Scenario(
        id="2",
        category="cash_game",
        position="Button",
        stack_size=100,
        hole_cards=["As", "Ks"],
        opponents=[
            Opponent(position="BB", hole_cards=["8h", "9h"]),
        ],
        flop=["Ah", "Kd", "5c"],
        gto_actions=[
            GtoAction(action="Check", ev=2.0, explanation="Checking is a reasonable option to control the pot size."),
            GtoAction(action="Bet", ev=15.0, explanation="Betting for value is the best play with top two pair.")
        ],
        correct_action=GtoAction(action="Bet", ev=15.0, explanation="Betting for value is the best play with top two pair."),
        stage="flop"
    ),
    "turn": Scenario(
        id="3",
        category="cash_game",
        position="Button",
        stack_size=100,
        hole_cards=["As", "Ks"],
        opponents=[
            Opponent(position="BB", hole_cards=["8h", "9h"]),
        ],
        flop=["Ah", "Kd", "5c"],
        turn="7h",
        gto_actions=[
            GtoAction(action="Check", ev=5.0, explanation="Checking can be a valid option, but betting is stronger."),
            GtoAction(action="Bet", ev=20.0, explanation="Continuing to bet for value is the optimal play.")
        ],
        correct_action=GtoAction(action="Bet", ev=20.0, explanation="Continuing to bet for value is the optimal play."),
        stage="turn"
    ),
    "river": Scenario(
        id="4",
        category="cash_game",
        position="Button",
        stack_size=100,
        hole_cards=["As", "Ks"],
        opponents=[
            Opponent(position="BB", hole_cards=["8h", "9h"]),
        ],
        flop=["Ah", "Kd", "5c"],
        turn="7h",
        river="2s",
        gto_actions=[
            GtoAction(action="Check", ev=8.0, explanation="Checking is a safe play, but you might miss out on value."),
            GtoAction(action="Bet", ev=25.0, explanation="A value bet is warranted on this dry river.")
        ],
        correct_action=GtoAction(action="Bet", ev=25.0, explanation="A value bet is warranted on this dry river."),
        stage="river"
    ),
}

@router.get("/practice/scenario", response_model=ScenarioResponse)
def get_practice_scenario(stage: str = "preflop"):
    scenario = mock_scenarios.get(stage)
    if not scenario:
        raise HTTPException(status_code=404, detail="Scenario not found for this stage")

    hero = Hero(
        position=scenario.position,
        hole_cards=scenario.hole_cards,
        stack_size=scenario.stack_size
    )

    opponent_responses = [OpponentResponse(position=opp.position) for opp in scenario.opponents]

    return ScenarioResponse(
        id=scenario.id,
        category=scenario.category,
        stage=scenario.stage,
        hero=hero,
        opponents=opponent_responses,
        gto_actions=scenario.gto_actions,
        flop=scenario.flop,
        turn=scenario.turn,
        river=scenario.river,
    )

@router.post("/practice/attempt")
def post_attempt(attempt: Attempt):
    scenario = next((s for s in mock_scenarios.values() if s.id == attempt.scenario_id), None)
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