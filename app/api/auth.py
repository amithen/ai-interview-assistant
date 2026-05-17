from fastapi import Depends, HTTPException,APIRouter
from sqlalchemy.orm import Session
from starlette import status

from app.db.session import get_db
from app.models.user import User
from app.schemas.user_schema import UserCreate, UserLogin

from app.auth.hashing import hash_password, verify_password
from app.auth.jwt_handler import create_access_token

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(request: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == request.email).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Email already registered")
    new_user = User(name=request.name, email=request.email, hashed_password=hash_password(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User created successfully"}


@router.post("/login", status_code=status.HTTP_201_CREATED)
async def login(request: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Incorrect email or password")
    if not verify_password(request.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Incorrect email or password")

    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


