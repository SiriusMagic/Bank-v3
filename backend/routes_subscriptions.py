from fastapi import APIRouter, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from datetime import datetime, timezone, timedelta
import os
from models_subscriptions import Subscription, SubscriptionPlan, Loan, LoanRequest

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

# Subscription Plans Configuration
SUBSCRIPTION_PLANS = {
    "bronze": {
        "name": "Bronce",
        "level": "bronze",
        "monthly_fee": 9.99,
        "interest_rate": 3.5,
        "loan_limit": 150.0,
        "microcredit_only": True,
        "major_loans_limit": 0,
        "icon": "bronze",
        "color": "#CD7F32"
    },
    "silver": {
        "name": "Plata",
        "level": "silver",
        "monthly_fee": 19.99,
        "interest_rate": 2.0,
        "loan_limit": 500.0,
        "microcredit_only": True,
        "major_loans_limit": 0,
        "icon": "silver",
        "color": "#C0C0C0"
    },
    "gold": {
        "name": "Oro",
        "level": "gold",
        "monthly_fee": 49.99,
        "interest_rate": 1.5,
        "loan_limit": 2000.0,
        "microcredit_only": False,
        "major_loans_limit": 1,
        "icon": "gold",
        "color": "#FFD700"
    },
    "platinum": {
        "name": "Platino",
        "level": "platinum",
        "monthly_fee": 99.99,
        "interest_rate": 1.0,
        "loan_limit": 10000.0,
        "microcredit_only": False,
        "major_loans_limit": -1,  # Unlimited
        "icon": "platinum",
        "color": "#E5E4E2"
    }
}

@router.get("/subscription-plans")
async def get_subscription_plans():
    """Get all available subscription plans"""
    return list(SUBSCRIPTION_PLANS.values())

@router.get("/subscription")
async def get_user_subscription():
    """Get user's active subscription"""
    subscription = await db.subscriptions.find_one({"user_id": "default_user", "status": "active"})
    if not subscription:
        return None
    return serialize_doc(subscription)

@router.post("/subscription")
async def subscribe(plan_level: str):
    """Subscribe to a plan"""
    try:
        if plan_level not in SUBSCRIPTION_PLANS:
            raise HTTPException(status_code=400, detail="Invalid plan")
        
        # Cancel existing subscription
        await db.subscriptions.update_many(
            {"user_id": "default_user", "status": "active"},
            {"$set": {"status": "cancelled"}}
        )
        
        plan = SUBSCRIPTION_PLANS[plan_level]
        subscription = {
            "user_id": "default_user",
            "plan": plan_level,
            "monthly_fee": plan["monthly_fee"],
            "interest_rate": plan["interest_rate"],
            "loan_limit": plan["loan_limit"],
            "status": "active",
            "start_date": datetime.now(timezone.utc),
            "next_billing_date": datetime.now(timezone.utc) + timedelta(days=30)
        }
        
        result = await db.subscriptions.insert_one(subscription)
        subscription['id'] = str(result.inserted_id)
        return serialize_doc(subscription)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/loans")
async def request_loan(loan_request: LoanRequest):
    """Request a new loan"""
    try:
        # Get user's active subscription
        subscription = await db.subscriptions.find_one({"user_id": "default_user", "status": "active"})
        if not subscription:
            raise HTTPException(status_code=400, detail="No hay suscripción activa")
        
        subscription_id = str(subscription['_id'])
        plan = SUBSCRIPTION_PLANS.get(subscription['plan'])
        
        # Validate loan type
        if loan_request.loan_type == "microcredit":
            # Check microcredit limit
            if loan_request.amount > plan['loan_limit']:
                raise HTTPException(
                    status_code=400, 
                    detail=f"El monto excede el límite de tu plan ({plan['loan_limit']})"
                )
        elif loan_request.loan_type == "personal":
            # Check if plan allows major loans
            if plan['microcredit_only']:
                raise HTTPException(
                    status_code=400,
                    detail="Tu plan solo permite microcréditos. Actualiza a Oro o Platino."
                )
            # Check major loans limit
            active_major_loans = await db.loans.count_documents({
                "user_id": "default_user",
                "loan_type": {"$in": ["personal", "business"]},
                "status": {"$in": ["approved", "active"]}
            })
            if plan['major_loans_limit'] != -1 and active_major_loans >= plan['major_loans_limit']:
                raise HTTPException(
                    status_code=400,
                    detail=f"Has alcanzado el límite de préstamos mayores de tu plan"
                )
        elif loan_request.loan_type == "business":
            raise HTTPException(status_code=400, detail="Préstamos para negocios próximamente")
        
        # Calculate interest
        interest_amount = loan_request.amount * (plan['interest_rate'] / 100)
        total_amount = loan_request.amount + interest_amount
        
        # Create loan
        loan = {
            "user_id": "default_user",
            "subscription_id": subscription_id,
            "loan_type": loan_request.loan_type,
            "amount": loan_request.amount,
            "interest_rate": plan['interest_rate'],
            "total_amount": total_amount,
            "status": "approved" if loan_request.loan_type == "microcredit" else "pending",
            "created_at": datetime.now(timezone.utc),
            "due_date": datetime.now(timezone.utc) + timedelta(days=30),
            "paid_amount": 0.0,
            "remaining_amount": total_amount
        }
        
        if loan_request.cedula:
            loan['cedula'] = loan_request.cedula
        
        result = await db.loans.insert_one(loan)
        loan['id'] = str(result.inserted_id)
        return serialize_doc(loan)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/loans")
async def get_user_loans():
    """Get user's loans"""
    loans = await db.loans.find({"user_id": "default_user"}).sort("created_at", -1).to_list(100)
    return serialize_doc(loans)

@router.get("/loans/{loan_id}")
async def get_loan(loan_id: str):
    """Get specific loan"""
    try:
        loan = await db.loans.find_one({"_id": ObjectId(loan_id)})
        if not loan:
            raise HTTPException(status_code=404, detail="Préstamo no encontrado")
        return serialize_doc(loan)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/dev/seed-subscriptions")
async def seed_subscriptions():
    """Seed database with sample subscription"""
    try:
        # Clear existing subscriptions and loans
        await db.subscriptions.delete_many({})
        await db.loans.delete_many({})
        
        # Create a default bronze subscription
        plan = SUBSCRIPTION_PLANS["bronze"]
        subscription = {
            "user_id": "default_user",
            "plan": "bronze",
            "monthly_fee": plan["monthly_fee"],
            "interest_rate": plan["interest_rate"],
            "loan_limit": plan["loan_limit"],
            "status": "active",
            "start_date": datetime.now(timezone.utc),
            "next_billing_date": datetime.now(timezone.utc) + timedelta(days=30)
        }
        
        result = await db.subscriptions.insert_one(subscription)
        subscription_id = str(result.inserted_id)
        
        return {"message": "Subscription seeded successfully", "subscription_id": subscription_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))