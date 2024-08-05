from fastapi import HTTPException, status
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def check(post_to_check, id: int = None, mode: str = "Post", detail_msg: str = None):
    if not post_to_check and not detail_msg:
        raise HTTPException(
            status_code=(
                status.HTTP_404_NOT_FOUND
                if mode != "auth"
                else status.HTTP_403_FORBIDDEN
            ),
            detail=(
                f"{mode} with id: '{id}' not found"
                if mode != "auth"
                else "Invalid credentials"
            ),
        )
    elif detail_msg and not post_to_check:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail_msg)


async def hash(password: str):
    return pwd_context.hash(password)


async def verify(user_provided, hashed_pass):
    return pwd_context.verify(user_provided, hashed_pass)
