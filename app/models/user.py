from pydantic import BaseModel
from datetime import datetime
from typing import List

# custom defined
from app.utils.security import verify_password
from app.models.common import IDModel, UpdatedAtModel, CreatedAtModel


class UserBase(BaseModel):
    username: str
    role: List[int]


class UserCreate(UserBase, IDModel, UpdatedAtModel, CreatedAtModel):
    password: str


class User(UserBase):
    id: str
    token: str


class UserInDB(UserBase):
    id: str
    salt: str = ''
    hashed_password: str = ''
    updatedAt: str
    createdAt: str

    def check_password(self, password: str):
        return verify_password(self.salt + password, self.hashed_password)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = 'bearer'


class TokenPayload(BaseModel):
    id: str
    exp: datetime


class UserListModel(BaseModel):
    id: str
    username: str
    role: List
    createdAt: str


class UserListResponse(BaseModel):
    data: List[UserListModel]
    total: int
