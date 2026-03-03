from pydantic import BaseModel

class StartSessionRequest(BaseModel):
    session_id: str

class PredictRequest(BaseModel):
    session_id: str
    guess: str
    pattern: str

class CloseRequest(BaseModel):
    session_id: str

