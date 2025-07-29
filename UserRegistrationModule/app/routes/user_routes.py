import os
from fastapi import APIRouter, HTTPException, status, Depends,Request, Depends
from fastapi.security import OAuth2PasswordBearer
from app.models.user_model import ChangeDetails, ChangePassword, ForgetPassword, UserRegister, UserLogin
from app.utils.auth import hash_mobile_number, hash_password, verify_password, create_access_token, verify_token
from app.database.mongo import users
from datetime import datetime, timedelta, timezone
from bson import ObjectId
from openai import OpenAI
from app.utils.blacklist import add_to_blacklist



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

from app.utils.gpt_utils import explain_password_strength

client = OpenAI (api_key = os.getenv("OPENAI_API_KEY"))



router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

@router.get("/health")
async def health_check():
    return {"message": "App is running Healthy"}

@router.post("/register")
async def register(user: UserRegister):
    existing_user = users.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    

    hashed_pwd = hash_password(user.password)
    password_quality_suggestion = explain_password_strength(user.password)
    users.insert_one({
        **user.model_dump(exclude={"password"}),
        "password": hashed_pwd,
        "password_history": [hashed_pwd],
        "change_count": []
    })
    return {"message": "User registered successfully",
            "password_strength": password_quality_suggestion
            }

@router.post("/login")
async def login(user: UserLogin):
    db_user = users.find_one({"email": user.email})
    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = create_access_token({"sub": str(db_user["_id"])}, timedelta(minutes=30))
    return {"access_token": token, "token_type": "bearer"}

@router.post("/change-password")
async def change_password(data: ChangePassword, token: str = Depends(oauth2_scheme)):
    user_data = verify_token(token)
    user_id = user_data.get("sub")
    user = users.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not verify_password(data.old_password, user["password"]):
        raise HTTPException(status_code=400, detail="Old password is incorrect")

    today = datetime.now(timezone.utc).date()
    changes_today = [d for d in user["change_count"] if datetime.fromisoformat(d).date() == today]
    if len(changes_today) >= 3:
        raise HTTPException(status_code=400, detail="Password change limit reached for today")

    if data.new_password in user["password_history"]:
        raise HTTPException(status_code=400, detail="Password reuse is not allowed")

    hashed_new = hash_password(data.new_password)
    users.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": {"password": hashed_new},
         "$push": {"password_history": hashed_new, "change_count": [datetime.now(timezone.utc).isoformat()]}}
    )
    return {"message": "Password changed successfully"}

@router.post("/forget-password")
async def forget_password(data: ForgetPassword):
    user = users.find_one({"email": data.email})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    hashed_new = hash_password(data.new_password)
    users.update_one(
        {"email": data.email},
        {"$set": {"password": hashed_new},
         "$push": {"password_history": hashed_new, 
                   "change_count": [datetime.now(timezone.utc).isoformat()]
                   }
         }
    )
    return {"message": "Password reset successfully"}

@router.post("/change-mobile-number")
async def change_details(data: ChangeDetails, token: str = Depends(oauth2_scheme)):
    user_data = verify_token(token)
    user_id = user_data.get("sub")

    user = users.find_one({"_id": ObjectId(user_id), "mobile_number": data.old_mobile_number})
    if not user:
        raise HTTPException(status_code=404, detail="User not found or old mobile number does not match")

   
    users.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": {"mobile_number": data.new_mobile_number}}
    )

    return {"message": "Mobile number updated successfully", "new_mobile_number": data.new_mobile_number}

@router.get("/profile")
async def get_profile(token: str = Depends(oauth2_scheme)):
    user_data = verify_token(token)
    user_id = user_data.get("sub")
    user = users.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return {"email": user["email"]}


@router.post("/logout")
async def logout(token: str = Depends(oauth2_scheme)):
    add_to_blacklist(token)
    return {"message": "Logged out successfully and token blacklisted"}


