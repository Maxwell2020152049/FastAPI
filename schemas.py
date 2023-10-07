"""
数据表的实例
"""

from typing import Optional
from pydantic import BaseModel


class User(BaseModel):
    """
    用户表的实例
    """
    username: Optional[str] = None
    email: Optional[str] = None
    fullname: Optional[str] = None
    disabled: Optional[bool] = None

class UserInDB(User):
    """
    数据库中的用户
    """
    hashed_password: str

class Token(BaseModel):
    """
    认证token和类型
    """
    access_token: str
    token_type: str

class TokenData(BaseModel):
    """
    Token的数据
    """
    username: Optional[str] = None

class UserCreate(BaseModel):
    """
    用户的创建类
    """
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
