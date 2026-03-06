# PyDash - FastAPI Full-Stack Dashboard

A production-ready admin dashboard built with Python, FastAPI, SQLAlchemy, and Tailwind CSS.

## Features
- **Authentication**: JWT-based session management using HttpOnly cookies.
- **Dynamic UI**: Responsive sidebar and navigation built with Jinja2 and Tailwind CSS.
- **Data Management**: Full CRUD capability for Events, Participants, and Scoring.
- **Real-time Stats**: Dashboard KPIs and automated leaderboard aggregation.
- **Database**: SQLite with SQLAlchemy ORM and automatic seeding.
- **Validation**: Pydantic models for request validation and type safety.

## Prerequisites
- Python 3.8 or higher

## Installation

1. Clone the repository or extract the files.
2. Create a virtual environment:
    python -m venv venv
3. Activate the virtual environment:
    # Windows
    venv\Scripts\activate
    # macOS/Linux
    source venv/bin/activate
4. Install the dependencies:
    pip install -r requirements.txt

## Running the Application

Start the development server:
    python main.py

The application will be available at: `http://127.0.0.1:8000`

## Default Credentials
- **Username**: `admin`
- **Password**: `admin123`

## Project Structure
- `main.py`: Entry point and app configuration.
- `models.py`: SQLAlchemy database models.
- `schemas.py`: Pydantic validation schemas.
- `database.py`: DB engine and session handling.
- `auth_utils.py`: JWT and password hashing utilities.
- `routes/`: Backend logic for authentication and admin views.
- `templates/`: Jinja2 HTML templates for the frontend.
- `static/`: Custom CSS and assets.

## Usage Guide
1. **Dashboard**: View high-level statistics and recent scoring activity.
2. **Events**: Manage the list of active and upcoming events.
3. **Participants**: View and filter the list of registered users.
4. **Scoring**: Use the scoring form to assign points to a participant for a specific event.
5. **Leaderboard**: Check the auto-calculated rankings based on total points.
6. **Single Entry**: Quickly register new participants.

## Troubleshooting
- **Database errors**: Delete `dashboard.db` and restart the application to recreate and re-seed the database.
- **Session issues**: If you cannot log in, clear your browser cookies for `127.0.0.1`.
