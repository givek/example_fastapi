from fastapi import HTTPException, status, Depends
from fastapi.params import Depends
from fastapi.routing import APIRouter

from sqlalchemy.orm import session
from sqlalchemy.orm.session import Session

from app import models
from app.utils import hash_password
from app.schemas import UserCreate
from app.database import get_db


router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # hash user password.
    user.password = hash_password(user.password)
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/{id}")
def get_user(id: int, db: session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="user does not exist"
        )
    return user
