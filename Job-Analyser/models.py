from pydantic import BaseModel
from typing import Optional

class JobAnalysis(BaseModel):
    job_title:str
    company_name:Optional[str]=None
    experience_level:str
    experience_years:Optional[str]=None
    employment_type:str
    work_mode:str

    required_skills:list[str]
    preferred_skills:list[str]

    salary_range:Optional[str]=None
    location:Optional[str]=None

    responsibilities:list[str]

    red_flags:list[str]

    summary:str

    