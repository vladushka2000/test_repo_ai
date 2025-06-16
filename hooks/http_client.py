from typing import Iterable

import httpx

import consts
import dtos
import interfaces


class HTTPClient(interfaces.IClient):
    """
    Клиент для HTTP-запросов
    """

    def __init__(self) -> None:
        """
        Инициализировать переменны
        """

        self._client = httpx.AsyncClient(timeout=None)

    def connect(self) -> None:
        """
        Установить соединение
        """

        pass

    async def disconnect(self) -> None:
        """
        Разорвать соединение
        """

        await self._client.aclose()

    async def create(self, request_params: dtos.HTTPRequestDTO) -> dtos.HTTPResponseDTO:
        """
        Сделать POST-запрос
        :param request_params: параметры запроса
        :return: результаты запроса
        """
        try:
            response = await self._client.post(
                url=request_params.url,
                headers=request_params.headers,
                params=request_params.query_params,
                json=request_params.payload,
                data=request_params.form_data,
            )
    
            try:
                payload = response.json()
            except Exception:
                payload = response
    
            return dtos.HTTPResponseDTO(
                status=response.status_code,
                headers=response.headers,
                payload=payload
            )
        except:
            print("Ошибочка")

    async def retrieve(self, request_params: dtos.HTTPRequestDTO) -> dtos.HTTPResponseDTO:
        """
        Сделать GET-запрос
        :param request_params: параметры запроса
        :return: результаты запроса
        """

        response = await self._client.get(
            url=request_params.url,
            headers=request_params.headers,
            params=request_params.query_params
        )

        return dtos.HTTPResponseDTO(
            status=response.status_code,
            headers=response.headers,
            payload=response.json()
        )

    async def list(self, *args, **kwargs) -> Iterable[any]:
        """
        Получить список записей
        """

        return super().list(*args, **kwargs)

    async def update(self, *args, **kwargs) -> httpx.Response:
        """
        Сделать PATCH-запрос
        """

        return super().update(*args, **kwargs)

    async def delete(self, *args, **kwargs) -> httpx.Response:
        """
        Сделать DELETE-запрос
        """

        return super().delete(*args, **kwargs)


async def create_us(client: interfaces.IClient, us: dtos.UserStoryCreate, token: str) -> dtos.HTTPResponseDTO:
    """
    Создать US
    :param client: HTTP-клиент
    :param us: данные US
    :param token: токен от API DSTracker
    :return: ответ сервера
    """

    try:
        request = dtos.HTTPRequestDTO(
            url=f"{consts.DSTRACKER_API}/user-stories/",
            payload=us.model_dump(mode="json"),
            headers={
                "Authorization": f"Bearer {token}"
            }
        )
    except:
        print("Тут ошибка")

    return await client.create(request)


async def get_token(client: interfaces.IClient, creds: dtos.UserCreds) -> dtos.HTTPResponseDTO:
    """
    Получить токен DSTracker
    :param client: HTTP-клиент
    :param creds: креды пользователя
    :return: ответ сервера
    """

    request = dtos.HTTPRequestDTO(
        url=f"{consts.DSTRACKER_API}/auth/sign-in",
        form_data={
            "username": creds.username,
            "password": creds.password
        }
    )

    return await client.create(request)
