import os
import bcrypt
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

# --- Database ---
MONGO_URL = os.getenv("MONGO_URL", "")
client = MongoClient(MONGO_URL)
db = client["fastapi"]
user_collection = db["sample_data"]

# --- App ---
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Models ---
class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

# --- Helpers ---
def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))

# --- Health endpoints ---
@app.get("/")
def root():
    return {"status": "ok", "message": "Backend is running"}

@app.get("/health")
def health():
    try:
        client.admin.command("ping")
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "database": str(e)}

# --- Auth endpoints ---
@app.post("/register")
def register(user: UserCreate):
    if user_collection.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="Email already registered")
    user_collection.insert_one({
        "email": user.email,
        "password": hash_password(user.password),
    })
    return {"message": "User registered successfully"}

@app.post("/login")
def login(user: UserLogin):
    db_user = user_collection.find_one({"email": user.email})
    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    return {"message": "Login successful"}
