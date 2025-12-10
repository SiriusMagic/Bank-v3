from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class Subscription(BaseModel):
    id: Optional[str] = None
    user_id: str = "default_user"
    plan: str  # bronze, silver, gold, platinum
    monthly_fee: float
    interest_rate: float  # Monthly interest rate
    loan_limit: float
    status: str = "active"  # active, cancelled
    start_date: datetime = Field(default_factory=lambda: datetime.now())
    next_billing_date: Optional[datetime] = None

class SubscriptionPlan(BaseModel):
    name: str
    level: str
    monthly_fee: float
    interest_rate: float
    loan_limit: float
    microcredit_only: bool
    major_loans_limit: int  # 0 for microcredit only, 1 for gold, unlimited (-1) for platinum
    icon: str
    color: str

class Loan(BaseModel):
    id: Optional[str] = None
    user_id: str = "default_user"
    subscription_id: str
    loan_type: str  # microcredit, personal, business
    amount: float
    interest_rate: float
    status: str = "pending"  # pending, approved, active, paid, rejected
    created_at: datetime = Field(default_factory=lambda: datetime.now())
    due_date: Optional[datetime] = None
    paid_amount: float = 0.0
    remaining_amount: float = 0.0

class LoanRequest(BaseModel):
    loan_type: str
    amount: float
    cedula: Optional[str] = None  # For personal loans