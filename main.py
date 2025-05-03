import os
import uvicorn
import nest_asyncio
from pyngrok import ngrok
from dotenv import load_dotenv

from routes import app
from database import Users, cur, con

load_dotenv()

if __name__ == "__main__":
    try:
        print(Users("").some())
        print(cur.execute("SELECT * FROM users").fetchall())
    except KeyboardInterrupt:
        print("Exiting...")
        con.close()
        print("Application Finished With Success!")
        exit(0)


"""
nest_asyncio.apply()

ngrok.set_auth_token(os.getenv("AUTH_TOKEN"))

public_url = ngrok.connect(int(os.getenv("PORT")), url=os.getenv("NGROK_URL"))
print(f"Public URL: {public_url}")

uvicorn.run(app, host=os.getenv("HOST"), port=int(os.getenv("PORT")))
"""