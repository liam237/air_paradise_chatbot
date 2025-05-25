# chatbot/api/schemas.py

from pydantic import BaseModel

class PredictionRequest(BaseModel):
    DISTANCE: float
    SCHEDULED_TIME: float
    MONTH: int
    DAY_OF_WEEK: int
    ORIGIN_AIRPORT: str
    DESTINATION_AIRPORT: str
    SCHEDULED_DEPARTURE: str
