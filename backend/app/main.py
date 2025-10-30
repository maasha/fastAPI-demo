from fastapi import FastAPI, HTTPException
from app.models import User, UserCreate, UserUpdate

app = FastAPI()

# In-memory storage (temporary - will be replaced with PostgreSQL later)
users_db = []
user_id_counter = 1


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
def create_user(user: UserCreate):
    """Create a new user"""
    global user_id_counter
    
    # Create user dictionary with ID
    new_user = {
        "id": user_id_counter,
        "name": user.name,
        "age": user.age,
        "address": user.address
    }
    
    # Add to database and increment counter
    users_db.append(new_user)
    user_id_counter += 1
    
    return new_user


@app.get("/users", response_model=list[User])
def get_all_users():
    """Get all users"""
    return users_db


@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: int):
    """Get a single user by ID"""
    for user in users_db:
        if user["id"] == user_id:
            return user
    
    # User not found
    raise HTTPException(status_code=404, detail=f"User with id {user_id} not found")


@app.put("/users/{user_id}", response_model=User)
def update_user(user_id: int, user_update: UserUpdate):
    """Update a user by ID"""
    for user in users_db:
        if user["id"] == user_id:
            # Update only the fields that were provided
            if user_update.name is not None:
                user["name"] = user_update.name
            if user_update.age is not None:
                user["age"] = user_update.age
            if user_update.address is not None:
                user["address"] = user_update.address
            
            return user
    
    # User not found
    raise HTTPException(status_code=404, detail=f"User with id {user_id} not found")


@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    """Delete a user by ID"""
    for i, user in enumerate(users_db):
        if user["id"] == user_id:
            users_db.pop(i)
            return {"message": f"User {user_id} deleted successfully"}
    
    # User not found
    raise HTTPException(status_code=404, detail=f"User with id {user_id} not found")
