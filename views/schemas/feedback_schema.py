from pydantic import BaseModel

class FeedbackRequest(BaseModel):
    prediction_id: int
    correct_label: bool

class UpdateFeedbackRequest(BaseModel):
    correct_label: bool

class FeedbackResponse(BaseModel):
    message: str

class FeedbackResponseFull(BaseModel):
    id: int
    prediction_id: int
    correct_label: bool

    model_config = {
        "from_attributes": True
    }