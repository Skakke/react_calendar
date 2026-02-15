from app.database import SessionLocal
from app import models
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_user(db, username: str, password: str):
    # skip if already exists
    existing = db.query(models.User).filter(models.User.username == username).first()
    if existing:
        print(f"User already exists: {username} (skipping)")
        return existing

    user = models.User(
        username=username,
        password_hash=pwd_context.hash(password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    print(f"Created user: {username}")
    return user

def main():
    db = SessionLocal()
    try:
        create_user(db, "hans", "hans123")
        create_user(db, "anna", "anna123")
        create_user(db, "peter", "peter123")
    finally:
        db.close()

if __name__ == "__main__":
    main()
