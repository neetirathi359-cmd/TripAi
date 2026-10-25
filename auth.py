from datetime import datetime
from fastapi import APIRouter, HTTPException, status
from config.database import users_collection
from schemas.user_schema import UserCreate, UserLogin, Token
from models.user_model import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(user: UserCreate):
    existing_user = await users_collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_pwd = hash_password(user.password)
    new_user = {
        "name": user.name,
        "email": user.email,
        "password": hashed_pwd,
        "createdAt": datetime.utcnow()
    }
    
    result = await users_collection.insert_one(new_user)
    return {"message": "User created successfully", "userId": str(result.inserted_id)}

@router.post("/login", response_model=Token)
async def login(user_data: UserLogin):
    user = await users_collection.find_one({"email": user_data.email})
    if not user or not verify_password(user_data.password, user["password"]):
        raise HTTPException(status_code=400, detail="Invalid email or password")
    
    user_id_str = str(user["_id"])
    access_token = create_access_token(data={"sub": user_id_str})
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user_id_str,
            "name": user["name"],
            "email": user["email"]
        }
    }