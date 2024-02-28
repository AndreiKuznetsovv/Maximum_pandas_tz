from database import CConnection, session_scope
from sqlalchemy import text


connection = CConnection()

with session_scope(connection) as session:
    # Тест соединения с БД
    print(session.execute(text("SELECT 1")).fetchone())

