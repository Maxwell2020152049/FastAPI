"""
用户的接口
"""

from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

import deps, crud, utils, schemas

app_user = APIRouter()

@app_user.get("/me")
async def read_users_me(current_user: schemas.User = Depends(utils.get_current_active_user)):
    """
    获取当前可用的用户
    """
    return current_user


@app_user.get("/me/items")
async def read_own_items(current_user: schemas.User = Depends(utils.get_current_active_user)):
    """
    示例函数
    """
    return [{"item_id": "Foo", "owner": current_user.username}]

@app_user.post("/token", response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm
                                 = Depends(OAuth2PasswordRequestForm)):
    """
    获取用户的许可证和许可证类型
    """
    # print(dict(form_data))

    user = utils.authenticate_user(utils.fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=utils.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = utils.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app_user.post("/signup", summary="创建新用户")
async def create_new_user(user: schemas.UserCreate, database: Session = Depends(deps.get_db)):
    """
    1. 检查用户是否被注册;
    2. 若已经被注册, 跳到4; 若未被注册, 跳到3
    3. 将用户密码做哈希, 存入数据库;
    4. 结束
    """

    user_in_database = crud.get_user_by_username(database, user.username)

    print(user_in_database)

    if user_in_database:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="该用户名已经被注册"
        )

    user.password = utils.get_password_hash(user.password)

    crud.create_user(database, user)

@app_user.post("/login", summary="登录")
async def login(user: schemas.UserCreate, database: Session = Depends(deps.get_db)):
    """
    登录功能
    """
    user_in_database = crud.get_user_by_username(database, user.username)

    if not user_in_database:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"用户名 '{user.username}'不存在"
        )

    if not utils.verify_password(user.password, user_in_database.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="密码错误",
        )

    return "yes"
