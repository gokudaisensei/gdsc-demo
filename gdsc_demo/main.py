from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from datetime import timedelta, datetime
from typing import Annotated

from contextlib import asynccontextmanager

from passlib.context import CryptContext
from jose import jwt, JWTError

import schemas
import models

SECRET_KEY = "74cc957a4e35ec2fd0a8745cc9a2e8f3a0cb05bdb1fd9dab86273e68f66356e2"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@asynccontextmanager
async def lifespan(app: FastAPI):
    models.Base.metadata.create_all(models.ENGINE)
    setup()

    yield

    models.Base.metadata.drop_all(models.ENGINE)
    models.session.close()


app = FastAPI(lifespan=lifespan)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db: Session, username: str) -> models.User | None:
    return db.query(models.User).filter(models.User.username == username).first()


def authenticate_user(db, username: str, password: str):
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(models.session, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


@app.get("/")
def root():
    return {"message": "Root URL"}


@app.post("/token", response_model=schemas.Token)
def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = authenticate_user(models.session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/products", response_model=list[schemas.Product])
def get_all_products(user: schemas.User = Depends(get_current_user)):
    return models.session.query(models.Product).all()


@app.get("/products/{product_id}", response_model=schemas.Product)
def get_product_by_id(product_id: int, user: schemas.User = Depends(get_current_user)):
    if product := models.session.query(models.Product).get(product_id):
        return product
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
    )


@app.get("/me")
def get_current_user_information(
    current_user: schemas.User = Depends(get_current_user),
):
    return current_user


@app.get("/users", response_model=list[schemas.Product])
def get_all_users(user: schemas.User = Depends(get_current_user)):
    return models.session.query(models.User).all()


@app.post("/users")
async def create_user(
    user_in: schemas.UserCreate,
    current_user: models.User = Depends(get_current_user),
):
    if get_user(models.session, username=user_in.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The user with this username already exists in the system.",
        )
    user = user_in.model_dump()
    user["hashed_password"] = get_password_hash(user["password"])
    del user["password"]
    models.session.add(models.User(**user))
    return user


def setup():
    dummy_products = [
        models.Product(
            name="Product 1", price=10.99, description="Description for Product 1"
        ),
        models.Product(
            name="Product 2", price=19.99, description="Description for Product 2"
        ),
        models.Product(
            name="Product 3", price=5.99, description="Description for Product 3"
        ),
    ]

    dummy_users = [
        models.User(username="user1", hashed_password=get_password_hash("pwd1")),
        models.User(username="user2", hashed_password=get_password_hash("pwd2")),
        models.User(username="user3", hashed_password=get_password_hash("pwd3")),
    ]

    models.session.add_all(dummy_products)
    models.session.add_all(dummy_users)
    models.session.commit()
