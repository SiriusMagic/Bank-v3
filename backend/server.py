from fastapi import FastAPI, APIRouter, HTTPException
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime, timezone, timedelta
from bson import ObjectId
import random

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app without a prefix
app = FastAPI()

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Helper function to serialize MongoDB documents
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

# Models
class Card(BaseModel):
    id: Optional[str] = None
    type: str  # debit, credit, virtual
    holder_name: str
    brand: str = "VISA"
    balance: float
    frozen: bool = False
    last4: str
    exp_month: str
    exp_year: str
    color_theme: str
    cashback: float = 0.0

class Transaction(BaseModel):
    id: Optional[str] = None
    card_id: str
    date: datetime
    amount: float
    category: str
    description: str

class Document(BaseModel):
    id: Optional[str] = None
    card_id: str
    name: str
    url: str

class FreezeRequest(BaseModel):
    frozen: bool


class CreateDisposableCardRequest(BaseModel):
    brand: str  # VISA or Mastercard
    amount: float
    holder_name: str
    exp_month: str
    exp_year: str

class MoneyTransferRequest(BaseModel):
    amount: float

# Routes
@api_router.get("/")
async def root():
    return {"message": "Aira Card Management API"}

@api_router.get("/cards")
async def get_cards():
    """Get all cards"""
    cards = await db.cards.find().to_list(1000)
    return serialize_doc(cards)

@api_router.get("/cards/destroyed-history")
async def get_destroyed_history():
    """Get history of destroyed disposable cards"""
    try:
        history = await db.destroyed_cards.find().sort("destroyed_at", -1).to_list(100)
        return serialize_doc(history)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@api_router.get("/cards/{card_id}")
async def get_card(card_id: str):
    """Get specific card details"""
    try:
        card = await db.cards.find_one({"_id": ObjectId(card_id)})
        if not card:
            raise HTTPException(status_code=404, detail="Card not found")
        return serialize_doc(card)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@api_router.get("/cards/{card_id}/transactions")
async def get_transactions(card_id: str, range: str = "semana"):
    """Get transactions for a card filtered by range"""
    try:
        # Calculate date range
        now = datetime.now(timezone.utc)
        if range == "hoy":
            start_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
        elif range == "semana":
            start_date = now - timedelta(days=7)
        else:  # personaliza or default
            start_date = now - timedelta(days=30)
        
        transactions = await db.transactions.find({
            "card_id": card_id,
            "date": {"$gte": start_date}
        }).sort("date", -1).to_list(1000)
        
        return serialize_doc(transactions)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@api_router.get("/cards/{card_id}/documents")
async def get_documents(card_id: str):
    """Get documents for a card"""
    try:
        documents = await db.documents.find({"card_id": card_id}).to_list(1000)
        return serialize_doc(documents)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@api_router.patch("/cards/{card_id}/freeze")
async def freeze_card(card_id: str, request: FreezeRequest):
    """Freeze or unfreeze a card"""
    try:
        result = await db.cards.update_one(
            {"_id": ObjectId(card_id)},
            {"$set": {"frozen": request.frozen}}
        )
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Card not found")
        
        card = await db.cards.find_one({"_id": ObjectId(card_id)})
        return serialize_doc(card)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@api_router.get("/cards/{card_id}/history")
async def get_history(card_id: str, range_type: str = "semana"):
    """Get historical spending data for charts"""
    try:
        # Calculate date range
        now = datetime.now(timezone.utc)
        if range_type == "hoy":
            start_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
            days = 1
        elif range_type == "semana":
            start_date = now - timedelta(days=7)
            days = 7
        else:  # personaliza
            start_date = now - timedelta(days=30)
            days = 30
        
        # Get transactions for the period
        transactions = await db.transactions.find({
            "card_id": card_id,
            "date": {"$gte": start_date}
        }).sort("date", 1).to_list(1000)
        
        # Group by day and sum amounts
        daily_data = {}
        for i in range(days):
            date = start_date + timedelta(days=i)
            date_str = date.strftime("%Y-%m-%d")
            daily_data[date_str] = 0
        
        for trans in transactions:
            date_str = trans["date"].strftime("%Y-%m-%d")
            if date_str in daily_data:
                daily_data[date_str] += abs(trans["amount"])
        
        # Convert to list format for chart
        history = [{"date": date, "amount": amount} for date, amount in sorted(daily_data.items())]
        return history
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))



