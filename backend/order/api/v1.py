from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def get_order():
    return "order app created!"
