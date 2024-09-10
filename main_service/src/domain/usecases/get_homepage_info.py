from typing import Optional, Union

from main_service.src.domain.entities.request import RequestModel
from main_service.src.domain.entities.response import ResponseModel, ResponseSuccess, ResponseFailure, ResponseStatus
from main_service.src.domain.interfaces.usecase import IUseCase
from main_service.src.infrastructure.config.logging_config import logging_config
from main_service.src.infrastructure.repositories.home_repo import HomeRepository


class GetHomepageInfo(IUseCase):

    def __init__(self):
        self.db_repository = HomeRepository()
        self.logger = logging_config.get_logger()

    class Request(RequestModel):
        user_id: int
        time_period: Optional[str] = "month"

    class Response(ResponseModel):
        response: Union[ResponseSuccess, ResponseFailure]

        class Config:
            arbitrary_types_allowed = True

        def __init__(self, response: Union[ResponseSuccess, ResponseFailure]):
            super().__init__(response=response)

    async def execute(self, request: Request):
        self.logger.debug(f"Method '{self.__class__.__name__}.execute' was called")
        try:
            db_data = await self.db_repository.get_homepage_info(request.user_id, request.time_period)
        except Exception as e:
            self.logger.error(f"Class '{self.__class__.__name__}' raised an exception \"{e}\"")
            return self.Response(ResponseFailure(status=ResponseStatus.NOT_FOUND, details="Getting result error"))

        try:
            warnings = []
            last_spending = (
                {
                    "value": db_data["last_spending_value"],
                    "description": db_data["last_spending_description"],
                    "time": db_data["last_spending_time"],
                }
                if db_data["last_spending_value"] is not None
                   or db_data["last_spending_time"] is not None
                else None
            )

            current_sub = 0 if db_data["current_sub"] is None else db_data["current_sub"]
            current_balance = (
                0 if db_data["current_balance"] is None else db_data["current_balance"]
            )

            if current_balance < 0:
                warnings.append("Balance is negative")

            if db_data["month_limit"] is not None:
                if db_data["current_month_sub"] > db_data["month_limit"]:
                    warnings.append("Monthly limit exceeded")
        except Exception as e:
            self.logger.error(f"Class '{self.__class__.__name__}' raised an exception \"{e}\"")
            return self.Response(
                ResponseFailure(
                    status=ResponseStatus.INTERNAL_ERROR,
                    details="Processing result error"
                )
            )

        self.logger.info(f"Method '{self.__class__.__name__}.execute' worked successfully")
        return self.Response(
            ResponseSuccess(
                data={
                    "name": db_data["name"],
                    "surname": db_data["surname"],
                    "email": db_data["email"],
                    "main_currency": db_data["main_currency"],
                    "month_limit": db_data["month_limit"],
                    "birth_date": db_data["birth_date"],
                    "current_sub": current_sub,
                    "current_balance": current_balance,
                    "last_spending": last_spending,
                    "warnings": warnings,
                },
                status=ResponseStatus.SUCCESS
            )
        )
