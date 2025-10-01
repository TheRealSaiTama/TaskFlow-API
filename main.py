from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import schemas, auth, models
from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import Session
from database import engine, SessionLocal
from models import Base
from fastapi.middleware.cors import CORSMiddleware
from datetime import timedelta
import uvicorn

app = FastAPI()

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# create the table
Base.metadata.create_all(bind=engine)



# --- DB session dependency ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# --- Authentication dependency ---
async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token_data = auth.verify_token(token, credentials_exception)
    user = db.query(models.User).filter(models.User.email == token_data.email).first()
    if user is None:
        raise credentials_exception
    return schemas.User.from_orm(user)


# --- routes ---
@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = auth.get_password_hash(user.password)

    new_user = models.User(email=user.email, hashed_password=hashed_password)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me/", response_model=schemas.User)
async def read_users_me(current_user = Depends(get_current_user)):
    return current_user 


@app.post("/boards", response_model=schemas.Board)
async def create_board(
    board: schemas.BoardCreate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    new_board = models.Board(name=board.name, user_id=current_user.id)
    db.add(new_board)
    db.commit()
    db.refresh(new_board)
    return new_board 

from typing import List
@app.get("/boards/", response_model=List[schemas.Board])
async def getboard(db: Session=Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    boards = db.query(models.Board).filter(models.Board.user_id == current_user.id).all()
    return boards

@app.get("/boards/{board_id}", response_model=schemas.Board)
async def get_board(board_id: int, db: Session=Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    board = db.query(models.Board).filter(models.Board.id == board_id, models.Board.user_id == current_user.id).first()
    if not board:
        raise HTTPException(status_code=404, detail="Board not found")
    return board

@app.put("/boards/{board_id}", response_model=schemas.Board)
async def update_board(board_id: int, board_data: schemas.BoardCreate, db: Session=Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    db_board = db.query(models.Board).filter(models.Board.id == board_id, models.Board.user_id == current_user.id).first()
    if not db_board:
        raise HTTPException(status_code=404, detail="Board not found")
    db_board.name = board_data.name
    db.commit()
    db.refresh(db_board)
    return db_board

@app.delete("/boards/{board_id}", response_model=schemas.Board)
async def delete_board(board_id: int, db: Session=Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    board = db.query(models.Board).filter(models.Board.id == board_id, models.Board.user_id == current_user.id).first()
    if not board:
        raise HTTPException(status_code=404, detail="Board not found")
    db.delete(board)
    db.commit()
    return board


@app.post("/boards/{board_id}/columns/", response_model=schemas.Column)
async def create_column(board_id: int, column: schemas.ColumnCreate, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    db_board = db.query(models.Board).filter(models.Board.id == board_id, models.Board.user_id == current_user.id).first()
    if not db_board:
        raise HTTPException(status_code=404, detail="Board not found")
    new_column = models.Column(title=column.title, board_id=board_id)
    db.add(new_column)
    db.commit()
    db.refresh(new_column)
    return new_column

@app.get("/boards/{board_id}/columns/", response_model=List[schemas.Column])
async def get_columns(board_id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    db_board = db.query(models.Board).filter(models.Board.id == board_id, models.Board.user_id == current_user.id).first()
    if not db_board:
        raise HTTPException(status_code=404, detail="Board not found")
    columns = db.query(models.Column).filter(models.Column.board_id == board_id).all()
    return columns

@app.put("/columns/{column_id}", response_model=schemas.Column)
async def update_column(column_id: int, column_data: schemas.ColumnCreate, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    db_column = db.query(models.Column).join(models.Board).filter(models.Column.id == column_id, models.Board.user_id == current_user.id).first()
    if not db_column:
        raise HTTPException(status_code=404, detail="Column not found")
    db_column.title = column_data.title
    db.commit()
    db.refresh(db_column)
    return db_column

@app.delete("/columns/{column_id}", response_model=schemas.Column)
async def delete_column(column_id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    db_column = db.query(models.Column).join(models.Board).filter(models.Column.id == column_id, models.Board.user_id == current_user.id).first()
    if not db_column:
        raise HTTPException(status_code=404, detail="Column not found")
    db.delete(db_column)
    db.commit()
    return db_column

@app.post("/columns/{column_id}/cards/", response_model=schemas.Card)
async def create_card(column_id: int, card: schemas.CardCreate, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    db_column = db.query(models.Column).join(models.Board).filter(models.Column.id == column_id, models.Board.user_id == current_user.id).first()
    if not db_column:
        raise HTTPException(status_code=404, detail='column not found or access denied')

    new_card = models.Card(
        title=card.title,
        content=card.content,
        position=card.position,
        column_id=column_id
    )

    db.add(new_card)
    db.commit()
    db.refresh(new_card)
    return new_card

@app.get("/columns/{column_id}/cards/", response_model=List[schemas.Card])
async def get_cards(column_id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    db_column = db.query(models.Column).join(models.Board).filter(models.Column.id == column_id, models.Board.user_id == current_user.id).first()
    if not db_column:
        raise HTTPException(status_code=404, detail='column not found or access denied')
    cards = db.query(models.Card).filter(models.Card.column_id == column_id).all()
    return cards

@app.put("/cards/{card_id}", response_model=schemas.Card)
async def update_card(card_id: int, card_data: schemas.CardCreate, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    db_card = db.query(models.Card).join(models.Column).join(models.Board).filter(models.Card.id == card_id, models.Board.user_id == current_user.id).first()
    if not db_card:
        raise HTTPException(status_code=404, detail='card not found or access denied')
    db_card.title = card_data.title
    db_card.content = card_data.content
    db_card.position = card_data.position
    db.commit()
    db.refresh(db_card)
    return db_card

@app.delete("/cards/{card_id}", response_model=schemas.Card)
async def delete_card(card_id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    db_card = db.query(models.Card).join(models.Column).join(models.Board).filter(models.Card.id == card_id, models.Board.user_id == current_user.id).first()
    if not db_card:
        raise HTTPException(status_code=404, detail='card not found or access denied')
    db.delete(db_card)
    db.commit()
    return db_card