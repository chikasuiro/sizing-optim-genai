from pydantic import BaseModel

class GeometryParams(BaseModel):
    length_oval: float
    radius: float
    thickness: float
    fillet_size: float
    reasoning: str

class Individual(BaseModel):
    params: GeometryParams
    score: float
    history: str

class SelectionResult(BaseModel):
    selected_id: int
    justification: str
