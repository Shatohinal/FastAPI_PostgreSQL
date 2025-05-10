from fastapi import APIRouter
from app.students.dao import StudentDAO


router = APIRouter(prefix='/students', tags=['Работа со студентами'])


@router.get("/", summary="Получить всех студентов")
async def get_all_students():
    return await StudentDAO.find_all_students()