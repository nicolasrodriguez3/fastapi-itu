from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.exceptions import BadRequest
from app.schemas import RegisterUser, LoginUser, TokenResponse
from app.controller import AuthController

router = APIRouter(prefix="/auth")
controller = AuthController()


@router.post(
    "/register",
    status_code=201,
    responses={
        201: {"description": "Ok"},
        400: {"description": BadRequest.description}
    }
)
async def register(new_user: RegisterUser) -> TokenResponse:
    return controller.register(new_user)

@router.post(
    "/login",
    responses={
        200: {"description": "Ok"},
        400: {"description": BadRequest.description}
    }
)
async def login(credentials: OAuth2PasswordRequestForm = Depends()) -> TokenResponse:
    return controller.login(credentials)

