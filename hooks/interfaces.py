import abc
from typing import Iterable


class IClient(abc.ABC):
    """
    Интерфейс клиента
    """

    @abc.abstractmethod
    async def connect(self, *args, **kwargs) -> any:
        """
        Установить соединение с БД
        """

        raise NotImplementedError

    @abc.abstractmethod
    async def disconnect(self, *args, **kwargs) -> any:
        """
        Разорвать соединение с БД
        """

        raise NotImplementedError

    @abc.abstractmethod
    def create(self, *args, **kwargs) -> any:
        """
        Создать запись
        """

        raise NotImplementedError

    @abc.abstractmethod
    def retrieve(self, *args, **kwargs) -> any:
        """
        Получить запись
        """

        raise NotImplementedError

    @abc.abstractmethod
    def list(self, *args, **kwargs) -> Iterable[any]:
        """
        Получить список записей
        """

        raise NotImplementedError

    @abc.abstractmethod
    def update(self, *args, **kwargs) -> any:
        """
        Обновить запись
        """

        raise NotImplementedError

    @abc.abstractmethod
    def delete(self, *args, **kwargs) -> any:
        """
        Удалить запись
        """

        raise NotImplementedError
