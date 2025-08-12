from fastapi import APIRouter, Depends, HTTPException, Request
from app.models.user import User

router = APIRouter()

@router.post("/users", status_code=201)
def create_user(user: User, request: Request):
    user_dict = user.dict()
    try:
        request.app.database["users"].insert_one(user_dict)
        return {"message": "User created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))