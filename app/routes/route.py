from typing import Any

from fastapi import Depends, APIRouter, HTTPException, Query, Body
from fastapi.responses import JSONResponse, StreamingResponse

from app.database_configration.db_configration import connect_to_mongo
from app.models.user_model import User
from app.models.candidate_model import Candidate

from motor.motor_asyncio import AsyncIOMotorClient

from app.repositories.user_repository import UserRepository
from app.repositories.candidate_repository import CandidateRepository

from app.services.services import UserService, CandidateService

router = APIRouter()


@router.get("/")
def home():
    return JSONResponse(content={"message": "Welcome in our API"})


@router.get("/health")
async def get_health():
    return {"Message": "Health"}


@router.post("/user")
async def create_user(user: User, db: AsyncIOMotorClient = Depends(connect_to_mongo)):
    """
    :param user: data which received from Frontend
    :param db: DataBase
    :return: JSON
    """
    user_service = UserService(UserRepository(db))
    await user_service.create_user(user)
    return JSONResponse(content={"message": "User created successfully"}, status_code=201)


@router.get("/user")
async def get_all_users(db: AsyncIOMotorClient = Depends(connect_to_mongo)):
    """
    This view used to return all users in the model
    :param db: DataBase
    :return: JSON
    """
    user_service = UserService(UserRepository(db))
    all_user = await user_service.get_all_user()
    for user in all_user:
        user['_id'] = str(user['_id'])

    return JSONResponse(content=all_user, status_code=200)


@router.get("/candidate/{uuid}")
async def get_candidates(uuid: str, db: AsyncIOMotorClient = Depends(connect_to_mongo)):
    """
    :param uuid: Integer represent CandidateID
    :param db: Database connection dependency obtained using (connect_to_mongo).
    :return: JSONResponse
    """
    candidate_service = CandidateService(CandidateRepository(db))
    candidate = await candidate_service.get_candidate(uuid)
    if candidate:
        candidate['_id'] = str(candidate['_id'])  # Convert ObjectId to string
        return JSONResponse(content=candidate, status_code=200)
    else:
        raise HTTPException(status_code=404, detail="Candidate not found")


@router.post('/candidate', response_model=Any)
async def create_candidate(candidate: Candidate, db: AsyncIOMotorClient = Depends(connect_to_mongo)):
    """
    :param candidate: Candidate data which received from FE
    :param db: Database connection dependency obtained using (connect_to_mongo).
    :return: JSONResponse
    """
    candidate_service = CandidateService(CandidateRepository(db))
    await candidate_service.create_candidate(candidate)
    return JSONResponse(content={"message": "Created candidate successfully"}, status_code=201)


@router.delete('/candidate/{email}')
async def delete_candidate_by_email(email: str,
                                    db: AsyncIOMotorClient = Depends(connect_to_mongo)):
    """
    :param email: String
    :param db: Database connection dependency obtained using (connect_to_mongo).
    :return: JSONResponse
    """
    candidate_service = CandidateService(CandidateRepository(db))
    response = await candidate_service.delete_candidate(email)
    return JSONResponse(content=response, status_code=204)


@router.put('/candidate/{uuid}')
async def update_candidate(uuid: str,
                           candidate: Candidate,
                           db: AsyncIOMotorClient = Depends(connect_to_mongo)):
    """
    :param uuid: String
    :param candidate: Candidate data which received from FE
    :param db: Database connection dependency obtained using (connect_to_mongo).
    :return: JSONResponse
    """
    candidate_service = CandidateService(CandidateRepository(db))
    updated_candidate = await candidate_service.update_candidate(uuid, candidate)
    updated_candidate['_id'] = str(updated_candidate['_id'])  # Convert ObjectId to string
    return JSONResponse(content=updated_candidate, status_code=201)


@router.get('/all-candidates')
async def get_all_candidates(
        db: AsyncIOMotorClient = Depends(connect_to_mongo),
        keyword: str = Query(None, alias='q', description='Global search keyword'),
        field_filters: dict = Body({}, alias='filters', description='Field-specific filters'),
):
    """
    Retrieve a list of candidates based on optional search parameters.

    Parameters:
    - `db` (AsyncIOMotorClient): Database connection dependency obtained using (connect_to_mongo).
    - `keyword` (str, optional): Global search keyword to filter candidates.
    - `field_filters` (dict, optional): Field-specific filters to narrow down the candidate search.

    Returns:
    - `JSONResponse`: A JSON response containing the list of candidates matching the specified criteria.

    Raises:
    - HTTPException: If there is an error during the retrieval process, an HTTPException is raised
                    with appropriate status code and details.

    Note:
    The returned JSON response includes the list of candidates in the 'content' field.
    If there is an error during the retrieval process, an error message is included in the 'error' field.
    """
    candidate_service = CandidateService(CandidateRepository(db))
    try:
        all_candidates = await candidate_service.get_all_candidates(keyword=keyword, filters=field_filters)
        for candidate in all_candidates:
            candidate['_id'] = str(candidate['_id'])
        return JSONResponse(content=[candidate for candidate in all_candidates], status_code=200)
    except HTTPException as e:
        return JSONResponse(content={"error": e.detail}, status_code=e.status_code)


@router.get('/generate-report', response_model=Any)
async def generate_report(db: AsyncIOMotorClient = Depends(connect_to_mongo)):
    """
    :param db: Database connection dependency obtained using (connect_to_mongo).
    :return: Any
    """
    candidate_service = CandidateService(CandidateRepository(db))
    try:
        candidates = await candidate_service.get_all_candidates()
        if not candidates:
            return JSONResponse(content={"error": "Does not have any candidates"}, status_code=200)

        csv_data = "first_name,last_name,email,uuid,career_level,job_major,years_of_experience,degree_type,skills,nationality,city,salary,gender\n"
        for candidate_dict in candidates:
            candidate = Candidate(**candidate_dict)  # Convert dict to Candidate instance
            csv_data += (
                f"{candidate.first_name},{candidate.last_name},{candidate.email},{candidate.uuid},"
                f"{candidate.career_level},{candidate.job_major},{candidate.years_of_experience},"
                f"{candidate.degree_type},"
                f"{'|'.join(candidate.skills)},{candidate.nationality},{candidate.city},"
                f"{candidate.salary},{candidate.gender}\n"
            )

        return StreamingResponse(content=iter([csv_data]), media_type="text/csv",
                                 headers={"Content-Disposition": "attachment;filename=candidates_report.csv"})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=400)
