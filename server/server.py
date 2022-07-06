from db_users_controller import DB_Users_Controller
from fastapi import *
from fastapi.responses import FileResponse
import uvicorn

print("Starting_server...")
db_users_controller = DB_Users_Controller()
app = FastAPI()


@app.get("")
async def test():
    print(Request.base_url)

@app.get("/item")
async def root():
    # print("ANSWER")
    return FileResponse("tmp/database.db")


@app.middleware("http")
async def debug_request(request: Request, call_next):
    response = await call_next(request)
    print(Request.base_url)
    return response

uvicorn.run(app=app, host="localhost",port=9999)
