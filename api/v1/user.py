from typing import Any
from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from models.users import User
from schemas.user_schema import UserSchema, UserSchemaCreate, UserSchemaOut
from security.auth import authenticate_user, create_access_token, get_current_user
from sqlalchemy.ext.asyncio import AsyncSession
from core.deps import get_session
from security.security import generate_password_hash
router = APIRouter()

@router.get("/check_user", response_model=UserSchema)
async def check_user(user: User = Depends(get_current_user)):
    return user

@router.post("/create_user", response_model=UserSchema)
async def create_user(user:UserSchemaCreate, db:AsyncSession = Depends(get_session)):
    new_user: User = User(
        name=user.name,
        email=user.email,
        password=generate_password_hash(user.password),
        is_admin=user.is_admin,
        is_active=user.is_active
    )
    
    async with db as session:
        try:
            session.add(new_user)
            await session.commit()
            await session.refresh(new_user)
            return new_user
        except Exception as e:
             raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Erro ao criar usuário: {e}")
        
@router.get("/get_users", response_model=list[UserSchemaOut])
async def get_users(db:AsyncSession = Depends(get_session), current_user: User = Depends(get_current_user)):
    async with db as session:
        query = select(User)
        result = await session.execute(query)
        users: list[UserSchemaOut] = result.scalars().all()
        return users
    
@router.get("/get_user_by_id/{user_id}", response_model=UserSchema)
async def get_user_by_id(user_id:int, db:AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(User).filter(User.id == user_id)
        result = await session.execute(query)
        user: User | None = result.scalar_one_or_none()
        return user

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db:AsyncSession = Depends(get_session)) -> Any:
    user = await authenticate_user(form_data.username, form_data.password, db=db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuário ou senha inválidos")
    
    return JSONResponse(content={
        "access_token": create_access_token(user.id),
        "token_type": "Bearer"
    })

@router.put("/update_user/{user_id}", response_model=UserSchema)
async def update_user(user_id:int, user:UserSchema, db:AsyncSession = Depends(get_session), current_user: User = Depends(get_current_user)):
    new_user = User(
        name=user.name,
        email=user.email,
        password=generate_password_hash(user.password),
        is_admin=user.is_admin,
        is_active=user.is_active
    )

    async with db as session:   
        query = select(User).filter(User.id == user_id)
        result = await session.execute(query)
        user_db = result.scalar_one_or_none()
        if user_db is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")
        
        user_db.name = new_user.name
        user_db.email = new_user.email
        user_db.password = new_user.password
        user_db.is_admin = new_user.is_admin
        user_db.is_active = new_user.is_active

        session.add(user_db)
        await session.commit()
        return user_db

@router.delete("/delete_user/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id:int, db:AsyncSession = Depends(get_session), current_user: User = Depends(get_current_user)):
    async with db as session:
        query = select(User).filter(User.id == user_id)
        result = await session.execute(query)
        user_db = result.scalar_one_or_none()
        if user_db is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")
        
        await session.delete(user_db)
        await session.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
