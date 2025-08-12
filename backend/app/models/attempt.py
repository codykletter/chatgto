from pydantic import BaseModel

class Attempt(BaseModel):
    scenario_id: str
    action: str