from app.dao.base import BaseDAO
from app.majors.models import Major
from app.database import async_session_maker

class MajorsDAO(BaseDAO[Major]):
    model = Major
