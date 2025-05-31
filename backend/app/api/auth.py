from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.core.database import get_db
from app.models.user import User
from app.schemas.auth import UserLogin, UserRegister, Token
from app.core.security import verify_password, get_password_hash, create_access_token

router = APIRouter()

@router.post("/register", response_model=Token)
async def register(user: UserRegister, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == user.email))
    if result.scalar():
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = User(
        email=user.email,
        name=user.name,
        password_hash=get_password_hash(user.password)
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    access_token = create_access_token({"sub": str(new_user.id)})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/login", response_model=Token)
async def login(user: UserLogin, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == user.email))
    db_user = result.scalar()
    if not db_user or not verify_password(user.password, db_user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token({"sub": str(db_user.id)})
    return {"access_token": access_token, "token_type": "bearer"} 