from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import firebase_admin
from firebase_admin import credentials
from app.api.v1 import health, users

load_dotenv()

# Initialize Firebase Admin SDK
try:
    cred = credentials.Certificate("firebase-service-account.json")
    firebase_admin.initialize_app(cred)
except (ValueError, FileNotFoundError):
    print("WARNING: 'firebase-service-account.json' not found or invalid. Firebase Admin SDK not initialized.")

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="/api/v1")
app.include_router(users.router, prefix="/api/v1")

@app.on_event("startup")
def startup_db_client():
    app.mongodb_client = MongoClient(os.getenv("DATABASE_URL"))
    app.database = app.mongodb_client.get_database("chatgto")
    print("Connected to the MongoDB database!")

@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()

@app.get("/")
def read_root():
    return {"Hello": "World"}