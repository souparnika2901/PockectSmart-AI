from fastapi import APIRouter, Depends, HTTPException, Form
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.schemas import RegisterRequest,LoginRequest
from app.services.auth_service import create_user,authenticate,create_access_token
router=APIRouter(tags=["auth"])
@router.post("/register")
def register(
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    try:
        u = create_user(db, email, password)
    except ValueError as e:
        raise HTTPException(409, str(e))

    r = JSONResponse({
        "message": "Registration successful",
        "email": u.email
    })

    r.set_cookie(
        "access_token",
        create_access_token(u.id),
        httponly=True,
        samesite="lax",
        max_age=86400
    )

    return r
@router.post("/api/login")
def login(d:LoginRequest,db:Session=Depends(get_db)):
    u=authenticate(db,d.email,d.password)
    if not u: raise HTTPException(401,"Invalid email or password.")
    r=JSONResponse({"message":"Login successful","email":u.email});r.set_cookie("access_token",create_access_token(u.id),httponly=True,samesite="lax",max_age=86400);return r
@router.post("/api/logout")
def logout():
    r=JSONResponse({"message":"Logged out"});r.delete_cookie("access_token");return r
