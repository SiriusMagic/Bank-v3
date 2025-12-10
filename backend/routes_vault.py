from fastapi import APIRouter, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from datetime import datetime, timezone
import os
from models_vault import Vault, TransferToCard, VaultTransaction

router = APIRouter()

mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

def serialize_doc(doc):
    """Convert MongoDB document to JSON-serializable format"""
    if doc is None:
        return None
    if isinstance(doc, list):
        return [serialize_doc(item) for item in doc]
    if isinstance(doc, dict):
        result = {}
        for key, value in doc.items():
            if key == '_id' and isinstance(value, ObjectId):
                result['id'] = str(value)
            elif isinstance(value, ObjectId):
                result[key] = str(value)
            elif isinstance(value, datetime):
                result[key] = value.isoformat()
            elif isinstance(value, dict):
                result[key] = serialize_doc(value)
            elif isinstance(value, list):
                result[key] = serialize_doc(value)
            else:
                result[key] = value
        return result
    return doc

@router.get("/vault")
async def get_vault():
    """Get user's vault"""
    vault = await db.vault.find_one({"user_id": "default_user"})
    if not vault:
        # Create default vault
        vault = {
            "user_id": "default_user",
            "name": "Mi Bóveda Segura",
            "balance": 10000.0,  # Initial balance
            "created_at": datetime.now(timezone.utc)
        }
        result = await db.vault.insert_one(vault)
        vault['_id'] = result.inserted_id
    return serialize_doc(vault)

@router.post("/vault/deposit")
async def deposit_to_vault(amount: float):
    """Deposit money to vault"""
    try:
        vault = await db.vault.find_one({"user_id": "default_user"})
        if not vault:
            raise HTTPException(status_code=404, detail="Bóveda no encontrada")
        
        vault_id = str(vault['_id'])
        new_balance = vault['balance'] + amount
        
        # Update vault balance
        await db.vault.update_one(
            {"_id": ObjectId(vault_id)},
            {"$set": {"balance": new_balance}}
        )
        
        # Record transaction
        transaction = {
            "vault_id": vault_id,
            "transaction_type": "deposit",
            "amount": amount,
            "description": "Depósito a bóveda",
            "date": datetime.now(timezone.utc)
        }
        await db.vault_transactions.insert_one(transaction)
        
        return {"success": True, "new_balance": new_balance}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/vault/transfer-to-card")
async def transfer_to_card(transfer: TransferToCard):
    """Transfer money from vault to card"""
    try:
        # Get vault
        vault = await db.vault.find_one({"user_id": "default_user"})
        if not vault:
            raise HTTPException(status_code=404, detail="Bóveda no encontrada")
        
        # Check sufficient balance
        if vault['balance'] < transfer.amount:
            raise HTTPException(status_code=400, detail="Saldo insuficiente en la bóveda")
        
        # Get card
        card = await db.cards.find_one({"_id": ObjectId(transfer.card_id)})
        if not card:
            raise HTTPException(status_code=404, detail="Tarjeta no encontrada")
        
        vault_id = str(vault['_id'])
        
        # Update vault balance
        new_vault_balance = vault['balance'] - transfer.amount
        await db.vault.update_one(
            {"_id": ObjectId(vault_id)},
            {"$set": {"balance": new_vault_balance}}
        )
        
        # Update card balance
        new_card_balance = card['balance'] + transfer.amount
        await db.cards.update_one(
            {"_id": ObjectId(transfer.card_id)},
            {"$set": {"balance": new_card_balance}}
        )
        
        # Record transaction
        transaction = {
            "vault_id": vault_id,
            "transaction_type": "transfer_to_card",
            "amount": transfer.amount,
            "card_id": transfer.card_id,
            "description": f"Transferencia a tarjeta ****{card['last4']}",
            "date": datetime.now(timezone.utc)
        }
        await db.vault_transactions.insert_one(transaction)
        
        return {
            "success": True,
            "vault_balance": new_vault_balance,
            "card_balance": new_card_balance
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/vault/transactions")
async def get_vault_transactions(limit: int = 10):
    """Get vault transaction history"""
    try:
        vault = await db.vault.find_one({"user_id": "default_user"})
        if not vault:
            return []
        
        vault_id = str(vault['_id'])
        transactions = await db.vault_transactions.find(
            {"vault_id": vault_id}
        ).sort("date", -1).limit(limit).to_list(limit)
        
        return serialize_doc(transactions)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/dev/seed-vault")
async def seed_vault():
    """Seed vault with initial balance"""
    try:
        # Delete existing vault
        await db.vault.delete_many({"user_id": "default_user"})
        await db.vault_transactions.delete_many({})
        
        # Create new vault
        vault = {
            "user_id": "default_user",
            "name": "Mi Bóveda Segura",
            "balance": 10000.0,
            "created_at": datetime.now(timezone.utc)
        }
        result = await db.vault.insert_one(vault)
        
        return {"message": "Vault seeded successfully", "vault_id": str(result.inserted_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))