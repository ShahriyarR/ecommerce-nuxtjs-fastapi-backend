from fastapi import APIRouter, Depends
from ..schemas import CategoryInDB, CategoryCreate
from backend.users import auth_service

router = APIRouter()


@router.post(
    "/create",
    tags=["create category"],
    description="Create new category",
    response_model=CategoryInDB,
    # dependencies=[Depends(auth_service.check_if_user_is_admin)]
)
async def category_create(category: CategoryCreate) -> CategoryInDB:
    from ..crud import create_category

    return await create_category(category)
