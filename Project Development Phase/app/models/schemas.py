from typing import Literal
from pydantic import BaseModel, Field
class RegisterRequest(BaseModel):
    email:str
    password:str=Field(min_length=6,max_length=128)
class LoginRequest(BaseModel):
    email:str
    password:str
class HomeRequest(BaseModel):
    budget:float=Field(gt=0)
    rooms:list[str]=Field(min_length=1)
    style:str="modern"
    notes:str=""
class PartyRequest(BaseModel):
    budget:float=Field(gt=0)
    guests:int=Field(gt=0,le=10000)
    event_type:str="birthday"
    venue:str="home"
    city:str=""
    notes:str=""
class JewelryRequest(BaseModel):
    budget:float=Field(gt=0)
    occasion:str="casual"
    outfit_style:str="elegant"
    metal:str="any"
    notes:str=""
class RecommendationItem(BaseModel):
    name:str; category:str; platform:str; estimated_price:float; currency:str="INR"; reason:str; url:str
class RecommendationResponse(BaseModel):
    planner:str; budget:float; allocation:dict[str,float]; summary:str; tips:list[str]
    recommendations:list[RecommendationItem]; source:Literal["gemini","fallback"]
    disclaimer:str
