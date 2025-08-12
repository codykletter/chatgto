import os
import sys
from bson import ObjectId

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.models.scenario import Scenario, Street
from app.models.gto_action import GtoAction

def get_placeholder_scenarios():
    """
    Returns a list of placeholder scenarios for each street.
    """
    scenarios = [
        # Pre-flop Placeholder
        Scenario(
            id=str(ObjectId()),
            category="placeholder",
            position="UTG",
            stack_size=100,
            hole_cards=["Ah", "Kh"],
            community_cards=[],
            gto_actions=[
                GtoAction(action="Raise", ev=10.0, explanation="Placeholder explanation for raising."),
                GtoAction(action="Fold", ev=0.0, explanation="Placeholder explanation for folding.")
            ],
            correct_action=GtoAction(action="Raise", ev=10.0, explanation="Placeholder explanation for raising."),
            street=Street.PRE_FLOP,
        ),
        # Post-flop Placeholder
        Scenario(
            id=str(ObjectId()),
            category="placeholder",
            position="BB",
            stack_size=100,
            hole_cards=["Qh", "Qd"],
            community_cards=["Qc", "8h", "3s"],
            gto_actions=[
                GtoAction(action="Bet", ev=15.0, explanation="Placeholder explanation for betting."),
                GtoAction(action="Check", ev=5.0, explanation="Placeholder explanation for checking.")
            ],
            correct_action=GtoAction(action="Bet", ev=15.0, explanation="Placeholder explanation for betting."),
            street=Street.POST_FLOP,
        ),
        # Turn Placeholder
        Scenario(
            id=str(ObjectId()),
            category="placeholder",
            position="SB",
            stack_size=100,
            hole_cards=["Ts", "9s"],
            community_cards=["8s", "7s", "2h", "As"],
            gto_actions=[
                GtoAction(action="Bet", ev=25.0, explanation="Placeholder explanation for betting."),
                GtoAction(action="Check", ev=10.0, explanation="Placeholder explanation for checking.")
            ],
            correct_action=GtoAction(action="Bet", ev=25.0, explanation="Placeholder explanation for betting."),
            street=Street.TURN,
        ),
        # River Placeholder
        Scenario(
            id=str(ObjectId()),
            category="placeholder",
            position="Dealer",
            stack_size=100,
            hole_cards=["5c", "6c"],
            community_cards=["7c", "8c", "9c", "2h", "3d"],
            gto_actions=[
                GtoAction(action="Shove", ev=50.0, explanation="Placeholder explanation for shoving."),
                GtoAction(action="Check", ev=-10.0, explanation="Placeholder explanation for checking.")
            ],
            correct_action=GtoAction(action="Shove", ev=50.0, explanation="Placeholder explanation for shoving."),
            street=Street.RIVER,
        ),
    ]
    return scenarios

if __name__ == "__main__":
    # This script now only defines placeholder scenarios.
    # The database seeding logic has been removed as per the new requirements.
    # To use these scenarios, you can import the get_placeholder_scenarios function.
    placeholders = get_placeholder_scenarios()
    print(f"Defined {len(placeholders)} placeholder scenarios.")
    for scenario in placeholders:
        print(scenario.json(indent=2))