from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class InsurancePolicy(BaseModel):
    id: Optional[str] = None
    user_id: str = "default_user"
    plan_type: str  # vault_protection, basic_card, premium_card
    plan_name: str
    monthly_fee: float
    coverage_percentage_normal: int  # 100% for non-negligent
    coverage_percentage_negligent: int  # 75% for negligent
    status: str = "active"  # active, cancelled
    start_date: datetime = Field(default_factory=lambda: datetime.now())
    next_billing_date: Optional[datetime] = None

class InsurancePlan(BaseModel):
    id: str
    name: str
    plan_type: str
    monthly_fee: float
    coverage_normal: int
    coverage_negligent: int
    description: str
    features: List[str]
    icon: str

class InsuranceClaim(BaseModel):
    id: Optional[str] = None
    user_id: str = "default_user"
    policy_id: str
    claim_type: str  # fraud, error, negligent
    amount_lost: float
    description: str
    status: str = "pending"  # pending, investigating, approved, rejected
    evidence_files: List[str] = []
    created_at: datetime = Field(default_factory=lambda: datetime.now())
    resolved_at: Optional[datetime] = None
    reimbursement_amount: Optional[float] = None

class ClaimRequest(BaseModel):
    policy_id: str
    claim_type: str
    amount_lost: float
    description: str
    is_negligent: bool = False