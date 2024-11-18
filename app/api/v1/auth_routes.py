from fastapi import APIRouter
from fastapi.security import OAuth2PasswordRequestForm

from app.exceptions import BadRequest
from app.schemas import RegisterUser, LoginUser, TokenResponse

router = APIRouter(prefix="/users")
# controller = AuthController()


@router.post(
    "/register",
    status_code=201,
    responses={
        201: {"description": "Ok"},
        400: {"description": BadRequest.description}
    }
)
async def register(new_user: RegisterUser) -> TokenResponse:
    return

@router.post(
    "/login",
    responses={
        200: {"description": "Ok"},
        400: {"description": BadRequest.description}
    }
)
async def login(credentials: OAuth2PasswordRequestForm) -> TokenResponse:
    return

