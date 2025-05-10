from typing import List
from fastapi import APIRouter
from app.students.dao import StudentDAO
from app.students.schemas import SStudent


router = APIRouter(prefix='/students', tags=['Работа со студентами'])


@router.get("/", summary="Получить всех студентов", response_model=List[SStudent])
async def get_all_students():
    return await StudentDAO.find_all_students()