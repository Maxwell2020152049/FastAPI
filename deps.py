"""
依赖项
"""

from database import SessionLocal

# Dependency
def get_db():
    """
    返回当前数据库会话
    """
    database = SessionLocal()
    try:
        yield database
    finally:
        database.close()
