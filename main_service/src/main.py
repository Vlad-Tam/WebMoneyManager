import uvicorn
from fastapi import FastAPI

from main_service.src.home.router import router as home_router
from main_service.src.categories.router import router as categories_router
from main_service.src.transactions.router import router as transactions_router
from main_service.src.auth.router import router as auth_router

app = FastAPI()
app.include_router(home_router)
app.include_router(categories_router)
app.include_router(transactions_router)
app.include_router(auth_router)


if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)

