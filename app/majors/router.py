from fastapi import APIRouter
from app.majors.dao import MajorsDAO
from app.majors.schemas import SMajorsAdd


router = APIRouter(prefix='/majors', tags=['Работа с факультетами'])


@router.post("/add/")
async def register_user(major: SMajorsAdd) -> dict:
    check = await MajorsDAO.add(**major.model_dump())
    if check:
        return {"message": "Факультет успешно добавлен!", "major": major}
    else:
        return {"message": "Ошибка при добавлении факультета!"}
    