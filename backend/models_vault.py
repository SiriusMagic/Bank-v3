from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class Vault(BaseModel):
    id: Optional[str] = None
    user_id: str = "default_user"
    name: str = "Mi Bóveda Segura"
    balance: float = 0.0
    created_at: datetime = Field(default_factory=lambda: datetime.now())

class TransferToCard(BaseModel):
    card_id: str
    amount: float

class VaultTransaction(BaseModel):
    id: Optional[str] = None
    vault_id: str
    transaction_type: str  # deposit, transfer_to_card, transfer_from_card
    amount: float
    card_id: Optional[str] = None
    description: str
    date: datetime = Field(default_factory=lambda: datetime.now())