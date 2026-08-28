from pydantic import BaseModel, Field
from typing import List, Dict


#1 what the user send to the api 

class SentimentRequest(BaseModel):
    texts: List[str] = Field(...,
                            min_length = 1, 
                            description = "A list of text strings to analyze for sentiment")
# what the api returns to the user
class SentimentResult(BaseModel):
    positive: float
    negative:float
    neutral:float

#3 The Final response Wrapper
class SentimentResponse(BaseModel):
    model_name: str
    predictions: List[SentimentResult]    
