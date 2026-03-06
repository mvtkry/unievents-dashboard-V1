from fastapi import APIRouter, Depends, Request, Form, Query
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import get_db
import models, auth_utils, schemas
from fastapi.templating import Jinja2Templates
import math

router = APIRouter()
templates = Jinja2Templates(directory="templates")

def login_required(user = Depends(auth_utils.get_current_user)):
    if not user:
        raise HTTPException(status_code=302, headers={"Location": "/login"})
    return user

@router.get("/")
@router.get("/dashboard")
async def dashboard(request: Request, db: Session = Depends(get_db), current_user=Depends(auth_utils.get_current_user)):
    if not current_user:
        return RedirectResponse(url="/login")
    
    stats = {
        "events_count": db.query(models.Event).count(),
        "participants_count": db.query(models.Participant).count(),
        "total_scores": db.query(models.Score).count(),
        "avg_score": db.query(func.avg(models.Score.points)).scalar() or 0
    }
    
    recent_activities = db.query(models.Score).order_by(models.Score.recorded_at.desc()).limit(5).all()
    
    return templates.TemplateResponse("dashboard.html", {
        "request": request, 
        "user": current_user,
        "stats": stats,
        "recent_activities": recent_activities,
        "active_page": "dashboard"
    })

@router.get("/events")
async def events(request: Request, page: int = 1, db: Session = Depends(get_db), current_user=Depends(auth_utils.get_current_user)):
    if not current_user: return RedirectResponse(url="/login")
    
    limit = 10
    offset = (page - 1) * limit
    total = db.query(models.Event).count()
    events = db.query(models.Event).offset(offset).limit(limit).all()
    
    return templates.TemplateResponse("events.html", {
        "request": request,
        "user": current_user,
        "events": events,
        "page": page,
        "total_pages": math.ceil(total / limit),
        "active_page": "events"
    })

@router.get("/participants")
async def participants(request: Request, db: Session = Depends(get_db), current_user=Depends(auth_utils.get_current_user)):
    if not current_user: return RedirectResponse(url="/login")
    
    participants = db.query(models.Participant).all()
    return templates.TemplateResponse("participants.html", {
        "request": request,
        "user": current_user,
        "participants": participants,
        "active_page": "participants"
    })

@router.get("/scoring")
async def scoring_view(request: Request, db: Session = Depends(get_db), current_user=Depends(auth_utils.get_current_user)):
    if not current_user: return RedirectResponse(url="/login")
    
    events = db.query(models.Event).all()
    participants = db.query(models.Participant).all()
    return templates.TemplateResponse("scoring.html", {
        "request": request,
        "user": current_user,
        "events": events,
        "participants": participants,
        "active_page": "scoring"
    })

@router.post("/scoring")
async def process_scoring(
    request: Request,
    event_id: int = Form(...),
    participant_id: int = Form(...),
    points: float = Form(...),
    db: Session = Depends(get_db),
    current_user=Depends(auth_utils.get_current_user)
):
    if not current_user: return RedirectResponse(url="/login")
    
    new_score = models.Score(event_id=event_id, participant_id=participant_id, points=points)
    db.add(new_score)
    db.commit()
    return RedirectResponse(url="/leaderboard", status_code=302)

@router.get("/leaderboard")
async def leaderboard(request: Request, db: Session = Depends(get_db), current_user=Depends(auth_utils.get_current_user)):
    if not current_user: return RedirectResponse(url="/login")
    
    # Simple aggregation for leaderboard
    results = db.query(
        models.Participant.name,
        models.Participant.department,
        func.sum(models.Score.points).label("total_points")
    ).join(models.Score).group_by(models.Participant.id).order_by(func.sum(models.Score.points).desc()).all()
    
    return templates.TemplateResponse("leaderboard.html", {
        "request": request,
        "user": current_user,
        "results": results,
        "active_page": "leaderboard"
    })

@router.get("/single-entry")
async def single_entry(request: Request, current_user=Depends(auth_utils.get_current_user)):
    if not current_user: return RedirectResponse(url="/login")
    return templates.TemplateResponse("single_entry.html", {
        "request": request, 
        "user": current_user,
        "active_page": "single-entry"
    })

@router.post("/single-entry")
async def post_single_entry(
    name: str = Form(...),
    email: str = Form(...),
    department: str = Form(...),
    db: Session = Depends(get_db),
    current_user=Depends(auth_utils.get_current_user)
):
    if not current_user: return RedirectResponse(url="/login")
    
    participant = models.Participant(name=name, email=email, department=department)
    db.add(participant)
    db.commit()
    return RedirectResponse(url="/participants", status_code=302)
