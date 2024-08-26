from abc import ABC, abstractmethod

from currency_service.src.domain.entities.request import RequestModel


class IUseCase(ABC):
    @abstractmethod
    async def execute(self, request: RequestModel):
        pass
    