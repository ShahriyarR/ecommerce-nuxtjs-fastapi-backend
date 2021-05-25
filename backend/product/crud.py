from .schemas import CategoryCreate, CategoryInDB, ProductCreate, ProductInDB
from .models import Category, Product


async def create_category(category: CategoryCreate) -> CategoryInDB:
    created_category = await Category.create(**category.dict())
    return CategoryInDB.from_orm(created_category)


async def create_product(product: ProductCreate) -> ProductInDB:
    created_product = await Product.create(**product.dict())
    return ProductInDB.from_orm(created_product)
