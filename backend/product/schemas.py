import json
from backend.app.schemas import CoreModel, IDModelMixin, DateTimeModelMixin
from typing import Optional


class CategoryCreate(CoreModel):
    name: str
    slug: str


class CategoryInDB(CategoryCreate, IDModelMixin):

    class Config:
        orm_mode = True


class ProductCreate(CoreModel, DateTimeModelMixin):
    category: int
    name: str
    slug: str
    description: Optional[str]
    price: float
    image: Optional[str]
    thumbnail: Optional[str]


class ProductInDB(ProductCreate, IDModelMixin):

    class Config:
        orm_mode = True
