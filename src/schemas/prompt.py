from pydantic import BaseModel


class PromptRequest(BaseModel):
    input: str
    session_id: str


class PromptResponse(BaseModel):
    text: str
    seconds: float
