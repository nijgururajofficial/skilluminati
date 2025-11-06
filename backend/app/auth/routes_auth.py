"""Authentication routes - signup and login."""

from fastapi import APIRouter, HTTPException, status
from app.models.schemas import UserSignup, UserLogin, TokenResponse
from app.auth.jwt_handler import hash_password, verify_password, create_access_token
from app.db.memory_store import get_users_db

router = APIRouter(tags=["authentication"])


@router.post("/signup", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def signup(user: UserSignup):
    """
    Register a new user and return JWT token.
    """
    users_db = get_users_db()
    
    if user.email in users_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    
    # Hash password and store user
    hashed_password = hash_password(user.password)
    users_db[user.email] = {
        "email": user.email,
        "password": hashed_password,
        "name": user.name,
    }
    
    # Create access token
    access_token = create_access_token(data={"sub": user.email})
    return TokenResponse(access_token=access_token)


@router.post("/login", response_model=TokenResponse)
async def login(user: UserLogin):
    """
    Authenticate user and return JWT token.
    """
    users_db = get_users_db()
    
    if user.email not in users_db:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    
    stored_user = users_db[user.email]
    if not verify_password(user.password, stored_user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    
    # Create access token
    access_token = create_access_token(data={"sub": user.email})
    return TokenResponse(access_token=access_token)

