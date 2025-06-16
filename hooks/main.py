import argparse
import asyncio
import json
import uuid
from http import HTTPStatus
import logging

import consts
import dtos
import http_client
import interfaces

logger = logging.getLogger(__name__)


def _read_files(file_paths: list[str]) -> list[dtos.FileContentDTO]:
    """
    Прочитать содержимое файлов
    :param file_paths: пути файлов
    :return: список информации по файлам
    """

    contents = []

    for path in file_paths:
        if not path.strip():
            continue
        try:
            with open(path, "rb") as f:
                contents.append(
                    dtos.FileContentDTO(
                        path=path,
                        content=json.loads(f.read())
                    )
                )
        except Exception as e:
            logger.error(f"Ошибка при чтении {path}: {e}")

    return contents


async def _create_us(
    client: interfaces.IClient,
    files: list[dtos.FileContentDTO],
    token: str,
    user_id: uuid.UUID
) -> list[str]:
    """
    Создать US в DsTracker на основе переданных данных
    :param client: HTTP-клиент
    :param files: данные о файлах
    :param token: токен DSTracker
    :return: список созданных US
    """

    to_create: dict[uuid.UUID, dtos.UserStoryCreate] = {}
    created = []

    for file in files:
        try:
            us = dtos.UserStoryCreate(
                id=file.content["id"],
                role=file.content["task_role"],
                action=file.content["action"],
                goal=file.content["goal"],
                acceptance_criteria=file.content["acceptance_criteria"],
                functional_requirements=file.content.get("functional_requirements"),
                non_functional_requirements=file.content.get("non_functional_requirements"),
                title=file.content["title"],
                description=file.content.get("description"),
                creator_id=user_id,
                updated_by_id=user_id
            )

            if priority := file.content.get("priority"):
                us.priority = consts.Priority(priority)

            to_create[us.id] = us
        except Exception as e:
            logger.error(f"Ошибка при чтении файла {e}")

    for us in to_create.values():
        try:
            response = await http_client.create_us(client, us, token)

            if response.status == HTTPStatus.OK:
                created.append(us.title)
        except Exception as e:
            logger.error(e)
            continue

    return created


async def _get_access_token(client: interfaces.IClient, creds: dtos.UserCreds) -> str:
    """
    Получить access-токен для переданных кредов
    :param client: HTTP-клиент
    :param creds: креды пользователя
    :return: access-токен
    """

    response = await http_client.get_token(client, creds)

    if response.status != HTTPStatus.OK:
        raise ConnectionError("Не удалось получить токен")

    return response.payload["access_token"]


async def main():
    http_client_ = http_client.HTTPClient()

    parser = argparse.ArgumentParser()
    parser.add_argument("--username", help="Имя пользователя DSTracker")
    parser.add_argument("--password", help="Пароль пользователя DSTracker")
    parser.add_argument("--id", help="Идентификатор пользователя DSTracker")
    parser.add_argument("--new", help="Новые файлы", default="")
    parser.add_argument("--modified", help="Обновленные файлы", default="")

    try:
        args = parser.parse_args()

        username = args.username
        password = args.password
        id_ = uuid.UUID(args.id)
        user_creds = dtos.UserCreds(
            username=username,
            password=password
        )

        token = await _get_access_token(http_client_, user_creds)

        new_files = args.new.split() if args.new else []
        modified_files = args.modified.split() if args.modified else []

        logger.info("Получение access-токена...")

        logger.info("Чтение новых файлов...")

        new_contents = _read_files(new_files)
        new_us = []

        for file_info in new_contents:
            if file_info.path.split("/")[-1].startswith("us"):
                new_us.append(file_info)

                print(f"Добавлен новый US {file_info.path}")

        print(Чтение измененных файлов...")

        modified_contents = _read_files(modified_files)
        modified_us = []

        for file_info in modified_contents:
            if file_info.path.split("/")[-1].startswith("US"):
                modified_us.append(file_info)

                print(f"Добавлен измененный US {file_info.path}")

        await _create_us(http_client_, new_us, token, id_)

        print(f"Созданы US в DSTracker")
    finally:
        await http_client_.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
