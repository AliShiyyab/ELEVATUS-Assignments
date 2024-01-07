from http.client import HTTPException
from typing import List, Union

from app.models.candidate_model import Candidate
from app.models.user_model import User
from app.repositories.candidate_repository import CandidateRepository
from app.repositories.user_repository import UserRepository


class CandidateService:
    def __init__(self, candidate_repository: CandidateRepository):
        self.candidate_repository: CandidateRepository = candidate_repository

    async def create_candidate(self, candidate: Candidate) -> Union[Candidate, HTTPException]:
        """
        This service used to create candidate depends on the data which received from FE
        :param candidate: Dict
        :return: Candidate Data or HTTPException
        """
        try:
            return await self.candidate_repository.create_candidate(candidate_data=candidate)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error creating candidate: {str(e)}")

    async def update_candidate(self, candidate_id: str,
                               updated_candidate: Candidate) -> Union[Candidate, HTTPException]:
        """
        This service is used to update candidate data based on the candidate id (uuid)
        :param candidate_id: String
        :param updated_candidate: dict for new data
        :return: Candidate Data or HTTPException
        """
        try:
            updated_candidate = await self.candidate_repository.update_candidate(candidate_id, updated_candidate)
            updated_candidate['_id'] = str(updated_candidate['_id'])
            return updated_candidate
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error updating candidate: {str(e)}")

    async def delete_candidate(self, email: str) -> Union[dict, HTTPException]:
        """
        This service used to delete the candidate data using email
        :param email: String
        :return: dict or HTTPException
        """
        try:
            deleted_count = await self.candidate_repository.delete_candidate(email)
            if deleted_count == 0:
                raise HTTPException(status_code=404, detail="Candidate not found")
            return {"message": "Candidate deleted successfully"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error deleting candidate: {str(e)}")

    async def get_candidate(self, uuid: str) -> Union[Candidate, HTTPException]:
        """
        This service used to get candidates using uuid
        :param uuid: string
        :return: Candidate or raise exception
        """
        candidate = await self.candidate_repository.get_candidate_by_id(uuid=uuid)
        try:
            if candidate:
                return candidate
        except Exception as e:
            raise HTTPException(status_code=404, detail="Candidate not found")

    async def get_all_candidates(self, keyword: str = None,
                                 filters: dict = None) -> Union[List[Candidate], HTTPException]:
        """
        This service used to return all candidates in the model
        :param keyword: string
        :param filters: dictionary
        :return: List of Candidates or raise exception
        """
        try:
            candidates = await self.candidate_repository.find_candidates(keyword=keyword, filters=filters)
            return candidates
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error getting user: {str(e)}")


class UserService:

    def __init__(self, user_repository: UserRepository):
        self.user_repository: UserRepository = user_repository

    async def get_user_by_email(self, email: str) -> Union[User, HTTPException]:
        """
        This service used to return user data using email
        :param email: String
        :return: User or HTTPException
        """
        try:
            user = self.user_repository.get_user_by_email(email)
            if user:
                return user
            else:
                raise HTTPException(status_code=404, detail="User not found")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error getting user: {str(e)}")

    async def create_user(self, user: User) -> Union[User, HTTPException]:
        """
        This service used to create new user depends on the data which received from FE
        :param user: User Data
        :return: User data or HTTPException
        """
        try:
            return await self.user_repository.create_user(user)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error creating user: {str(e)}") from e

    async def get_all_user(self):
        try:
            return await self.user_repository.get_all()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error creating user: {str(e)}") from e

