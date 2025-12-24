from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI
from app.db import async_main
from app.routes import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await async_main()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router)

@app.get("/")
async def root():
    return {"message": "Hello World"}


if __name__ == "__main__":
    uvicorn.run(app)