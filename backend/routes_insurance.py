from fastapi import APIRouter, HTTPException, UploadFile, File
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from datetime import datetime, timezone, timedelta
import os
from models_insurance import InsurancePolicy, InsurancePlan, InsuranceClaim, ClaimRequest
from typing import List

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

# Insurance Plans Configuration
INSURANCE_PLANS = [
    {
        "id": "vault_protection",
        "name": "Plan Único: Protección de Bóveda",
        "plan_type": "vault_protection",
        "monthly_fee": 15.99,
        "coverage_normal": 100,
        "coverage_negligent": 75,
        "description": "Protección de Capital 100% Garantizada, incluso contra Errores Propios",
        "features": [
            "Cobertura del 100% si no hay negligencia",
            "Cobertura del 75% en caso de negligencia/estafa",
            "Investigación activa por Feruner Seguros",
            "Proceso de reclamo con soporte de evidencia",
            "Reembolso directo a tu bóveda"
        ],
        "icon": "shield",
        "featured": True
    },
    {
        "id": "basic_card",
        "name": "Seguro Básico de Tarjetas",
        "plan_type": "basic_card",
        "monthly_fee": 5.99,
        "coverage_normal": 100,
        "coverage_negligent": 0,
        "description": "Protección básica para tus tarjetas contra fraudes",
        "features": [
            "Cobertura del 100% por fraude comprobado",
            "Solo transacciones no autorizadas",
            "Proceso de reclamo estándar"
        ],
        "icon": "credit-card",
        "featured": False
    },
    {
        "id": "premium_card",
        "name": "Seguro Premium de Tarjetas",
        "plan_type": "premium_card",
        "monthly_fee": 9.99,
        "coverage_normal": 100,
        "coverage_negligent": 50,
        "description": "Protección completa para todas tus tarjetas",
        "features": [
            "Cobertura del 100% por fraude comprobado",
            "Cobertura del 50% en caso de negligencia",
            "Asistencia 24/7",
            "Reemplazo express de tarjetas"
        ],
        "icon": "credit-card",
        "featured": False
    }
]

@router.get("/insurance")
async def get_insurance_status():
    """Get user's insurance status"""
    policy = await db.insurance_policies.find_one({"user_id": "default_user", "status": "active"})
    
    if policy:
        return {
            "has_insurance": True,
            "plan_name": policy.get("plan_name", "Plan Único"),
            "plan_type": policy.get("plan_type"),
            "monthly_fee": policy.get("monthly_fee"),
            "status": "active"
        }
    else:
        return {
            "has_insurance": False,
            "plan_name": None,
            "plan_type": None,
            "monthly_fee": None,
            "status": "none"
        }

@router.post("/insurance/activate")
async def activate_insurance(request: dict):
    """Activate insurance plan"""
    try:
        plan_type = request.get("plan_type", "vault_protection")
        plan = next((p for p in INSURANCE_PLANS if p['plan_type'] == plan_type), None)
        
        if not plan:
            raise HTTPException(status_code=400, detail="Plan no encontrado")
        
        # Cancel existing policies
        await db.insurance_policies.update_many(
            {"user_id": "default_user", "status": "active"},
            {"$set": {"status": "cancelled"}}
        )
        
        # Create new policy
        policy = {
            "user_id": "default_user",
            "plan_type": plan['plan_type'],
            "plan_name": plan['name'],
            "monthly_fee": plan['monthly_fee'],
            "coverage_percentage_normal": plan['coverage_normal'],
            "coverage_percentage_negligent": plan['coverage_negligent'],
            "status": "active",
            "start_date": datetime.now(timezone.utc),
            "next_billing_date": datetime.now(timezone.utc) + timedelta(days=30)
        }
        
        result = await db.insurance_policies.insert_one(policy)
        return {"message": "Plan activado exitosamente", "policy_id": str(result.inserted_id)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/insurance/claim")
async def file_insurance_claim(
    amount: float,
    description: str,
    incident_type: str
):
    """File an insurance claim with evidence"""
    try:
        # Get active policy
        policy = await db.insurance_policies.find_one({"user_id": "default_user", "status": "active"})
        if not policy:
            raise HTTPException(status_code=400, detail="No tienes un plan activo")
        
        # Create claim
        claim_doc = {
            "user_id": "default_user",
            "policy_id": str(policy["_id"]),
            "incident_type": incident_type,
            "amount": amount,
            "description": description,
            "status": "pending",
            "evidence_count": 0,  # Would be updated with actual file uploads
            "created_at": datetime.now(timezone.utc)
        }
        
        result = await db.insurance_claims.insert_one(claim_doc)
        
        return {
            "message": "Reclamo enviado exitosamente",
            "claim_id": str(result.inserted_id),
            "status": "pending"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/dev/seed-insurance")
async def seed_insurance():
    """Seed insurance with default data"""
    try:
        # Clear existing
        await db.insurance_policies.delete_many({"user_id": "default_user"})
        await db.insurance_claims.delete_many({"user_id": "default_user"})
        
        return {"message": "Insurance seeded successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))