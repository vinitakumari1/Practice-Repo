from fastapi import APIRouter, HTTPException, Request, status
from app.models.user_model import UserRegister, UserLogin, ChangePassword, ForgetPassword
from app.utils.auth import hash_password, verify_password
from app.database.mongo import users
from datetime import datetime, timezone
from bson.objectid import ObjectId


router = APIRouter()

session_store = {}

# Simple GET route to verify the API is working.
@router.get("/health")
async def health_check():
    return {"message":"app is running healthy"}

@router.post("/register")
async def register(user: UserRegister):
# Simple GET route to verify the API is working.
    existing_user = users.find_one({"email": user.email}) # Checks if the user already exists in the DB by email.
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered") # If user exists, raise an error.
    hashed_pwd = hash_password(user.password) #Hashes the user's password before saving.
    users.insert_one({**user.model_dump(exclude={"password"}), "password": hashed_pwd, "password_history": [hashed_pwd], "change_count": []}) #Saves user data to MongoDB, excluding the plain password.
    return {"message": "User registered successfully"}

@router.post("/login")
async def login(user: UserLogin, request: Request):
    user_data = users.find_one({"email": user.email})
    if not user_data or not verify_password(user.password, user_data["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    session_store[user.email] = True
    
    return {"message": "Logged in successfully", "user": user.email}


@router.post("/change-password")
async def change_password(data: ChangePassword, request: Request):
    email = request.headers.get("X-User-Email") #Gets email from request headers (acts as session/user identity).
    if not email or email not in session_store:
        raise HTTPException(status_code=403, detail="Not logged in")
    user = users.find_one({"email": email})
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
        {"email": email},
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
        {"$set": {"password": hashed_new}, "$push": {"password_history": hashed_new, "change_count": [datetime.now(timezone.utc).isoformat()]}}
    )
    return {"message": "Password reset successfully"}

@router.post("/logout")
async def logout(request: Request):
    email = request.headers.get("X-User-Email")
    if email in session_store:
        del session_store[email]
    return {"message": "User logged out"}