from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional
from app.models.user import UserInDB, UserCreate, UserListModel
from app.utils.security import generate_salt, get_password_hash
from app.core.config import database_name, user_collection_name


async def get_user(conn: AsyncIOMotorClient, query: Optional[dict]) -> UserInDB:
    row = await conn[database_name][user_collection_name].find_one(query)
    return UserInDB(**row) if row else None


async def create_user(conn: AsyncIOMotorClient, user: UserCreate) -> UserInDB:
    salt = generate_salt()
    hashed_password = get_password_hash(salt + user.password)
    db_user = user.dict()
    db_user['salt'] = salt
    db_user['hashed_password'] = hashed_password
    del db_user['password']
    conn[database_name][user_collection_name].insert_one(db_user)
    return UserInDB(**user.dict())


async def get_user_list_by_query_with_page_and_limit(conn: AsyncIOMotorClient, query: Optional[dict], page: int,
                                                     limit: int):
    result = conn[database_name][user_collection_name].find(query).skip((page - 1) * limit).limit(limit)
    return [UserListModel(**x) async for x in result]


async def count_user_by_query(conn: AsyncIOMotorClient, query: Optional[dict]):
    result = await conn[database_name][user_collection_name].count_documents(query)
    return result
