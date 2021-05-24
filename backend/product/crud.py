from .schemas import CategoryCreate, CategoryInDB
from .models import Category


async def create_category(category: CategoryCreate) -> CategoryInDB:
    created_category = await Category.create(**category.dict())
    return CategoryInDB.from_orm(created_category)
