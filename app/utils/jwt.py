from datetime import datetime, timedelta
from typing import Optional
import jwt
# custom defined
from app.core.config import timezone, secret_key, algorithm, access_token_expire_minutes


# 创建token，token包含exp,和用户自定义的json数据
def create_access_token(*, data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(tz=timezone) + expires_delta
    else:
        expire = datetime.now(tz=timezone) + timedelta(minutes=access_token_expire_minutes)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, str(secret_key), algorithm=algorithm)
    return encoded_jwt
