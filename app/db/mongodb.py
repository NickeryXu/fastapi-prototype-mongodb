from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import database_url, max_connections_count, min_connections_count
from loguru import logger


class DataBase:
    client: AsyncIOMotorClient = None


db = DataBase()


async def get_database() -> AsyncIOMotorClient:
    return db.client


async def connect_to_mongodb() -> None:
    logger.info("连接数据库中...")
    db.client = AsyncIOMotorClient(str(database_url),
                                   maxPoolSize=max_connections_count,
                                   minPoolSize=min_connections_count,
                                   )
    logger.info("连接数据库成功！")


async def close_mongo_connection():
    logger.info("关闭数据库连接...")
    db.client.close()
    logger.info("数据库连接关闭！")
