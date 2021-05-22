from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def get_product():
    return "product app created!"
