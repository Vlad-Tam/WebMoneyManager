from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import HTTPBasicCredentials, HTTPBasic

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

security = HTTPBasic()


@router.get("")
def basic_auth_credentials(
        credentials: Annotated[HTTPBasicCredentials, Depends(security)]
):
    return {
        "Username": credentials.username,
        "Password": credentials.password
    }
