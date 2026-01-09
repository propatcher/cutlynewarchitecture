


from fastapi import APIRouter


router = APIRouter(
    prefix = "/links",
    tags=["Ссылки"]
)

@router.post("/shorten", response_model=LinkResponse)
async def shorten_url(
    url_data: CreateLinkRequest,
    current_user: User = Depends(get_current_user)
):
    """Создать короткую ссылку"""
    return await

async def new_user(user_data: UserRegisterRequest, user_service: UserService = Depends(get_user_service)) -> UserRegisterResponse:
@router.get("/{short_code}")
async def redirect_to_original(
    short_code: str,
    link_service: LinkService = Depends(get_link_service)
):
    """Редирект по короткому коду"""
    pass

@router.get("/", response_model=List[LinkResponse])
async def get_user_links(
    current_user: User = Depends(get_current_user)
):
    """Получить все ссылки пользователя"""
    pass