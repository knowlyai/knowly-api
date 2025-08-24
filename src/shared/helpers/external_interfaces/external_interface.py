from abc import ABC, abstractmethod
from typing import TypeVar, Generic

RequestDataType = TypeVar('RequestDataType')
ResponseDataType = TypeVar('ResponseDataType')


class IRequest(ABC, Generic[RequestDataType]):

    @property
    @abstractmethod
    def data(self) -> RequestDataType:
        pass


class IResponse(ABC, Generic[ResponseDataType]):

    @property
    @abstractmethod
    def status_code(self) -> int:
        pass

    @property
    @abstractmethod
    def data(self) -> ResponseDataType:
        pass