@api_router.get("/cards/destroyed-history")
async def get_destroyed_history():
    """Get history of destroyed disposable cards"""
    try:
        history = await db.destroyed_cards.find().sort("destroyed_at", -1).to_list(100)
        return serialize_doc(history)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@api_router.post("/cards/create-disposable")
async def create_disposable_card(request: CreateDisposableCardRequest):
    """Create a new disposable debit card"""
    try:
        # Check vault balance
        vault = await db.vault.find_one({})
        if not vault or vault.get("balance", 0) < request.amount:
            raise HTTPException(status_code=400, detail="Fondos insuficientes en la Bóveda")
        
        # Create new card
        new_card = {
            "type": "disposable",
            "holder_name": request.holder_name or "USUARIO AIRA",
            "brand": request.brand,
            "balance": request.amount,
            "initial_amount": request.amount,
            "frozen": False,
            "last4": str(random.randint(1000, 9999)),
            "exp_month": request.exp_month,
            "exp_year": request.exp_year,
            "color_theme": "purple" if request.brand == "Mastercard" else "orange",
            "cashback": 0.0,
            "created_at": datetime.now(timezone.utc)
        }
        
        result = await db.cards.insert_one(new_card)
        new_card["_id"] = result.inserted_id
        
        # Deduct from vault
        await db.vault.update_one(
            {"_id": vault["_id"]},
            {"$inc": {"balance": -request.amount}}
        )
        
        return serialize_doc(new_card)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@api_router.post("/cards/{card_id}/return-funds")
async def return_funds(card_id: str):
    """Return funds from card to vault"""
    try:
        card = await db.cards.find_one({"_id": ObjectId(card_id)})
        if not card:
            raise HTTPException(status_code=404, detail="Card not found")
        
        amount = card.get("balance", 0)
        if amount <= 0:
            raise HTTPException(status_code=400, detail="No funds to return")
        
        # Update card balance
        await db.cards.update_one(
            {"_id": ObjectId(card_id)},
            {"$set": {"balance": 0.0}}
        )
        
        # Update vault (assuming there's a vault collection)
        vault = await db.vault.find_one({})
        if vault:
            await db.vault.update_one(
                {"_id": vault["_id"]},
                {"$inc": {"balance": amount}}
            )
        
        return {"success": True, "amount_returned": amount}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@api_router.delete("/cards/{card_id}/destroy")
async def destroy_card(card_id: str):
    """Destroy a disposable card and return funds to vault"""
    try:
        card = await db.cards.find_one({"_id": ObjectId(card_id)})
        if not card:
            raise HTTPException(status_code=404, detail="Card not found")
        
        # Only disposable cards can be destroyed
        if card.get("type") not in ["disposable", "virtual"]:
            raise HTTPException(status_code=400, detail="Only disposable cards can be destroyed")
        
        amount = card.get("balance", 0)
        
        # Return funds to vault if any
        if amount > 0:
            vault = await db.vault.find_one({})
            if vault:
                await db.vault.update_one(
                    {"_id": vault["_id"]},
                    {"$inc": {"balance": amount}}
                )
        
        # Save to history
        history_record = {
            "card_id": str(card["_id"]),
            "holder_name": card.get("holder_name"),
            "brand": card.get("brand"),
            "last4": card.get("last4"),
            "initial_amount": card.get("initial_amount", 0),
            "returned_amount": amount,
            "destruction_reason": "Manual",
            "destroyed_at": datetime.now(timezone.utc)
        }
        await db.destroyed_cards.insert_one(history_record)
        
        # Delete the card
        await db.cards.delete_one({"_id": ObjectId(card_id)})
        
        return {"success": True, "amount_returned": amount}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@api_router.post("/cards/{card_id}/send")
