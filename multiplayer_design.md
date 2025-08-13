# Multi-Player Scenario Design

This document outlines the data model and API changes required to support multi-player scenarios in the poker training application.

## 1. Updated Data Models

The following are the proposed changes to `backend/app/models/scenario.py`.

### `Opponent` Model

A new model to represent an opponent at the table.

```python
class Opponent(BaseModel):
    position: str
    hole_cards: List[str] # These will be hidden from the user in the API response
```

### Updated `Scenario` Model

The `Scenario` model will be updated to include a list of `Opponent` objects.

```python
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
    position: str # Hero's position
    stack_size: int
    hole_cards: List[str] # Hero's hole cards
    opponents: List[Opponent]
    gto_actions: List[GtoAction]
    correct_action: GtoAction
    stage: str
    flop: Optional[List[str]] = None
    turn: Optional[str] = None
    river: Optional[str] = None
```

## 2. API Response JSON Structure

To ensure opponents' cards are not exposed to the frontend, the API response will have a slightly different structure.

### API Response Models

These models define the structure of the data sent to the client.

```python
# Pydantic models for the API response

class OpponentResponse(BaseModel):
    position: str
    # hole_cards are intentionally omitted.

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
```

### Example JSON Response

This is an example of what the API endpoint (`/practice/scenario`) would return.

```json
{
  "id": "1",
  "category": "cash_game",
  "stage": "preflop",
  "hero": {
    "position": "Button",
    "hole_cards": ["As", "Ks"],
    "stack_size": 100
  },
  "opponents": [
    {
      "position": "SB"
    },
    {
      "position": "BB"
    }
  ],
  "gto_actions": [
    {
      "action": "Fold",
      "ev": -0.5,
      "explanation": "Folding is a significant EV loss with a premium hand like AKs."
    },
    {
      "action": "Call",
      "ev": 8.0,
      "explanation": "Calling is profitable, but raising is optimal to isolate and build a pot."
    },
    {
      "action": "Raise",
      "ev": 10.0,
      "explanation": "Raising is the highest EV play, maximizing value and applying pressure."
    }
  ],
  "flop": null,
  "turn": null,
  "river": null
}