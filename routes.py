import json

from fastapi import FastAPI, Request, Body
from fastapi.middleware.cors import CORSMiddleware

from app.services import Users
from database import UsersDatabase

app  = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/v1/healthcheck")
def health_check():
    return {"status": "ok"}

@app.post("/api/v1/webhook")
async def webhook_test(body: dict = Body(...)):
    print(body)
    return body

@app.get("/api/v1/users")
async def get_users():
    return {"user_info": Users().get_all_user()}

@app.get("/api/v1/sync/users")
async def user_sync():
    monday_users = Users().get_all_user()

    for user in monday_users:
        UsersDatabase().create(
            id=user["id"],
            user_name=user["name"],
            monday_name=user["name"],
            monday_id=user["id"],
            role="U",
        )
        

    return {"status": "user sync complete"}