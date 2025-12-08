from backend.user_database import SessionLocal, User
from passlib.context import CryptContext
from sqlalchemy.exc import IntegrityError

pwd_ctx = CryptContext(schemes=["sha256_crypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_ctx.hash(password)

def verify_password(plain, hashed):
    return pwd_ctx.verify(plain, hashed)


def create_user(username: str, password: str):
    db = SessionLocal()
    try:
        hashed_pw = get_password_hash(password)
        user = User(username=username, hashed_password=hashed_pw)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    except IntegrityError:
        db.rollback()
        raise ValueError("Username already exists")
    finally:
        db.close()

def authenticate_user(username: str, password: str):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.username == username).first()
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user
    finally:
        db.close()
