from typing import Annotated, List
from fastapi import APIRouter, Path, Query

from app.schemas import ClaimRequest, NewClaimRequest, ClaimResponse
from app.controller import ClaimsController

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
async def create(new_claim: NewClaimRequest) -> ClaimResponse:
    return controller.create(new_claim)


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
) -> List[ClaimResponse]:
    return controller.get_list(limit, offset)


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
async def get_by_id(id: Annotated[int, Path(ge=1)]) -> ClaimResponse:
    return controller.get_by_id(id)


@router.patch("/{id}", status_code=200)
async def update(id: int, updated_claim: ClaimRequest) -> ClaimResponse:
    return controller.update(id, updated_claim)


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
async def delete(id: int) -> None:
    return None
