from fastapi import APIRouter, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from datetime import datetime, timezone
import os
from models_missions import PointsBalance, PointsTransaction, Mission, RedeemRequest

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

# Mission definitions
MISSIONS_CONFIG = [
    {
        "id": "subscription_loyalty",
        "name": "Lealtad de Suscripción",
        "description": "Paga tu suscripción mensual",
        "points": 10,
        "mission_type": "active",
        "icon": "crown",
        "event": "subscription_paid"
    },
    {
        "id": "loan_repayment",
        "name": "Pago Puntual",
        "description": "Repaga tu préstamo a tiempo",
        "points": 50,
        "mission_type": "active",
        "icon": "check-circle",
        "event": "loan_repaid"
    },
    {
        "id": "card_purchases",
        "name": "Compras con Tarjeta",
        "description": "Realiza compras con tus tarjetas",
        "points": 2,
        "mission_type": "passive",
        "icon": "shopping-cart",
        "event": "card_purchase"
    },
    {
        "id": "bill_payments",
        "name": "Pago de Servicios",
        "description": "Paga servicios públicos",
        "points": 5,
        "mission_type": "passive",
        "icon": "file-text",
        "event": "bill_payment"
    }
]

REDEMPTION_OPTIONS = [
    {
        "id": "cash_1",
        "name": "$1.00 en Bóveda",
        "description": "Canjea 100 puntos por $1.00 depositado en tu bóveda",
        "points_cost": 100,
        "reward_amount": 1.0,
        "redeem_type": "cash",
        "icon": "dollar-sign"
    },
    {
        "id": "cash_2",
        "name": "$2.00 en Bóveda",
        "description": "Canjea 200 puntos por $2.00 depositado en tu bóveda",
        "points_cost": 200,
        "reward_amount": 2.0,
        "redeem_type": "cash",
        "icon": "dollar-sign"
    },
    {
        "id": "cash_10",
        "name": "$10.00 en Bóveda",
        "description": "Canjea 1000 puntos por $10.00 depositado en tu bóveda",
        "points_cost": 1000,
        "reward_amount": 10.0,
        "redeem_type": "cash",
        "icon": "dollar-sign"
    },
    {
        "id": "interest_discount",
        "name": "Descuento de Interés 0.5%",
        "description": "Reduce 0.5% la tasa de interés de tu próximo préstamo",
        "points_cost": 500,
        "reward_amount": 0.5,
        "redeem_type": "interest_discount",
        "icon": "percent"
    },
    {
        "id": "exclusive_benefits",
        "name": "Beneficios Exclusivos",
        "description": "Próximamente: meses gratis, upgrades temporales y más",
        "points_cost": 0,
        "reward_amount": 0,
        "redeem_type": "benefits",
        "icon": "gift",
        "coming_soon": True
    }
]

async def get_or_create_points_balance():
    """Get or create user's points balance"""
    balance = await db.points_balance.find_one({"user_id": "default_user"})
    if not balance:
        balance = {
            "user_id": "default_user",
            "total_points": 0,
            "lifetime_points": 0,
            "created_at": datetime.now(timezone.utc)
        }
        result = await db.points_balance.insert_one(balance)
        balance['_id'] = result.inserted_id
    return balance

async def award_points(event_type: str, points: int, description: str, related_id: str = None):
    """Award points to user for an event"""
    # Get or create balance
    balance = await get_or_create_points_balance()
    balance_id = balance['_id']
    
    # Update balance
    new_total = balance['total_points'] + points
    new_lifetime = balance['lifetime_points'] + points
    
    await db.points_balance.update_one(
        {"_id": balance_id},
        {"$set": {
            "total_points": new_total,
            "lifetime_points": new_lifetime
        }}
    )
    
    # Record transaction
    transaction = {
        "user_id": "default_user",
        "points": points,
        "transaction_type": "earn",
        "event_type": event_type,
        "description": description,
        "date": datetime.now(timezone.utc),
        "related_id": related_id
    }
    await db.points_transactions.insert_one(transaction)
    
    return new_total

@router.get("/missions/balance")
async def get_points_balance():
    """Get user's points balance"""
    balance = await get_or_create_points_balance()
    return serialize_doc(balance)

@router.get("/missions")
async def get_missions():
    """Get all missions"""
    return MISSIONS_CONFIG

