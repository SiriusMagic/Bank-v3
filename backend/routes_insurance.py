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

@router.get("/insurance/plans")
async def get_insurance_plans():
    """Get all insurance plans"""
    return INSURANCE_PLANS

@router.get("/insurance/policy")
async def get_user_policy():
    """Get user's active insurance policy"""
    policy = await db.insurance_policies.find_one({"user_id": "default_user", "status": "active"})
    if not policy:
        return None
    return serialize_doc(policy)

@router.post("/insurance/subscribe")
async def subscribe_insurance(plan_id: str):
    """Subscribe to an insurance plan"""
    try:
        # Find plan
        plan = next((p for p in INSURANCE_PLANS if p['id'] == plan_id), None)
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
        policy['id'] = str(result.inserted_id)
        return serialize_doc(policy)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/insurance/claims")
async def file_claim(claim: ClaimRequest):
    """File an insurance claim"""
    try:
        # Get policy
        policy = await db.insurance_policies.find_one({"_id": ObjectId(claim.policy_id)})
        if not policy:
            raise HTTPException(status_code=404, detail="Póliza no encontrada")
        
        if policy['status'] != 'active':
            raise HTTPException(status_code=400, detail="Póliza no activa")
        
        # Calculate reimbursement
        coverage_percent = policy['coverage_percentage_negligent'] if claim.is_negligent else policy['coverage_percentage_normal']
        reimbursement = claim.amount_lost * (coverage_percent / 100)
        
        # Create claim
        claim_doc = {
            "user_id": "default_user",
            "policy_id": claim.policy_id,
            "claim_type": claim.claim_type,
            "amount_lost": claim.amount_lost,
            "description": claim.description,
            "status": "pending",
            "is_negligent": claim.is_negligent,
            "coverage_percent": coverage_percent,
            "expected_reimbursement": reimbursement,
            "evidence_files": [],
            "created_at": datetime.now(timezone.utc)
        }
        
        result = await db.insurance_claims.insert_one(claim_doc)
        claim_doc['id'] = str(result.inserted_id)
        
        return serialize_doc(claim_doc)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/insurance/claims")
async def get_user_claims():
    """Get user's insurance claims"""
    claims = await db.insurance_claims.find({"user_id": "default_user"}).sort("created_at", -1).to_list(100)
    return serialize_doc(claims)

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