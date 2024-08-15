import uvicorn
from fastapi import FastAPI
from src.home.router import router as home_router
from src.categories.router import router as categories_router
from src.transactions.router import router as transactions_router

app = FastAPI()
app.include_router(home_router)
app.include_router(categories_router)
app.include_router(transactions_router)


if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)

