from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class Goal(BaseModel):
    id: Optional[str] = None
    user_id: str = "default_user"
    name: str
    target_amount: float
    current_amount: float = 0.0
    icon: str = "mountain"
    category: str = "general"
    created_at: datetime = Field(default_factory=lambda: datetime.now())
    target_date: Optional[datetime] = None
    color: str = "#FFD700"

class GoalCreate(BaseModel):
    name: str
    target_amount: float
    target_date: Optional[str] = None
    category: str = "general"
    icon: str = "mountain"

class GoalUpdate(BaseModel):
    name: Optional[str] = None
    target_amount: Optional[float] = None
    target_date: Optional[str] = None

class Contribution(BaseModel):
    id: Optional[str] = None
    goal_id: str
    amount: float
    date: datetime = Field(default_factory=lambda: datetime.now())
    description: Optional[str] = None
    type: str = "deposit"  # deposit or withdraw

class ContributionCreate(BaseModel):
    amount: float
    description: Optional[str] = None
    type: str = "deposit"