"""
通用组件
"""

from typing import Optional
from datetime import datetime, timedelta
from passlib.context import CryptContext

from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt


from schemas import (
    UserInDB,
    TokenData,
    User
)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/token")
"""
OAuth2PasswordBearer实例。
使用OAuth2密码模式的认证方案。
"""


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
"""
CryptContext实例。
提供哈希算法和验证功能。
"""


# to get a string like this run:
# openssl rand -hex 32
# 使用openssl工具得到的密钥
SECRET_KEY = "1e6cee0942c9da2fd8804ecacb247b9ac421c1a969a58e171b7a606d07ce8d3b"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# 用户数据
fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    }
}

def verify_password(plain_password: str, hashed_password: str):
    """
    判断明文密码(plain_password)和哈希密码(hashed_password)是否能对应上。
    哈希算法是pwd_context对象指定的算法
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str):
    """
    返回密码(password)哈希后的结果。
    哈希算法是pwd_context对象指定的算法。
    """
    return pwd_context.hash(password)

def authenticate_user(fake_db, username: str, password: str):
    """
    实现用户的认证: 
    从数据库(db)中, 按照用户名(username)找到用户,
    若为空, 说明用户不存在;
    若非空, 再验证用户密码。
    """
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return True

def get_user(database, username: str):
    """
    在数据库(db)中使用用户名(username)获取用户。
    """
    if username in database:
        user_dict = database[username]
        return UserInDB(**user_dict)
    return None

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    复制数据(data), 并添加过期时间(当前时间 + 到期时间)。
    到期时间缺省值为15分钟。
    返回值: 使用密钥(SECRET_KEY), 指定加密算法(ALGORITHM)编码后的jwt字符串。
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    获取当前用户。
    使用OAuth2认证方案获得token。
    验证token正确性。
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="无法验证凭据",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError as jwt_error:
        raise credentials_exception from jwt_error
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)):
    """
    验证当前用户是否可用
    """
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
