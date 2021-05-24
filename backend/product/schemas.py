from backend.app.schemas import CoreModel, IDModelMixin


class CategoryCreate(CoreModel):
    name: str
    slug: str


class CategoryInDB(CategoryCreate, IDModelMixin):
    pass