@router.get("/missions/history")
async def get_points_history(limit: int = 20):
    """Get points transaction history"""
    try:
        transactions = await db.points_transactions.find(
            {"user_id": "default_user"}
        ).sort("date", -1).limit(limit).to_list(limit)
        return serialize_doc(transactions)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/missions/redemptions")
async def get_redemption_options():
    """Get available redemption options"""
    return REDEMPTION_OPTIONS

@router.post("/missions/redeem")
async def redeem_points(request: RedeemRequest):
    """Redeem points for rewards"""
    try:
        # Get balance
        balance = await get_or_create_points_balance()
        
        # Check sufficient points
        if balance['total_points'] < request.points_cost:
            raise HTTPException(status_code=400, detail="Puntos insuficientes")
        
        # Find redemption option
        option = next((opt for opt in REDEMPTION_OPTIONS if opt['points_cost'] == request.points_cost), None)
        if not option:
            raise HTTPException(status_code=400, detail="Opción de canje no válida")
        
        if option.get('coming_soon'):
            raise HTTPException(status_code=400, detail="Esta opción estará disponible próximamente")
        
        # Process redemption based on type
        if request.redeem_type == "cash":
            # Add money to vault
            vault = await db.vault.find_one({"user_id": "default_user"})
            if vault:
                new_balance = vault['balance'] + request.reward_amount
                await db.vault.update_one(
                    {"_id": vault['_id']},
                    {"$set": {"balance": new_balance}}
                )
                
                # Record vault transaction
                vault_transaction = {
                    "vault_id": str(vault['_id']),
                    "transaction_type": "deposit",
                    "amount": request.reward_amount,
                    "description": f"Canje de {request.points_cost} puntos",
                    "date": datetime.now(timezone.utc)
                }
                await db.vault_transactions.insert_one(vault_transaction)
        
        elif request.redeem_type == "interest_discount":
            # Store discount for next loan
            discount_record = {
                "user_id": "default_user",
                "discount_percent": request.reward_amount,
                "used": False,
                "created_at": datetime.now(timezone.utc)
            }
            await db.interest_discounts.insert_one(discount_record)
        
        # Deduct points
        new_total = balance['total_points'] - request.points_cost
        await db.points_balance.update_one(
            {"_id": balance['_id']},
            {"$set": {"total_points": new_total}}
        )
        
        # Record transaction
        transaction = {
            "user_id": "default_user",
            "points": -request.points_cost,
            "transaction_type": "redeem",
            "event_type": request.redeem_type,
            "description": option['name'],
            "date": datetime.now(timezone.utc)
        }
        await db.points_transactions.insert_one(transaction)
        
        return {
            "success": True,
            "new_balance": new_total,
            "reward": option['name']
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/missions/award/{event_type}")
async def manual_award_points(event_type: str, points: int, description: str):
    """Manually award points (for testing or admin)"""
    try:
        new_total = await award_points(event_type, points, description)
        return {"success": True, "new_balance": new_total}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/dev/seed-missions")
async def seed_missions():
    """Seed missions with initial points"""
    try:
        # Delete existing
        await db.points_balance.delete_many({"user_id": "default_user"})
        await db.points_transactions.delete_many({"user_id": "default_user"})
        
        # Create balance with some points
        balance = {
            "user_id": "default_user",
            "total_points": 250,
            "lifetime_points": 250,
            "created_at": datetime.now(timezone.utc)
        }
        result = await db.points_balance.insert_one(balance)
        
        # Add some sample transactions
        sample_transactions = [
            {
                "user_id": "default_user",
                "points": 10,
                "transaction_type": "earn",
                "event_type": "subscription_paid",
                "description": "Pago de suscripción mensual",
                "date": datetime.now(timezone.utc)
            },
            {
                "user_id": "default_user",
                "points": 50,
                "transaction_type": "earn",
                "event_type": "loan_repaid",
                "description": "Repago puntual de préstamo",
                "date": datetime.now(timezone.utc)
            },
            {
                "user_id": "default_user",
                "points": 2,
                "transaction_type": "earn",
                "event_type": "card_purchase",
                "description": "Compra con tarjeta",
                "date": datetime.now(timezone.utc)
            }
        ]
        
        for trans in sample_transactions:
            await db.points_transactions.insert_one(trans)
        
        return {"message": "Missions seeded successfully", "balance_id": str(result.inserted_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))