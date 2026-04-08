from pydantic import BaseModel
from typing import List, Optional

class Email(BaseModel):
    id: str
    subject: str
    body: str

class Observation(BaseModel):
    email: Email
    conversation: List[str]
    status: str

class Action(BaseModel):
    action_type: str  # classify | ask | route | respond | escalate
    content: str

class Reward(BaseModel):
    score: float
    feedback: Optional[str] = None