from fastapi import APIRouter, HTTPException, Request, status
from app.models.user_model import UserRegister, UserLogin, ChangePassword, ForgetPassword
from app.utils.auth import hash_password, verify_password
from app.database.mongo import users
from datetime import datetime, timezone
from bson.objectid import ObjectId


router = APIRouter()

session_store = {}


@router.get("/health")
async def health_check():
    return {"message":"app is running healthy"}

@router.post("/register")
async def register(user: UserRegister):
    existing_user = users.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_pwd = hash_password(user.password)
    users.insert_one({**user.dict(exclude={"password"}), "password": hashed_pwd, "password_history": [hashed_pwd], "change_count": []})
    return {"message": "User registered successfully"}

@router.post("/login")
async def login(user: UserLogin, request: Request):
    user_data = users.find_one({"email": user.email})
    if not user_data or not verify_password(user.password, user_data["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    session_store[user.email] = True
    request.session = {"user": user.email}
    return {"message": "Logged in successfully", "user": user.email}

