from typing import Annotated, List
from fastapi import APIRouter, Path, Query, Depends

from app.schemas import ClaimRequest, NewClaimRequest, ClaimResponse, DecodedJwt
from app.controller import ClaimsController
from app.exceptions import NotFound
from app.dependencies import has_permission
from app.enums import USER_ROLES

router = APIRouter(prefix="/claims")
controller = ClaimsController()


@router.post(
    "/",
    status_code=201,
    responses={
        201: {"description": "Reclamo creado"},
    },
    description="Crea un nuevo reclamo con los campos pasados por Body Param. Falla si faltan algunos de los campos obligatorios.",
)
async def create(
    new_claim: NewClaimRequest,
    token: DecodedJwt = Depends(has_permission(USER_ROLES)),
) -> ClaimResponse:
    return controller.create(new_claim, token.user_id)


@router.get(
    "/",
    status_code=200,
    responses={
        200: {
            "description": "Get all claims",
        }
    },
    description="Retorna una lista paginada con los reclamos del usuario. Si no hay proyectos para mostrar, retorna lista vacía.",
)
async def get_list(
    limit: Annotated[int, Query(ge=1, le=100)] = 10,
    offset: Annotated[int, Query(ge=0)] = 0,
    token: DecodedJwt = Depends(has_permission(USER_ROLES)),
) -> List[ClaimResponse]:
    return controller.get_list(limit, offset, token.user_id)


@router.get(
    "/{id}",
    status_code=200,
    description="Retorna un reclamo según su ID.",
    responses={
        200: {"description": "Reclamo"},
        404: {"description": "Reclamo no encontrado"},
        422: {"description": "ID no es un entero válido"},
    },
)
async def get_by_id(
    id: Annotated[int, Path(ge=1)],
    token: DecodedJwt = Depends(has_permission(USER_ROLES)),
) -> ClaimResponse:
    return controller.get_by_id(id, token)


@router.patch("/{id}", status_code=200)
async def update(
    id: int,
    updated_claim: ClaimRequest,
    token: DecodedJwt = Depends(has_permission(USER_ROLES)),
) -> ClaimResponse:
    return controller.update(id, updated_claim, token)


@router.delete(
    "/{id}",
    status_code=204,
    description="Elimina un reclamo según su ID",
    responses={
        200: {"description": "Reclamo eliminado"},
        404: {"description": "Reclamo no encontrado"},
        422: {"description": "ID no es un entero válido"},
    },
)
async def delete(
    id: int,
    token: DecodedJwt = Depends(has_permission(USER_ROLES)),
) -> None:
    controller.delete(id, token)
