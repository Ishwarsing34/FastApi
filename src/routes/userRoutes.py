import json
from pathlib import Path

from fastapi import APIRouter, HTTPException

from src.dtos.productSchema import UserCreate, UserMessage, UserResponse, UserUpdate

userRoutes = APIRouter()

FILE_PATH = Path("src/data/users.json")


def get_all_users():
    with open(FILE_PATH, "r") as file:
        return json.load(file)


def save_users(users):
    with open(FILE_PATH, "w") as file:
        json.dump(users, file)


@userRoutes.get("/", response_model=list[UserResponse])
def getUsers():
    users = get_all_users()
    return [{"name": user["name"], "email": user["email"]} for user in users]


@userRoutes.get("/{email}", response_model=UserResponse)
def getUserByEmail(email: str):
    users = get_all_users()
    for user in users:
        if user["email"] == email:
            return {"name": user["name"], "email": user["email"]}
    raise HTTPException(status_code=404, detail={"error": "user not found"})


@userRoutes.post("/", response_model=UserMessage)
def createUser(user: UserCreate):
    users = get_all_users()

    for existing_user in users:
        if existing_user["email"] == user.email:
            raise HTTPException(status_code=400, detail={"error": "email already exists"})

    new_user = {
        "name": user.name,
        "email": user.email,
        "password": user.password,
    }
    users.append(new_user)
    save_users(users)
    return {
        "message": "user created successfully",
        "user": {"name": new_user["name"], "email": new_user["email"]}
    }


@userRoutes.put("/{email}", response_model=UserMessage)
def updateUser(email: str, user: UserUpdate):
    users = get_all_users()

    for existing_user in users:
        if existing_user["email"] == email:
            update_data = user.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                if value is not None:
                    existing_user[key] = value
            save_users(users)
            return {
                "message": "user updated successfully",
                "user": {"name": existing_user["name"], "email": existing_user["email"]}
            }

    raise HTTPException(status_code=404, detail={"error": "user not found"})


@userRoutes.delete("/{email}", response_model=UserMessage)
def deleteUser(email: str):
    users = get_all_users()

    for index, user in enumerate(users):
        if user["email"] == email:
            deleted_user = users.pop(index)
            save_users(users)
            return {
                "message": "user deleted successfully",
                "user": {"name": deleted_user["name"], "email": deleted_user["email"]}
            }

    raise HTTPException(status_code=404, detail={"error": "user not found"})
