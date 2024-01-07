import uuid
from typing import Union
from motor.motor_asyncio import AsyncIOMotorClient
from app.models.user_model import User


class UserRepository:
    def __init__(self, db: AsyncIOMotorClient) -> Union[None, User]:
        self.db = db

    async def get_user_by_email(self, email):
        user = await self.db.users.find_one({"email": email})
        if user:
            return user
        else:
            return None

    async def create_user(self, user_data) -> Union[None, int]:
        user_uuid = str(uuid.uuid4())
        user_data.uuid = user_uuid
        user_data_dict = user_data.dict() if hasattr(user_data, 'dict') else dict(user_data)
        is_email_already_used = await self.db.users.find_one({'email': user_data.email})
        if is_email_already_used:
            return None
        result = await self.db.users.insert_one(user_data_dict)
        return result.inserted_id

    async def get_all(self):
        return await self.db.users.find().to_list(length=None)
