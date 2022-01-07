from fastapi import status, HTTPException
from fastapi.param_functions import Depends
from fastapi.routing import APIRouter

from sqlalchemy.orm import Session

from app import models
from app.oauth2 import get_current_user
from app.schemas import Vote
from app.database import get_db


router = APIRouter(prefix="/vote", tags=["Votes"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: Vote, db: Session = Depends(get_db), user=Depends(get_current_user)):

    vote_query = db.query(models.Vote).filter(
        models.Vote.post_id == vote.post_id, models.Vote.user_id == user.id
    )

    found_vote = vote_query.first()

    if vote.dir == 1:
        if found_vote:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="user has already voted this post.",
            )

        new_vote = models.Vote(post_id=vote.post_id, user_id=user.id)
        db.add(new_vote)
        db.commit()
        return {"message", "successfully added vote."}
    else:
        if not found_vote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Vote does not exists."
            )

        vote_query.delete(synchronize_session=False)
        db.commit()

        return {"message", "successfully deleted vote."}
