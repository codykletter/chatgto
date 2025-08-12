# Development Plan: Extending Poker Scenarios

This document outlines the plan to extend the poker training application to support preflop, flop, turn, and river scenarios.

## 1. High-Level Overview

The goal is to evolve the training tool from a single-stage scenario handler to a multi-stage game flow simulator. This requires changes in both the frontend and backend to manage game state, community cards, and stage-specific logic.

## 2. UI/Frontend Changes

### 2.1. Stage Selector

A dropdown menu will be added to the training interface to allow users to select the current game stage (Preflop, Flop, Turn, River). This component will control the game state on the frontend and fetch the appropriate scenario data from the backend.

**File:** `chatgto/frontend/src/app/training/page.tsx`

```typescript
// src/app/training/page.tsx

import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";

// ... existing component logic

const [stage, setStage] = useState('preflop');

// ...

<Select onValueChange={setStage} defaultValue={stage}>
  <SelectTrigger className="w-[180px]">
    <SelectValue placeholder="Select Stage" />
  </SelectTrigger>
  <SelectContent>
    <SelectItem value="preflop">Preflop</SelectItem>
    <SelectItem value="flop">Flop</SelectItem>
    <SelectItem value="turn">Turn</SelectItem>
    <SelectItem value="river">River</SelectItem>
  </SelectContent>
</Select>

// ... rest of the component```

### 2.2. Community Cards Display

The existing `CommunityCards` component will be used to display the flop, turn, and river cards. Its visibility and content will be tied to the selected game stage.

**File:** `chatgto/frontend/src/components/ui/community-cards.tsx`

```typescript
// src/components/ui/community-cards.tsx
// No changes needed if it already accepts an array of cards.
// The parent component will pass the correct cards based on the stage.

// Example usage in src/app/training/page.tsx
<CommunityCards cards={communityCards} />
```

## 3. Backend Changes

### 3.1. Data Model Updates

The `Scenario` model needs to be updated to include community cards and potentially stage-specific actions.

**File:** `chatgto/backend/app/models/scenario.py`

```python
# backend/app/models/scenario.py
from sqlmodel import SQLModel, Field
from typing import Optional, List

class Scenario(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    position: str
    stack_size: int
    hero_hand: str # e.g., "AsKd"
    villain_hand: Optional[str] = None
    
    # New fields for different stages
    flop: Optional[str] = None # e.g., "QcJsTh"
    turn: Optional[str] = None # e.g., "8s"
    river: Optional[str] = None # e.g., "2d"
    
    # To define which stage this scenario starts at
    stage: str = Field(default="preflop")
```

### 3.2. API Endpoint Updates

The practice/scenario fetching endpoint will need to accept a `stage` parameter to return relevant scenarios.

**File:** `chatgto/backend/app/api/v1/practice.py`

```python
# backend/app/api/v1/practice.py
from fastapi import APIRouter, Query
from typing import List
from app.models.scenario import Scenario

router = APIRouter()

@router.get("/scenarios", response_model=List[Scenario])
def get_scenarios_by_stage(stage: str = "preflop"):
    """
    Fetch scenarios for a specific game stage.
    This is a placeholder. The actual implementation will query the database.
    """
    # Database query logic will go here, e.g.:
    # return db.query(Scenario).filter(Scenario.stage == stage).all()
    
    # Placeholder data:
    if stage == "preflop":
        return [Scenario(id=1, name="UTG Open", position="UTG", stack_size=100, hero_hand="AKo", stage="preflop")]
    if stage == "flop":
        return [Scenario(id=2, name="Flop C-Bet", position="BTN", stack_size=100, hero_hand="QhQd", flop="JcTs2d", stage="flop")]
    # ... etc. for turn and river
    return []

```

## 4. Game Stage Implementation

### 4.1. Preflop

This is the initial state. The logic will likely be similar to the current implementation, focusing on hole cards and positions.

