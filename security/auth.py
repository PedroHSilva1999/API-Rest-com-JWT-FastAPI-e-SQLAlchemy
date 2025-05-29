from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from datetime import datetime, timedelta
from core.configs import settings
import pytz
from security.security import verify_password
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException
from core.deps import get_session
from models.users import User
from typing import Optional
from sqlalchemy import select
from fastapi import status
from pydantic import BaseModel

oauth2_schema = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/users/login")

async def authenticate_user(email: str, password: str, db: AsyncSession = Depends(get_session)) -> Optional[User]:

    async with db as session:
        query = select(User).filter(User.email == email)
        result = await session.execute(query)
        user: User | None = result.scalar_one_or_none()

        if not user:
            return None
        
        if not verify_password(password, user.password):
            return None
        
        return user
    
def _create_access_token(token_type: str, time_expires: datetime, sub: str) -> str:
    payload = {}
    location_timezone = pytz.timezone("America/Sao_Paulo")
    expire = datetime.now(tz=location_timezone) + time_expires
    payload["type"] = token_type
    payload["exp"] = expire
    payload["sub"] = str(sub)

    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.ALGORITHM)

def create_access_token(sub: str) -> str:
    return _create_access_token(
        token_type="access_token",
        time_expires=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        sub=sub
    )

class TokenData(BaseModel):
    user_id: str | None = None

async def get_current_user(db:AsyncSession = Depends(get_session), token: str = Depends(oauth2_schema)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível autenticar a credencial",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.ALGORITHM],
            options={"verify_aud": False},
        )

        user_id: str = payload.get("sub")

        if user_id is None:
            raise credentials_exception
        
        token_data = TokenData(user_id=user_id)

        if token_data.user_id is None:
            raise credentials_exception
        
    except JWTError:
        raise credentials_exception
    
    async with db as session:
        query = select(User).filter(User.id == int(token_data.user_id))
        result = await session.execute(query)
        user: User | None = result.scalar_one_or_none()

        if user is None:
            raise credentials_exception
        
        return user
    
    


    
    
    
