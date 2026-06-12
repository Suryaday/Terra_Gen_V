from pydantic import BaseModel

class GenerateRequest(BaseModel):
    query: str

class GenerateResponse(BaseModel):
    query: str
    architecture: list[str]
    terraform: str
    warnings: list[str]
    generation_time_seconds: float