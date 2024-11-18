from typing import Annotated, List
from fastapi import APIRouter, Path, Query

from app.schemas import NewUserRequest, UserRequest, UserResponse
from app.controller import UsersController

router = APIRouter(prefix="/users")
controller = UsersController()


@router.post(
    "/",
    status_code=201,
    responses={
        201: {"description": "Usuario creado"},
    },
    description="Crea un nuevo usuario con los campos pasados por Body Param. Falla si faltan algunos de los campos obligatorios.",
)
async def create(new_claim: NewUserRequest) -> UserResponse:
    return controller.create(new_claim)


@router.get(
    "/",
    status_code=200,
    responses={
        200: {
            "description": "Get all users",
        }
    },
    description="Retorna una lista paginada con los usuarios del usuario. Si no hay proyectos para mostrar, retorna lista vacía.",
)
async def get_list(
    limit: Annotated[int, Query(ge=1, le=100)] = 10,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> List[UserResponse]:
    return controller.get_list(limit, offset)


@router.get(
    "/{id}",
    status_code=200,
    description="Retorna un usuario según su ID.",
    responses={
        200: {"description": "Usuario"},
        404: {"description": "Usuario no encontrado"},
        422: {"description": "ID no es un entero válido"},
    },
)
async def get_by_id(id: Annotated[int, Path(ge=1)]) -> UserResponse:
    return controller.get_by_id(id)


@router.patch("/{id}", status_code=200)
async def update(id: int, updated_claim: UserRequest) -> UserResponse:
    return controller.update(id, updated_claim)


@router.delete(
    "/{id}",
    status_code=204,
    description="Elimina un usuario según su ID",
    responses={
        200: {"description": "Usuario eliminado"},
        404: {"description": "Usuario no encontrado"},
        422: {"description": "ID no es un entero válido"},
    },
)
async def delete(id: int) -> None:
    return None
