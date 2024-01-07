from typing import List, Literal

from pydantic import BaseModel


class Candidate(BaseModel):
    first_name: str
    last_name: str
    email: str
    uuid: str
    career_level: str
    job_major: str
    years_of_experience: int
    degree_type: str
    skills: List[str]
    nationality: str
    city: str
    salary: int
    gender: Literal["Male", "Female", "Not Specified"]

    def dict(self):
        return {k: v for k, v in self.__dict__.items() if not k.startswith('_')}

