import enum
import uuid


class Environment(enum.Enum):
    DEVELOPMENT = "DEVELOPMENT"
    PRODUCTION = "PRODUCTION"
    TEST = "TEST"


class Severity(enum.Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class Priority(enum.Enum):
    HIGH = "Высокий"
    MEDIUM = "Средний"
    LOW = "Низкий"


class Status(enum.Enum):
    NEW = "NEW"
    IN_PROGRESS = "IN_PROGRESS"
    HOLD = "HOLD"
    CLOSED = "CLOSED"
    REJECTED = "REJECTED"
    REVIEW = "REVIEW"
    DONE = "DONE"


class ItemType(enum.Enum):
    EPIC = "EPIC"
    USER_STORY = "USER_STORY"
    USE_CASE = "USE_CASE"
    TASK = "TASK"
    BUG = "BUG"


class UserRole(enum.Enum):
    ADMIN = "Администратор"
    DELIVERY_MANAGER = "Деливери-менеджер"

    # Участники проекта
    ANALYST = "Участник проекта - Аналитик"
    UX_ANALYST = "Участник проекта - Аналитик UX"
    ARCHITECT = "Участник проекта - Архитектор"
    BACKEND_DEV = "Участник проекта - Разработчик backend"
    FRONTEND_DEV = "Участник проекта - Разработчик frontend"
    DESIGNER = "Участник проекта - Дизайнер"
    QA_ENGINEER = "Участник проекта - Тестировщик"
    DEVOPS_ENGINEER = "Участник проекта - Инженер DevOps"

    @classmethod
    def get_project_members(cls):
        """Возвращает только роли участников проекта"""
        return [
            cls.ANALYST,
            cls.UX_ANALYST,
            cls.ARCHITECT,
            cls.BACKEND_DEV,
            cls.FRONTEND_DEV,
            cls.DESIGNER,
            cls.QA_ENGINEER,
            cls.DEVOPS_ENGINEER,
        ]

DSTRACKER_API = "http://localhost:9000/api/v1"
