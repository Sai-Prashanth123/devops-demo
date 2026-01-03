from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from database import user_collection
from models import UserCreate, UserLogin
from auth import hash_password, verify_password

app = FastAPI()

# Allow browser clients to preflight and call the API during local dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/register")
async def register(user:UserCreate):
    if user_collection.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="Email already registered")
    user_collection.insert_one({
        "email": user.email,
        "password": hash_password(user.password) 
    })
    return {"message": "User registered successfully"}

@app.post("/login")
async def login(user:UserLogin):
    db_user = user_collection.find_one({"email": user.email})
    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    return {"message": "Login successful"}
