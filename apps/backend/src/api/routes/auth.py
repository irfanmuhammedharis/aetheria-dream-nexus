# Verified against Phase 2: Auth endpoints for registration and login

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from apps.backend.src.core.database import get_db
from apps.backend.src.services.auth import hash_password, verify_password, create_access_token
from apps.backend.src.models.db_models import User
from sqlalchemy import select
import uuid

router = APIRouter()

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

@router.post('/register')
async def register(request: RegisterRequest, db: AsyncSession = Depends(get_db)):
    # Check existing
    res = await db.execute(select(User).where(User.email == request.email))
    existing = res.scalar_one_or_none()
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Email already registered')

    new_user = User(id=uuid.uuid4(), email=request.email, password_hash=hash_password(request.password))
    db.add(new_user)
    await db.commit()
    return {'status': 'registered', 'user_id': str(new_user.id)}

@router.post('/login')
async def login(request: LoginRequest, db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(User).where(User.email == request.email))
    user = res.scalar_one_or_none()
    if not user or not verify_password(request.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid credentials')

    token = create_access_token(subject=str(user.id))
    return {'access_token': token, 'token_type': 'bearer'}

# Verification Log
# - Implemented simple registration and login endpoints.
# - Uses AsyncSession dependency and password hashing/JWT token generation.
# - Assumption: Token expiry and refresh not implemented; will add if approved.