from pydantic import BaseModel, EmailStr

class User(BaseModel):
    firebase_uid: str
    email: EmailStr