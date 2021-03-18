from fastapi import APIRouter, Depends, HTTPException, Body
from fastapi.security import OAuth2PasswordRequestForm
from starlette.status import HTTP_400_BAD_REQUEST
from typing import List
# custom defined
from app.models.user import UserCreate, User, TokenResponse, UserListResponse
from app.crud.user import create_user, get_user, get_user_list_by_query_with_page_and_limit, count_user_by_query
from app.dependencies.jwt import get_current_user_authorizer
from app.utils.jwt import create_access_token
from app.db.mongodb import AsyncIOMotorClient, get_database

router = APIRouter()


@router.post("/users/login", response_model=TokenResponse, tags=["user"], name='账号密码登录')
async def login(user: OAuth2PasswordRequestForm = Depends(), db: AsyncIOMotorClient = Depends(get_database)):
    dbuser = await get_user(conn=db, query={'username': user.username})
    if not dbuser:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail='40008')
    elif not dbuser.check_password(user.password):
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail='40009')
    token = create_access_token(data={"id": dbuser.id})
    # swaggerui 要求返回此格式
    return TokenResponse(access_token=token)


@router.post('/user', tags=['admin'], name='单个用户添加')
async def post_users(
        username: str = Body(..., embed=True), role: List[int] = Body(...),
        user: User = Depends(get_current_user_authorizer(required=True)),
        db: AsyncIOMotorClient = Depends(get_database)
):
    if 0 not in user.role:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail='40005')
    data_user = await get_user(conn=db, query={'username': username})
    # 用户名重复
    if data_user:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail='40001')
    user_model = UserCreate(
        username=username,
        password=username,
        role=role
    )
    await create_user(conn=db, user=user_model)
    return {'data': {'id': user_model.id}}


@router.get('/user_list', tags=['admin'], response_model=UserListResponse, name='用户列表获取')
async def get_user_list(
        search: str = None, page: int = 1, limit: int = 20,
        user: User = Depends(get_current_user_authorizer(required=True)),
        db: AsyncIOMotorClient = Depends(get_database)
):
    if 0 not in user.role:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail='40005')
    data_user = await get_user_list_by_query_with_page_and_limit(conn=db, query={
        'username': {'$regex': search}} if search else {}, page=page, limit=limit)
    total = await count_user_by_query(conn=db, query={'username': {'$regex': search}} if search else {})
    return UserListResponse(data=data_user, total=total)


@router.get('/user/me', tags=['user'], name='用户个人信息')
async def user_me(
        user: User = Depends(get_current_user_authorizer(required=True)),
        db: AsyncIOMotorClient = Depends(get_database)
):
    dbuser = await get_user(conn=db, query={'id': user.id})
    return {'username': dbuser.username, 'role': dbuser.role}
