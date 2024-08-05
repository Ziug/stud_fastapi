from fastapi import HTTPException, Response, status, Depends, APIRouter
from typing import List, Optional
from sqlalchemy.orm import Session

from sqlalchemy import func
from .. import models, schemas, oauth2
from ..utils import check
from ..database import get_db


router = APIRouter(
    prefix='/posts',
    tags=['Posts']
)


# ============================================ get ============================================
# @router.get("", response_model=List[schemas.PostResponse])
@router.get("", response_model=List[schemas.PostVote])
async def get_posts(db: Session = Depends(get_db), limit: int = 10, skip: int = 0, search: Optional[str] = ''):
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip)

    return posts.all()


# Retrieves a list of posts owned by the current user.
@router.get("/my", response_model=List[schemas.PostVote])
async def get_post_my(db: Session = Depends(get_db),
                           current_user: int = Depends(oauth2.get_current_user)):
    
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.owner_id == current_user.id).all()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="You have no posts")
    return post


# Retrieves a single post by its ID.
@router.get("/{id}", response_model=schemas.PostVote)
async def get_posts(id: int, response: Response, 
                    db: Session = Depends(get_db),
                    current_user: int = Depends(oauth2.get_current_user)):
    # post = conn.execute("""SELECT * FROM posts WHERE id = %s""", (id,)).fetchone()
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    await check(post, id)
    return post

# Retrieves a list of posts owned by a specific user.
@router.get("/user/{id}", response_model=List[schemas.PostVote])
async def get_post_by_user(id: int, response: Response, 
                           db: Session = Depends(get_db)):
    
    if not db.query(models.User).filter(models.User.id == id).first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: '{id}' not found")
    
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.owner_id == id).all()
    await check(post, id, mode = "User", detail_msg = "This user has no posts")
    return post


# ============================================ create ============================================
@router.post(
    "", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse
)
async def create_posts(new_post: schemas.PostCreate, 
                       db: Session = Depends(get_db), 
                       current_user: models.User = Depends(oauth2.get_current_user)):
    # new_post = conn.execute(
    #     """INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",
    #     (new_post.title, new_post.content, new_post.published),
    # ).fetchone()
    # conn.commit()

    # print(current_user.email)
    created_post = models.Post(owner_id = current_user.id, **new_post.model_dump())
    db.add(created_post)
    db.commit()
    db.refresh(created_post)

    return created_post


# ============================================ delete ============================================
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, 
                      db: Session = Depends(get_db), 
                      current_user: int = Depends(oauth2.get_current_user)):
    # deleted_post = conn.execute(
    #     """DELETE FROM posts WHERE id = %s RETURNING title""", (id,)
    # ).fetchone()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    await check(post, id)

    if current_user.id != post.owner_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform this action")
    
    post_query.delete(synchronize_session=False)
    db.commit()


# ============================================ update ============================================
@router.put("/{id}", response_model=schemas.PostResponse)
async def update_post(id: int, updated_post: schemas.PostCreate, 
                      db: Session = Depends(get_db),
                      current_user: int = Depends(oauth2.get_current_user)):
    # updated_post = conn.execute(
    #     """UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
    #     (
    #         post.title,
    #         post.content,
    #         post.published,
    #         id,
    #     ),
    # ).fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    await check(post, id)
    
    if current_user.id != post.owner_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform this action")
    
    post_query.update(updated_post.model_dump(), synchronize_session=False)
    db.commit()
    return post_query.first()
