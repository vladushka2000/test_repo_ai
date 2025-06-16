import dataclasses
import datetime
import uuid

from pydantic import BaseModel, Field

import consts


class HTTPRequestDTO(BaseModel):
    """
    DTO, содержащий информацию для HTTP-запроса
    """

    url: str = Field(description="URL запроса")
    headers: dict | None = Field(description="Заголовки", default=None)
    query_params: dict | None = Field(description="Параметры запроса", default=None)
    payload: dict | list | None = Field(description="Body запроса", default=None)
    form_data: dict | None = Field(description="Данные из html-формы", default=None)


class HTTPResponseDTO(BaseModel):
    """
    DTO, содержащий информацию ответа HTTP-запроса
    """

    status: int = Field(description="Статус ответа")
    headers: dict | None = Field(description="Заголовки", default=None)
    payload: dict | list[dict] | None = Field(description="Body ответа", default=None)


@dataclasses.dataclass
class FileContentDTO:
    """
    DTO, содержащий информацию о файле
    """

    path: str
    content: dict


class TrackableItemBase(BaseModel):
    id: uuid.UUID | None = Field(title="Идентификатор элемента", default=uuid.uuid4())
    title: str = Field(title="Наименование элемента")
    description: str | None = Field(title="Описание элемента", default=None)
    priority: consts.Priority = Field(title="Приоритет элемента", default=consts.Priority.MEDIUM)
    status: consts.Status = Field(title="Статус элемента", default=consts.Status.NEW)
    story_point: int | None = Field(title="Стори поинты", default=None)
    creator_id: uuid.UUID = Field(title="Идентификатор создателя")
    updated_by_id: uuid.UUID | None = Field(
        title="Идентификатор пользователя, обновившего элемент"
    )
    assignee_id: uuid.UUID | None = Field(
        title="Идентификатор исполнителя", default=None
    )
    parent_id: uuid.UUID | None = Field(
        title="Идентификатор родителя элемента", default=None
    )

    model_config = {"from_attributes": True}


class TrackableItemUpdate(BaseModel):
    title: str | None = Field(title="Наименование элемента", default=None)
    description: str | None = Field(title="Описание элемента", default=None)
    priority: consts.Priority | None = Field(
        title="Приоритет элемента", default=consts.Priority.MEDIUM
    )
    status: consts.Status | None = Field(title="Статус элемента", default=consts.Status.NEW)
    assignee_id: uuid.UUID | None = Field(
        title="Идентификатор исполнителя", default=None
    )
    parent_id: uuid.UUID | None = Field(
        title="Идентификатор родителя элемента", default=None
    )


class TrackableItem(TrackableItemBase):
    type: consts.ItemType = Field(title="Тип элемента (Эпик, Задача и т.д)")
    created_at: datetime.datetime = Field(title="Время создания элемента")
    updated_at: datetime.datetime | None = Field(title="Время обновления элемента")


class UserStoryBase(BaseModel):
    role: consts.UserRole = Field(title="Роль")
    action: str = Field(title="Действие")
    goal: str = Field(title="Цель")
    acceptance_criteria: str = Field(title="Критерии приемки")
    functional_requirements: str | None = Field(title="ФТ", default=None)
    non_functional_requirements: str | None = Field(title="НФТ", default=None)


class UserStoryCreate(UserStoryBase, TrackableItemBase):
    pass


class UserStory(UserStoryBase, TrackableItem):
    pass


class UserStoryUpdate(UserStoryBase, TrackableItemUpdate):
    pass


@dataclasses.dataclass
class UserCreds:
    """
    DTO кредов пользователя
    """

    username: str
    password: str
    token: str | None = None
