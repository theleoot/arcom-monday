import os
import uvicorn
import nest_asyncio
from pyngrok import ngrok
from dotenv import load_dotenv

from routes import app
from database import con

load_dotenv()
nest_asyncio.apply()


try:
    if int(os.getenv("USE_TUNNELING")):
        print("Here")
        public_url = ngrok.connect(int(os.getenv("PORT")), url=os.getenv("NGROK_URL"))
        print(f"Public URL: {public_url}")

    uvicorn.run(app, host=os.getenv("HOST"), port=int(os.getenv("PORT")))
except KeyboardInterrupt:
    print("Exiting...")
    con.close()
    print("Application Finished With Success!")
    exit(0)
