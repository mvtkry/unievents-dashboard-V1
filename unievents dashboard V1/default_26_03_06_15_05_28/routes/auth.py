from fastapi import APIRouter, Depends, HTTPException, Response, Request, Form
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from database import get_db
import models, auth_utils
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/login")
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/login")
def login(
    response: Response,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user or not auth_utils.verify_password(password, user.hashed_password):
        return templates.TemplateResponse("login.html", {
            "request": {}, 
            "error": "Invalid username or password"
        })
    
    access_token = auth_utils.create_access_token(data={"sub": user.username})
    
    response = RedirectResponse(url="/dashboard", status_code=302)
    response.set_cookie(key="access_token", value=f"Bearer {access_token}", httponly=True)
    return response

@router.get("/logout")
def logout():
    response = RedirectResponse(url="/login")
    response.delete_cookie("access_token")
    return response
