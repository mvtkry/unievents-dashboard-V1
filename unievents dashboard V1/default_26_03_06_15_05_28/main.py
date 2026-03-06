import os
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
import database, models, auth_utils
from routes import auth, admin

# Initialize database
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="PyDash Dashboard")

# Mount static files
os.makedirs("static/css", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include routers
app.include_router(auth.router)
app.include_router(admin.router)

@app.on_event("startup")
def startup_populate():
    db = database.SessionLocal()
    
    # Create default admin if not exists
    admin_user = db.query(models.User).filter(models.User.username == "admin").first()
    if not admin_user:
        hashed_pw = auth_utils.get_password_hash("admin123")
        admin_user = models.User(username="admin", hashed_password=hashed_pw, full_name="System Admin")
        db.add(admin_user)
        db.commit()
    
    # Seed Mock Data if empty
    if db.query(models.Event).count() == 0:
        events = [
            models.Event(name="Annual Hackathon", description="24-hour coding challenge", status="Active"),
            models.Event(name="Design Workshop", description="UI/UX design principles", status="Completed"),
            models.Event(name="Marketing Summit", description="Strategy planning for Q4", status="Planned"),
            models.Event(name="Tech Talk: AI", description="Introduction to Large Language Models", status="Active")
        ]
        db.add_all(events)
        
        participants = [
            models.Participant(name="Alice Johnson", email="alice@example.com", department="Engineering"),
            models.Participant(name="Bob Smith", email="bob@example.com", department="Marketing"),
            models.Participant(name="Charlie Brown", email="charlie@example.com", department="Design"),
            models.Participant(name="Diana Prince", email="diana@example.com", department="Sales")
        ]
        db.add_all(participants)
        db.commit()
        
        # Add some initial scores
        scores = [
            models.Score(event_id=1, participant_id=1, points=95.0),
            models.Score(event_id=1, participant_id=3, points=88.5),
            models.Score(event_id=2, participant_id=2, points=76.0),
            models.Score(event_id=4, participant_id=1, points=92.0)
        ]
        db.add_all(scores)
        db.commit()
        
    db.close()

@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    return RedirectResponse(url="/dashboard")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
import uvicorn

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000)
    