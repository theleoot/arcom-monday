import os
import json

from fastapi import FastAPI, Request, Body
from fastapi.middleware.cors import CORSMiddleware

from app.services import Users
from database import UsersDatabase
from app.services.get_board_data import MondayDashboardData

dashboard_data = MondayDashboardData(token=os.getenv("MONDAY_API_KEY"))

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

@app.get("/api/v1/board/get")
def get_board_data():
    clients_board = MondayDashboardData(token=os.getenv("MONDAY_API_KEY")).get_board("8895172562", "topics")
    return clients_board

@app.get("/api/v1/item/get/{board_id}")
def get_item_by_board_id(board_id: str):
    items = MondayDashboardData(token=os.getenv("MONDAY_API_KEY")).get_item(board_id)
    return items

@app.get("/api/v1/board/{board_id}/column/{column_id}/value/{value}")
def get_item_by_column_value(board_id: str, column_id: str, value: str):
    items = dashboard_data.items.fetch_items_by_column_value(board_id, column_id, value)
    return items

@app.get("/api/v1/columms")
def change_column_value(board_id: str, item_id: str, column_id: str, value: str):
    items = dashboard_data.items.change_item_value("8895173426", "8895177827", "numeric_mkqeqgqd", "122000")
    return items