async def send_money_from_card(card_id: str, request: MoneyTransferRequest):
    """Send money from card"""
    try:
        card = await db.cards.find_one({"_id": ObjectId(card_id)})
        if not card:
            raise HTTPException(status_code=404, detail="Card not found")
        
        if card.get("balance", 0) < request.amount:
            raise HTTPException(status_code=400, detail="Insufficient balance")
        
        await db.cards.update_one(
            {"_id": ObjectId(card_id)},
            {"$inc": {"balance": -request.amount}}
        )
        
        return {"success": True, "amount_sent": request.amount}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@api_router.post("/cards/{card_id}/receive")
async def receive_money_to_card(card_id: str, request: MoneyTransferRequest):
    """Receive money to card"""
    try:
        card = await db.cards.find_one({"_id": ObjectId(card_id)})
        if not card:
            raise HTTPException(status_code=404, detail="Card not found")
        
        await db.cards.update_one(
            {"_id": ObjectId(card_id)},
            {"$inc": {"balance": request.amount}}
        )
        
        return {"success": True, "amount_received": request.amount}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@api_router.post("/dev/seed")
async def seed_data():
    """Seed the database with sample data"""
    try:
        # Clear existing data
        await db.cards.delete_many({})
        await db.transactions.delete_many({})
        await db.documents.delete_many({})
        
        # Create cards
        cards_data = [
            {
                "type": "debit",
                "holder_name": "JACK NOLAN",
                "brand": "VISA",
                "balance": 66603.00,
                "frozen": False,
                "last4": "4532",
                "exp_month": "12",
                "exp_year": "2027",
                "color_theme": "turquoise",
                "cashback": 125.50
            },
            {
                "type": "credit",
                "holder_name": "JACK NOLAN",
                "brand": "VISA",
                "balance": 2500.50,
                "frozen": False,
                "last4": "8921",
                "exp_month": "06",
                "exp_year": "2026",
                "color_theme": "blue",
                "cashback": 45.25
            },
            {
                "type": "virtual",
                "holder_name": "JACK NOLAN",
                "brand": "VISA",
                "balance": 80.00,
                "frozen": False,
                "last4": "1234",
                "exp_month": "03",
                "exp_year": "2025",
                "color_theme": "green",
                "cashback": 2.10
            }
        ]
        
        card_ids = []
        for card_data in cards_data:
            result = await db.cards.insert_one(card_data)
            card_ids.append(str(result.inserted_id))
        
        # Create transactions for each card
        categories = ["Alimentación", "Transporte", "Entretenimiento", "Compras", "Servicios", "Salud"]
        descriptions = [
            "Supermercado", "Gasolina", "Cine", "Tienda online", "Netflix", "Farmacia",
            "Restaurante", "Uber", "Spotify", "Amazon", "Electricidad", "Gimnasio"
        ]
        
        for card_id in card_ids:
            # Create 20-30 transactions per card
            num_transactions = random.randint(20, 30)
            for i in range(num_transactions):
                days_ago = random.randint(0, 30)
                transaction = {
                    "card_id": card_id,
                    "date": datetime.now(timezone.utc) - timedelta(days=days_ago, hours=random.randint(0, 23)),
                    "amount": -round(random.uniform(5, 500), 2),
                    "category": random.choice(categories),
                    "description": random.choice(descriptions)
                }
                await db.transactions.insert_one(transaction)
        
        # Create documents for each card
        document_types = ["Estado de cuenta", "Contrato", "Términos y condiciones", "Seguro de tarjeta"]
        for card_id in card_ids:
            for doc_type in document_types:
                document = {
                    "card_id": card_id,
                    "name": doc_type,
                    "url": f"/documents/{card_id}/{doc_type.replace(' ', '_').lower()}.pdf"
                }
                await db.documents.insert_one(document)
        
        return {"message": "Database seeded successfully", "card_ids": card_ids}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Include goals routes
from routes_goals import router as goals_router
api_router.include_router(goals_router)

# Include subscriptions routes
from routes_subscriptions import router as subscriptions_router
api_router.include_router(subscriptions_router)

# Include vault routes
from routes_vault import router as vault_router
api_router.include_router(vault_router)

# Include missions routes
from routes_missions import router as missions_router
api_router.include_router(missions_router)

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)