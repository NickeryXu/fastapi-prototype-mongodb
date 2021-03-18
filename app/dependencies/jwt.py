from datetime import datetime, timedelta
from typing import Optional
from fastapi import Depends, Header
from starlette.exceptions import HTTPException
from starlette.status import HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND
from fastapi.security import OAuth2PasswordBearer
from app.models.user import UserInDB, TokenPayload, User
from app.db.mongodb import AsyncIOMotorClient, get_database
from app.core.config import jwt_token_prefix, secret_key, access_token_expire_minutes, algorithm, timezone, \
    database_name, user_collection_name
import jwt


async def get_user(conn: AsyncIOMotorClient, query: Optional[dict]) -> UserInDB:
    row = await conn[database_name][user_collection_name].find_one(query)
    return UserInDB(**row) if row else None


# Header中authorization信息校验，校验token的前缀
def _get_authorization_token(authorization: str = Header(...)):
    token_prefix, token = authorization.split(" ")
    if token_prefix != jwt_token_prefix:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="40006"
        )
    return token


# Swagger UI
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/users/login")


# 解密token，从db中获取用户信息
async def _get_current_user(db: AsyncIOMotorClient = Depends(get_database),
                            token: str = Depends(oauth2_scheme)) -> User:
    try:
        payload = jwt.decode(token, str(secret_key), algorithms=[algorithm])
        # TokenPayload可校验解密后内容
        token_data = TokenPayload(**payload)
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="40006"
        )
    '''
    从redis中读取用户数据，如无数据，再从mongo中查询，如有，直接返回
    '''

    dbuser = await get_user(db, {'id': token_data.id})
    if not dbuser:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="40007")

    user = User(**dbuser.dict(), token=token)
    return user


# 公开内容，无token可访问
def _get_authorization_token_optional(authorization: str = Header(None)):
    if authorization:
        return _get_authorization_token(authorization)
    return ""


# 可选项，用户信息
async def _get_current_user_optional(db: AsyncIOMotorClient = Depends(get_database),
                                     token: str = Depends(_get_authorization_token_optional), ) -> Optional[User]:
    if token:
        return await _get_current_user(db, token)

    return None


# 获取当前用户信息，required=True,必须拥有token才可访问，False,公开内容
def get_current_user_authorizer(*, required: bool = True):
    if required:
        return _get_current_user
    else:
        return _get_current_user_optional
