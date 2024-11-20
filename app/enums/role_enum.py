from enum import Enum
from typing import List


class RoleEnum(str, Enum):
    USER = "user"
    EMPLOYEE = "employee"
    BOSS = "boss"
    ADMIN = "admin"


# Listas de roles
USER_ROLES: List[RoleEnum] = [
    RoleEnum.USER,
    RoleEnum.EMPLOYEE,
    RoleEnum.BOSS,
    RoleEnum.ADMIN,
]

EMPLOYEE_ROLES: List[RoleEnum] = [
    RoleEnum.EMPLOYEE,
    RoleEnum.BOSS,
    RoleEnum.ADMIN,
]
BOSS_ROLES: List[RoleEnum] = [
    RoleEnum.BOSS,
    RoleEnum.ADMIN,
]
ADMIN_ROLES: List[RoleEnum] = [
    RoleEnum.ADMIN,
]
