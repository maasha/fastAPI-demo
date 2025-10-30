from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from app.models import User, UserCreate, UserUpdate
from app.database import engine, get_db
from app import db_models
from app.db_models import UserDB

app = FastAPI()

# Create database tables on startup
@app.on_event("startup")
def on_startup():
    db_models.Base.metadata.create_all(bind=engine)


@app.get("/")
def read_root():
    return {"message": "Hello World"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.get("/about")
def about():
    return {
        "name": "Analytics Platform API",
        "version": "1.0.0",
        "description": "Demo API for job interview"
    }


@app.post("/users", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """Create a new user"""
    # Create database user object
    db_user = UserDB(
        name=user.name,
        age=user.age,
        address=user.address
    )
    
    # Add to database and commit
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user


@app.get("/users", response_model=list[User])
def get_all_users(db: Session = Depends(get_db)):
    """Get all users"""
    return db.query(UserDB).all()


@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """Get a single user by ID"""
    user = db.query(UserDB).filter(UserDB.id == user_id).first()
    
    if user is None:
        raise HTTPException(status_code=404, detail=f"User with id {user_id} not found")
    
    return user


@app.put("/users/{user_id}", response_model=User)
def update_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
    """Update a user by ID"""
    user = db.query(UserDB).filter(UserDB.id == user_id).first()
    
    if user is None:
        raise HTTPException(status_code=404, detail=f"User with id {user_id} not found")
    
    # Update only the fields that were provided
    update_data = user_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(user, key, value)
    
    db.commit()
    db.refresh(user)
    
    return user


@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """Delete a user by ID"""
    user = db.query(UserDB).filter(UserDB.id == user_id).first()
    
    if user is None:
        raise HTTPException(status_code=404, detail=f"User with id {user_id} not found")
    
    db.delete(user)
    db.commit()
    
    return {"message": f"User {user_id} deleted successfully"}
