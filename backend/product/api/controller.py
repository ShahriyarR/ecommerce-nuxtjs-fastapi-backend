from fastapi import APIRouter, Depends, UploadFile, File, Body, Form
from ..schemas import CategoryInDB, CategoryCreate, ProductCreate, ProductInDB
from backend.users import check_if_user_is_admin
from backend.app.helpers import handle_file_upload
from typing import Optional

router = APIRouter()


@router.post(
    "/category/create",
    tags=["create category"],
    description="Create new category",
    response_model=CategoryInDB,
    dependencies=[Depends(check_if_user_is_admin)]
)
async def category_create(category: CategoryCreate) -> CategoryInDB:
    from ..crud import create_category

    return await create_category(category)


@router.post(
    "/product/create",
    tags=["create product"],
    description="Create new product",
    response_model=ProductInDB,
    dependencies=[Depends(check_if_user_is_admin)]
)
async def product_create(category: int = Form(...),
                         name: str = Form(...),
                         slug: str = Form(...),
                         price: float = Form(...),
                         description: str = Form(...),
                         image: UploadFile = File(...)
                         ) -> ProductInDB:
    product = ProductCreate(category=category,
                            name=name,
                            slug=slug,
                            price=price,
                            description=description)
    product.image = await handle_file_upload(image)
    # here we put id=10 manually for test purposes originally it should came from database
    return ProductInDB(id=10, **product.dict())