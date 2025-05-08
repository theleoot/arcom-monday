import os
import json
import datetime

from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware

from app.services.monday.items import Items

from database import UsersDatabase, CustomersDatabase

from app.services import Users
from app.services.get_board_data import MondayDashboardData


# Initialize FastAPI app
app = FastAPI()

# Middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Monday API token and dashboard data
MONDAY_API_KEY = os.getenv("MONDAY_API_KEY")
dashboard_data = MondayDashboardData(token=MONDAY_API_KEY)


# Healthcheck route
@app.get("/api/v1/healthcheck")
def health_check():
    return {"status": "ok"}


# Webhook route
@app.post("/api/v1/webhook")
async def webhook_test(body: dict = Body(...)):
    print(body)
    return body


# User-related routes
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


# Board-related routes
@app.get("/api/v1/board/get")
def get_board_data():
    return dashboard_data.get_board("8895172562", "topics")


@app.get("/api/v1/item/get/{board_id}")
def get_item_by_board_id(board_id: str):
    return dashboard_data.get_item(board_id)


@app.get("/api/v1/board/{board_id}/column/{column_id}/value/{value}")
def get_item_by_column_value(board_id: str, column_id: str, value: str):
    return dashboard_data.items.fetch_items_by_column_value(board_id, column_id, value)


@app.get("/api/v1/board/{board_id}/items/{column_id}/search/{search_value}")
def get_items_by_column(board_id: str, column_id: str, search_value: str):
    return Items(
        token=MONDAY_API_KEY, board_id=board_id, column_id=column_id
    ).get_column(search_value)


@app.get("/api/v1/columms")
def change_column_value(board_id: str, item_id: str, column_id: str, value: str):
    return dashboard_data.items.change_item_value(
        board_id, item_id, column_id, value
    )


# Customer-related routes
@app.post("/api/v1/customer")
def customer_create():
    return CustomersDatabase().create(
        id="9102499374",
        ramo_atividade="Test",
        board_id="8895172235",
        group_id="group_mkqrdxnr",
        data_sincronizacao_fonte=datetime.datetime.now().isoformat(" ", "seconds"),
        data_atualizacao_monday=datetime.datetime.now().isoformat(" ", "seconds"),
        codigo_cliente="111211",
        deleted=0,
        item_name="Test",
        codigo_rede=1,
        codigo_associacao=None,
        nome_associacao="Test Association",
    )

@app.get("/api/v1/customer/")
def get_customer_by_id(value: str):
    return CustomersDatabase().get_one(value)

@app.get("/api/v1/customers/update")
def customers_to_update():
    customers_fetch = list(CustomersDatabase().customers_to_update())

    for customer in customers_fetch:
        item_fetch = Items(token=os.getenv("MONDAY_API_KEY"),
                           board_id=customer["board_id"], 
                           column_id="numeric_mkqfswdp").get_by_id(customer["id"])
        
        return item_fetch