- **Infrastructure:** No new infrastructure needed. Uses existing components.
- **Code Changes:** The frontend will fetch `preflop` scenarios. The backend will serve them.
- **Placeholder Scenario:**
  - **Name:** Button vs. Big Blind
  - **Position:** BTN
  - **Stack:** 100bb
  - **Hand:** AJo
  - **Action:** Raise 2.5bb
- **Function Stubs:**
  - **Backend (`practice.py`):** `get_scenarios_by_stage(stage="preflop")`
  - **Frontend (`training/page.tsx`):**
    ```typescript
    const fetchPreflopScenario = async () => {
      const response = await fetch('/api/v1/scenarios?stage=preflop');
      const data = await response.json();
      // set scenario state
    };
    ```

### 4.2. Flop

This stage introduces the first three community cards.

- **Infrastructure:** The `CommunityCards` component will be used. The `Scenario` model is updated.
- **Code Changes:**
  - Frontend fetches `flop` scenarios and displays the 3 flop cards.
  - Backend serves scenarios that include a `flop` field.
- **Placeholder Scenario:**
  - **Name:** C-Bet Opportunity
  - **Position:** CO
  - **Stack:** 100bb
  - **Hand:** KQs
  - **Flop:** Qs Td 5h
  - **Action:** Bet 1/3 pot
- **Function Stubs:**
  - **Backend (`practice.py`):** `get_scenarios_by_stage(stage="flop")`
  - **Frontend (`training/page.tsx`):**
    ```typescript
    const fetchFlopScenario = async () => {
      const response = await fetch('/api/v1/scenarios?stage=flop');
      const data = await response.json();
      setCommunityCards(data.flop.match(/.{1,2}/g)); // e.g., ["Qs", "Td", "5h"]
      // set other scenario state
    };
    ```

### 4.3. Turn

This stage adds the fourth community card.

- **Infrastructure:** No new infrastructure.
- **Code Changes:**
  - Frontend displays the 3 flop cards + 1 turn card.
  - Backend serves scenarios with `flop` and `turn` fields.
- **Placeholder Scenario:**
  - **Name:** Turn Barrel
  - **Position:** MP
  - **Stack:** 100bb
  - **Hand:** 88
  - **Flop:** 7h 6s 2d
  - **Turn:** 9c
  - **Action:** Check/Call
- **Function Stubs:**
  - **Backend (`practice.py`):** `get_scenarios_by_stage(stage="turn")`
  - **Frontend (`training/page.tsx`):**
    ```typescript
    const fetchTurnScenario = async () => {
      const response = await fetch('/api/v1/scenarios?stage=turn');
      const data = await response.json();
      const flopCards = data.flop.match(/.{1,2}/g);
      const turnCard = data.turn;
      setCommunityCards([...flopCards, turnCard]);
      // set other scenario state
    };
    ```

### 4.4. River

This stage adds the final community card.

- **Infrastructure:** No new infrastructure.
- **Code Changes:**
  - Frontend displays all 5 community cards.
  - Backend serves scenarios with `flop`, `turn`, and `river` fields.
- **Placeholder Scenario:**
  - **Name:** River Value Bet
  - **Position:** BB
  - **Stack:** 100bb
  - **Hand:** A5s
  - **Flop:** Ah 9s 5d
  - **Turn:** 2c
  - **River:** 3h
  - **Action:** Bet 3/4 pot
- **Function Stubs:**
  - **Backend (`practice.py`):** `get_scenarios_by_stage(stage="river")`
  - **Frontend (`training/page.tsx`):**
    ```typescript
    const fetchRiverScenario = async () => {
      const response = await fetch('/api/v1/scenarios?stage=river');
      const data = await response.json();
      const flopCards = data.flop.match(/.{1,2}/g);
      const turnCard = data.turn;
      const riverCard = data.river;
      setCommunityCards([...flopCards, turnCard, riverCard]);
      // set other scenario state
    };