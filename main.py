from database import CConnection, session_scope
from sqlalchemy import text


connection = CConnection()

with session_scope(connection) as session:
    print(session.execute(text("SELECT 1")).fetchone())

