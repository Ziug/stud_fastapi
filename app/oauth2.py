from datetime import timedelta, datetime, timezone, tzinfo
from jwt import PyJWTError
import jwt

from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from . import models
from .database import get_db
from .schemas import TokenData
from .config import settings


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = f'{settings.secret_key}'
ALGORITHM = f'{settings.algorithm}'
ACCESS_TOKEN_EXPIRE_MINUTES = int(settings.access_token_expire_minutes)

async def create_access_token(data: dict):
    to_encode = data.copy()
    
    expire = datetime.now(timezone(timedelta(hours=3))) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    
    encoded = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded


async def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM) 
        id: str = str(payload.get('user_id'))
        
        if not id:
            raise credentials_exception
        token_data = TokenData(id=id)
    except PyJWTError:
        raise credentials_exception
    
    return token_data
    
    
async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code = status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentails',
        headers={"WWW-Authenticate": "Bearer"})
    
    token = await verify_access_token(token, credentials_exception)
    user = db.query(models.User).filter(models.User.id == token.id).first()
    
    return user