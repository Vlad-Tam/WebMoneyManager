import uvicorn
from fastapi import FastAPI

from currency_service.src.infrastructure.api.v1.currency import router as currency_router

app = FastAPI()
app.include_router(currency_router)


if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)
