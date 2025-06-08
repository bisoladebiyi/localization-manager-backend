from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
from supabase import create_client, Client
from dotenv import load_dotenv
from datetime import datetime
from typing import Dict, List, Optional
from uuid import UUID
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

# Supabase setup 
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_API_KEY = os.getenv("SUPABASE_API_KEY")
SUPABASE_TABLE = "localizations"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_API_KEY)

# Model 
class TranslationValue(BaseModel):
    value: Optional[str] = None
    updatedAt: Optional[datetime] = None
    updatedBy: Optional[str] = None

class Localization(BaseModel):
    key: str                     
    category: Optional[str] = None     
    description: Optional[str] = None
    translations: Dict[str, TranslationValue]

class LocalizationUpdate(BaseModel):
    id: UUID
    key: str
    category: Optional[str] = None
    description: Optional[str] = None
    translations: Dict[str, TranslationValue]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Serialize translation updatedby property
def serialize_props(obj):
    if isinstance(obj, datetime):
        return obj.isoformat() 
    if isinstance(obj, UUID):
        return str(obj)
    return obj

def deep_serialize(data):
    if isinstance(data, dict):
        return {k: deep_serialize(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [deep_serialize(item) for item in data]
    else:
        return serialize_props(data)


# ENDPOINT 
@app.get("/api/localizations")
def get_localizations():
    response = supabase.table("localizations").select("*").execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="No localizations found")
    return response.data

@app.get("/api/localizations/{id}")
def get_localization(id: str):
    response = supabase.table("localizations").select("*").eq("id", id).single().execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Localization not found")
    return response.data

@app.post("/api/localizations")
def create_localization(localization: Localization):
    try:
        serialized_data = deep_serialize(localization.model_dump())
        response = supabase.table("localizations").insert(serialized_data).execute()
        return {
            "data": response.data,
            "message": "Localization created successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/api/localizations/{id}")
def edit_localization(id: str, localization: LocalizationUpdate):
    try:
        serialized_data = deep_serialize(localization.model_dump())
        response = supabase.table("localizations").update(serialized_data).eq("id",id).execute()
        return {"data": response.data, "message": "Localization updated successfully"} 
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/localizations/{id}")
def delete_localization(id: str):
    try:
        response = supabase.table("localizations").delete().eq("id", id).execute()
        return {"data": response.data, "message": "Localization deleted successfully"}   
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# EXTRA 
@app.post("/api/localizations/bulk-update")
def bulk_update_localizations(localizations: List[LocalizationUpdate]):
    updateCount = 0
    failedUpdatesId = []

    for localization in localizations:
        try:
            serialized_data = deep_serialize(localization.model_dump())
            response = supabase.table("localizations").update(serialized_data).eq("id", localization.id).execute()

            if response.data:
                updateCount += 1
            else:
                failedUpdatesId.append(localization.id)
        except Exception:
            failedUpdatesId.append(localization.id)

    return {"updateCount": updateCount, "failedUpdatesId": failedUpdatesId}