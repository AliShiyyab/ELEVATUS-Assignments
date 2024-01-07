from motor.motor_asyncio import AsyncIOMotorClient


class CandidateRepository:
    def __init__(self, db: AsyncIOMotorClient):
        self.db = db

    async def create_candidate(self, candidate_data):
        candidate_data_dict = candidate_data.dict() if hasattr(candidate_data, 'dict') else dict(candidate_data)
        result = await self.db.candidates.insert_one(candidate_data_dict)
        return await self.db.candidates.find_one({"_id": result.inserted_id})

    async def update_candidate(self, candidate_id, updated_candidate_data):
        updated_candidate_data_dict = (
            updated_candidate_data.dict() if hasattr(updated_candidate_data, 'dict') else dict(updated_candidate_data)
        )
        await self.db.candidates.update_one({"uuid": candidate_id}, {"$set": updated_candidate_data_dict})
        return await self.db.candidates.find_one({"uuid": candidate_id})

    async def delete_candidate(self, email):
        result = await self.db.candidates.delete_one({"email": email})
        return result.deleted_count

    async def get_candidate_by_id(self, uuid):
        return await self.db.candidates.find_one({"uuid": uuid})

    async def find_candidates(self, keyword: str = None, filters: dict = None):
        query = {}
        if keyword:
            query["$text"] = {"$search": keyword}
        if filters:
            for field, value in filters.items():
                query[field] = value

        return await self.db.candidates.find(query).to_list(length=None)

    async def get_all_candidates(self):
        return await self.db.candidates.find().to_list(length=None)
