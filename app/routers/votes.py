from fastapi import HTTPException, Response, status, Depends, APIRouter
from sqlalchemy.orm import Session

from ..utils import check
from ..schemas import Vote
from ..database import get_db
from .. import models, oauth2


router = APIRouter(prefix = '/vote', tags=["Vote"])


@router.post("", status_code=status.HTTP_201_CREATED)
async def vote(vote: Vote, 
               db: Session = Depends(get_db), 
               current_user: models.User = Depends(oauth2.get_current_user)):
    
    await check(db.query(models.Post).filter(models.Post.id == vote.post_id).first(), vote.post_id)
    
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()
    
    
    if vote.like_status:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                                detail=f"User {current_user.id} has already voted on post {vote.post_id}")
            
        new_vote = models.Vote(post_id = vote.post_id, user_id = current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "Vote added successfully"}
    
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                                detail="Vote does not exist")
        
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "Vote deleted successfully"}