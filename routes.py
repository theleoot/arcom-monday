import json

from fastapi import FastAPI, Request, Body
from fastapi.middleware.cors import CORSMiddleware

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