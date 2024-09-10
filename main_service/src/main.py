import uvicorn
from fastapi import FastAPI

from main_service.src.infrastructure.api.api_v1.auth import router as security_router
from main_service.src.infrastructure.api.api_v1.categories import router as categories_router
from main_service.src.infrastructure.api.api_v1.home import router as home_router
from main_service.src.infrastructure.api.api_v1.transactions import router as transactions_router
from main_service.src.infrastructure.api.api_v1.currency import router as currency_router


app = FastAPI()
app.include_router(home_router)
app.include_router(categories_router)
app.include_router(transactions_router)
app.include_router(security_router)
app.include_router(currency_router)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
