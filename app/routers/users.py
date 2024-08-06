from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Depends, APIRouter

from .. import models, schemas
from ..utils import hash, check
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix='/users',
    tags=['Users']
)


# ============================================ create ============================================
@router.post(
    "", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse
)
async def create_user(new_user: schemas.UserCreate, db: Session = Depends(get_db)):

    new_user.password = await hash(new_user.password)
    created_user = models.User(**new_user.model_dump())
    
    try:
        db.add(created_user)
        db.commit()
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="This email is already registered")
    db.refresh(created_user)

    return created_user


# ============================================ get ============================================
@router.get("/{id}", response_model=schemas.UserResponse)
async def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    await check(user, id, "User")
    return user
