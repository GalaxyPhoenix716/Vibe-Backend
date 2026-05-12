from fastapi import FastAPI
from sqlmodel import SQLModel
from db.database import engine
from routes.auth_routes import router as auth_router

app = FastAPI()
app.include_router(auth_router)

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)