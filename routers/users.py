from fastapi import APIRouter
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from dependency import get_db
from models import users as models
from schemas import users as schemas

router = APIRouter()


@router.get('/read/{user_id}/', response_model=schemas.User, status_code=status.HTTP_200_OK)
async def user_read(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='not found')
    return user


@router.post('/create/', response_model=schemas.User, status_code=status.HTTP_201_CREATED)
async def user_create(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user_username = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user_username:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="username already exists")

    db_user_email = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user_email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="email already exists")

    user = models.User(username=user.username, email=user.email, password=user.password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
