from fastapi import FastAPI
from tasks import router

app = FastAPI()
app.include_router(router)


@app.get("/")
async def root():
    return {"message": "Welcome to Our Task Manager API"}
