import json
from fastapi import APIRouter,Depends,HTTPException,File,Form,UploadFile,Request
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.db import RecommendationHistory
from app.models.schemas import HomeRequest,PartyRequest,JewelryRequest,RecommendationResponse
from app.services.auth_service import get_user_from_token
from app.services.recommendation_service import home,party,jewelry
router=APIRouter(prefix="/api",tags=["planners"])
def user(request:Request,db):
    u=get_user_from_token(db,request.cookies.get("access_token"))
    if not u: raise HTTPException(401,"Please log in first.")
    return u
def save(db,u,planner,budget,inp,result):
    db.add(RecommendationHistory(user_id=u.id,planner=planner,budget=budget,input_json=json.dumps(inp),result_json=json.dumps(result)));db.commit()
@router.post("/generate-home",response_model=RecommendationResponse)
def generate_home(d:HomeRequest,request:Request,db:Session=Depends(get_db)):
    u=user(request,db);x=home(d);save(db,u,"home",d.budget,d.model_dump(),x);return x
@router.post("/generate-party",response_model=RecommendationResponse)
def generate_party(d:PartyRequest,request:Request,db:Session=Depends(get_db)):
    u=user(request,db);x=party(d);save(db,u,"party",d.budget,d.model_dump(),x);return x
@router.post("/generate-jewelry",response_model=RecommendationResponse)
async def generate_jewelry(budget:float=Form(...),occasion:str=Form("casual"),outfit_style:str=Form("elegant"),metal:str=Form("any"),notes:str=Form(""),outfit_image:UploadFile|None=File(None),request:Request=None,db:Session=Depends(get_db)):
    u=user(request,db)
    if budget<=0: raise HTTPException(422,"Budget must be positive.")
    data=None;mime=None
    if outfit_image and outfit_image.filename:
        mime=outfit_image.content_type or ""
        if mime not in {"image/jpeg","image/png","image/webp"}: raise HTTPException(415,"Only JPG, PNG and WEBP images are allowed.")
        data=await outfit_image.read()
        if len(data)>5*1024*1024: raise HTTPException(413,"Image must be 5 MB or smaller.")
    d=JewelryRequest(budget=budget,occasion=occasion,outfit_style=outfit_style,metal=metal,notes=notes);x=jewelry(d,data,mime);save(db,u,"jewelry",budget,d.model_dump(),x);return x
@router.get("/history")
def history(request:Request,db:Session=Depends(get_db)):
    u=user(request,db);rows=db.query(RecommendationHistory).filter_by(user_id=u.id).order_by(RecommendationHistory.created_at.desc()).limit(20).all()
    return [{"id":r.id,"planner":r.planner,"budget":r.budget,"created_at":r.created_at.isoformat(),"result":json.loads(r.result_json)} for r in rows]
@router.get("/session-info")
def session_info(request:Request,db:Session=Depends(get_db)):
    u=user(request,db);return {"logged_in":True,"user_id":u.id,"email":u.email}
@router.get("/session-data")
def session_data(request:Request,db:Session=Depends(get_db)):
    u=user(request,db);return {"email":u.email,"recommendation_count":db.query(RecommendationHistory).filter_by(user_id=u.id).count()}
