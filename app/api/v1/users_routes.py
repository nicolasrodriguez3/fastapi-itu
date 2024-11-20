from typing import Annotated, List
from fastapi import APIRouter, Path, Query, Depends

from app.exceptions import NotFound, Unauthorized, Forbidden
from app.schemas import NewUserRequest, UserRequest, UserResponse, DecodedJwt
from app.controller import UsersController
from app.dependencies import has_permission
from app.enums import ADMIN_ROLES, USER_ROLES

router = APIRouter(prefix="/users")
controller = UsersController()


@router.post(
    "/",
    status_code=201,
    responses={
        201: {"description": "Usuario creado"},
        401: Unauthorized.as_dict(),
        403: Forbidden.as_dict(),
    },
    description="Crea un nuevo usuario con los campos pasados por Body Param. Falla si faltan algunos de los campos obligatorios.",
)
async def create(
    new_claim: NewUserRequest,
    _: DecodedJwt = Depends(has_permission(ADMIN_ROLES)),
) -> UserResponse:
    return controller.create(new_claim)


@router.get(
    "/",
    status_code=200,
    responses={
        200: {
            "description": "Ontener lista paginada de usuarios",
        },
        401: Unauthorized.as_dict(),
        403: Forbidden.as_dict(),
        404: NotFound.as_dict(),
        422: {"description": "ID no es un entero valido"},
    },
    description="Retorna una lista paginada con los usuarios del usuario. Si no hay proyectos para mostrar, retorna lista vacía.",
)
async def get_list(
    limit: Annotated[int, Query(ge=1, le=100)] = 10,
    offset: Annotated[int, Query(ge=0)] = 0,
    _: DecodedJwt = Depends(has_permission(ADMIN_ROLES)),
) -> List[UserResponse]:
    return controller.get_list(limit, offset)


@router.get(
    "/me",
    status_code=200,
    description="Retorna información del usuario logueado.",
    responses={
        200: {"description": "Usuario"},
        401: Unauthorized.as_dict(),
    },
)
async def get_logged_user(
    token: DecodedJwt = Depends(has_permission(USER_ROLES)),
) -> UserResponse:
    token_dict: dict = token.model_dump()
    return controller.get_by_id(token_dict["user_id"])


@router.get(
    "/{id}",
    status_code=200,
    description="Retorna un usuario según su ID.",
    responses={
        200: {"description": "Usuario"},
        401: Unauthorized.as_dict(),
        403: Forbidden.as_dict(),
        404: NotFound.as_dict(),
        422: {"description": "ID no es un entero válido"},
    },
)
async def get_by_id(
    id: Annotated[int, Path(ge=1)],
    _: DecodedJwt = Depends(has_permission(ADMIN_ROLES)),
) -> UserResponse:
    return controller.get_by_id(id)


@router.patch(
    "/{id}",
    status_code=200,
    description="Actualiza un usuario segun su ID. Falla si faltan algunos de los campos obligatorios.",
    responses={
        200: {"description": "Usuario actualizado"},
        401: Unauthorized.as_dict(),
        403: Forbidden.as_dict(),
        404: NotFound.as_dict(),
        422: {"description": "ID no es un entero valido"},
    },
)
async def update(
    id: Annotated[int, Path(ge=1)],
    updated_claim: UserRequest,
    _: DecodedJwt = Depends(has_permission(ADMIN_ROLES)),
) -> UserResponse:
    return controller.update(id, updated_claim)


@router.delete(
    "/{id}",
    status_code=204,
    description="Elimina un usuario según su ID",
    responses={
        204: {"description": "Usuario eliminado"},
        401: Unauthorized.as_dict(),
        403: Forbidden.as_dict(),
        404: NotFound.as_dict(),
        422: {"description": "ID no es un entero válido"},
    },
)
async def delete(
    id: Annotated[int, Path(ge=1)],
    _: DecodedJwt = Depends(has_permission(ADMIN_ROLES)),
) -> None:
    return controller.delete(id)
