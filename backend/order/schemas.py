from backend.app.schemas import CoreModel, IDModelMixin, DateTimeModelMixin
from pydantic import EmailStr


class OrderCreate(CoreModel, DateTimeModelMixin):
    first_name: str
    last_name: str
    email: EmailStr
    address: str
    zipcode: str
    phone: str
    place: str


class OrderInDB(OrderCreate, IDModelMixin):

    class Config:
        orm_mode = True


class OrderItemCreate(CoreModel):
    price: float
    product: int
    quantity: int


class OrderItemInDB(OrderItemCreate, IDModelMixin):

    class Config:
        orm_mode = True
