from db_users_controller import DB_Users_Controller
import alembic
from fastapi import *
import uvicorn

print("Starting_server...")
db_users_controller = DB_Users_Controller()
app = FastAPI()
uvicorn.run(app=app, host="localhost",port=8000)



@app.get("/")
async def root():
    print("ANSWER")
    return {"AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA":"NE AKAI MNE TUT"}

