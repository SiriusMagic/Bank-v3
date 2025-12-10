from fastapi import APIRouter, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from datetime import datetime, timezone, timedelta
import os
from models_goals import Goal, GoalCreate, GoalUpdate, Contribution, ContributionCreate
import random

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

@router.get("/goals")
async def get_goals():
    """Get all goals"""
    goals = await db.goals.find().to_list(1000)
    return serialize_doc(goals)

@router.get("/goals/{goal_id}")
async def get_goal(goal_id: str):
    """Get specific goal"""
    try:
        goal = await db.goals.find_one({"_id": ObjectId(goal_id)})
        if not goal:
            raise HTTPException(status_code=404, detail="Goal not found")
        return serialize_doc(goal)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/goals")
async def create_goal(goal: GoalCreate):
    """Create a new goal"""
    try:
        goal_dict = {
            "user_id": "default_user",
            "name": goal.name,
            "target_amount": goal.target_amount,
            "current_amount": 0.0,
            "icon": goal.icon,
            "category": goal.category,
            "created_at": datetime.now(timezone.utc),
            "target_date": datetime.fromisoformat(goal.target_date) if goal.target_date else None,
            "color": "#FFD700"
        }
        
        result = await db.goals.insert_one(goal_dict)
        goal_dict['id'] = str(result.inserted_id)
        return serialize_doc(goal_dict)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.patch("/goals/{goal_id}")
async def update_goal(goal_id: str, goal_update: GoalUpdate):
    """Update a goal"""
    try:
        update_data = {k: v for k, v in goal_update.model_dump().items() if v is not None}
        
        if 'target_date' in update_data and update_data['target_date']:
            update_data['target_date'] = datetime.fromisoformat(update_data['target_date'])
        
        result = await db.goals.update_one(
            {"_id": ObjectId(goal_id)},
            {"$set": update_data}
        )
        
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Goal not found")
        
        goal = await db.goals.find_one({"_id": ObjectId(goal_id)})
        return serialize_doc(goal)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/goals/{goal_id}")
async def delete_goal(goal_id: str):
    """Delete a goal"""
    try:
        result = await db.goals.delete_one({"_id": ObjectId(goal_id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Goal not found")
        
        # Also delete all contributions for this goal
        await db.contributions.delete_many({"goal_id": goal_id})
        
        return {"message": "Goal deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/goals/{goal_id}/contributions")
async def get_contributions(goal_id: str, days: int = 30):
    """Get contributions for a goal"""
    try:
        start_date = datetime.now(timezone.utc) - timedelta(days=days)
        
        contributions = await db.contributions.find({
            "goal_id": goal_id,
            "date": {"$gte": start_date}
        }).sort("date", -1).to_list(1000)
        
        return serialize_doc(contributions)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/goals/{goal_id}/contributions")
async def add_contribution(goal_id: str, contribution: ContributionCreate):
    """Add a contribution to a goal"""
    try:
        # Verify goal exists
        goal = await db.goals.find_one({"_id": ObjectId(goal_id)})
        if not goal:
            raise HTTPException(status_code=404, detail="Goal not found")
        
        # Create contribution
        contribution_dict = {
            "goal_id": goal_id,
            "amount": contribution.amount,
            "date": datetime.now(timezone.utc),
            "description": contribution.description,
            "type": contribution.type
        }
        
        result = await db.contributions.insert_one(contribution_dict)
        
        # Update goal current_amount
        if contribution.type == "deposit":
            new_amount = goal['current_amount'] + contribution.amount
        else:  # withdraw
            new_amount = max(0, goal['current_amount'] - contribution.amount)
        
        await db.goals.update_one(
            {"_id": ObjectId(goal_id)},
            {"$set": {"current_amount": new_amount}}
        )
        
        contribution_dict['id'] = str(result.inserted_id)
        return serialize_doc(contribution_dict)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/goals/{goal_id}/history")
async def get_goal_history(goal_id: str, days: int = 30):
    """Get cumulative history for goal progress chart"""
    try:
        start_date = datetime.now(timezone.utc) - timedelta(days=days)
        
        # Get all contributions
        contributions = await db.contributions.find({
            "goal_id": goal_id,
            "date": {"$gte": start_date}
        }).sort("date", 1).to_list(1000)
        
        # Build cumulative history
        history = []
        cumulative = 0
        
        # Group by day
        daily_data = {}
        for contrib in contributions:
            date_str = contrib['date'].strftime("%Y-%m-%d")
            if date_str not in daily_data:
                daily_data[date_str] = 0
            
            if contrib['type'] == 'deposit':
                daily_data[date_str] += contrib['amount']
            else:
                daily_data[date_str] -= contrib['amount']
        
        # Create cumulative series
        for i in range(days):
            date = start_date + timedelta(days=i)
            date_str = date.strftime("%Y-%m-%d")
            
            if date_str in daily_data:
                cumulative += daily_data[date_str]
            
            history.append({
                "date": date_str,
                "amount": cumulative
            })
        
        return history
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/dev/seed-goals")
async def seed_goals():
    """Seed database with sample goals"""
    try:
        # Clear existing goals and contributions
        await db.goals.delete_many({})
        await db.contributions.delete_many({})
        
        # Create sample goals
        goals_data = [
            {
                "user_id": "default_user",
                "name": "Tarjetas",
                "target_amount": 100.00,
                "current_amount": 0.00,
                "icon": "mountain",
                "category": "general",
                "created_at": datetime.now(timezone.utc),
                "target_date": None,
                "color": "#FFD700"
            },
            {
                "user_id": "default_user",
                "name": "Mi primer millón",
                "target_amount": 800.00,
                "current_amount": 1.57,
                "icon": "mountain",
                "category": "savings",
                "created_at": datetime.now(timezone.utc) - timedelta(days=15),
                "target_date": None,
                "color": "#FFD700"
            },
            {
                "user_id": "default_user",
                "name": "Vacaciones",
                "target_amount": 500.00,
                "current_amount": 150.00,
                "icon": "mountain",
                "category": "travel",
                "created_at": datetime.now(timezone.utc) - timedelta(days=30),
                "target_date": datetime.now(timezone.utc) + timedelta(days=90),
                "color": "#00CED1"
            }
        ]
        
        goal_ids = []
        for goal_data in goals_data:
            result = await db.goals.insert_one(goal_data)
            goal_ids.append(str(result.inserted_id))
        
        # Create sample contributions for goals with progress
        for i, goal_id in enumerate(goal_ids):
            if i > 0:  # Skip first goal (0 amount)
                num_contributions = random.randint(3, 8)
                for j in range(num_contributions):
                    days_ago = random.randint(0, 30)
                    contribution = {
                        "goal_id": goal_id,
                        "amount": round(random.uniform(5, 50), 2),
                        "date": datetime.now(timezone.utc) - timedelta(days=days_ago, hours=random.randint(0, 23)),
                        "description": f"Aporte #{j+1}",
                        "type": "deposit"
                    }
                    await db.contributions.insert_one(contribution)
        
        return {"message": "Goals seeded successfully", "goal_ids": goal_ids}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))