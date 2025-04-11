from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import List, Dict, Optional

app = FastAPI()

# Модель данных
class User(BaseModel):
    id: int
    name: str
    email: str

class UserCreate(BaseModel):
    name: str
    email: str

# "База данных" - храним пользователей в памяти
db: List[User] = [
    User(id=1, name="Ivan Ivanov", email="i.i.ivanov@mail.com"),
    User(id=2, name="Petr Petrov", email="p.p.petrov@mail.com")
]

@app.get("/api/v1/user", response_model=User)
def get_user(email: str):
    """Получение пользователя по email"""
    user = next((u for u in db if u.email == email), None)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user

@app.post("/api/v1/user", status_code=status.HTTP_201_CREATED, response_model=User)
def create_user(user_data: UserCreate):
    """Создание нового пользователя"""
    # Проверка на существующий email
    if any(u.email == user_data.email for u in db):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Создаем нового пользователя
    new_id = max(u.id for u in db) + 1 if db else 1
    new_user = User(id=new_id, **user_data.dict())
    db.append(new_user)
    return new_user

@app.delete("/api/v1/user/{user_id}", status_code=status.HTTP_200_OK)
def delete_user(user_id: int):
    """Удаление пользователя по ID"""
    global db
    user = next((u for u in db if u.id == user_id), None)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    db = [u for u in db if u.id != user_id]
    return {"message": "User deleted successfully"}