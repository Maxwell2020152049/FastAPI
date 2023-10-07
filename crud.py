"""
业务的增删查改操作
"""

from sqlalchemy.orm import  Session
from schemas import UserCreate
import models

def create_user(database: Session, user: UserCreate):
    """
    [Atomic] 在数据库的user表中插入一条记录。
    """
    user_in_database = models.User(**user.dict())

    database.add(user_in_database)
    database.commit()
    database.flush()


def get_user_by_username(database: Session, username: str):
    """
    [Atomic] 在数据库的user表中查询用户名为`username`的用户。
    """
    return database.query(models.User).filter(models.User.username == username).first()
