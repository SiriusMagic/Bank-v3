from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class PointsBalance(BaseModel):
    id: Optional[str] = None
    user_id: str = "default_user"
    total_points: int = 0
    lifetime_points: int = 0
    created_at: datetime = Field(default_factory=lambda: datetime.now())

class PointsTransaction(BaseModel):
    id: Optional[str] = None
    user_id: str = "default_user"
    points: int
    transaction_type: str  # earn, redeem
    event_type: str  # subscription_paid, loan_repaid, card_purchase, bill_payment, redeem_cash, etc
    description: str
    date: datetime = Field(default_factory=lambda: datetime.now())
    related_id: Optional[str] = None

class Mission(BaseModel):
    id: str
    name: str
    description: str
    points: int
    mission_type: str  # active, passive
    icon: str
    progress: int = 0
    goal: int = 1
    completed: bool = False

class RedeemRequest(BaseModel):
    redeem_type: str  # cash, interest_discount, benefits
    points_cost: int
    reward_amount: Optional[float] = None