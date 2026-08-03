from database import Fixture, FixtureResponse, Team, Prediction, PredictionResponse

from pydantic import BaseModel

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, Session
import sqlalchemy

from typing import List

app = FastAPI()
DATABASE_URL = "sqlite:///./football_predictor.db"  # SQLite database URL for local development
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = sqlalchemy.orm.declarative_base()

# CORS (Cross-Origin Resource Sharing) settings to prevent errors when the frontend and backend are on different origins
origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:5500",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class FixtureListItem(BaseModel):
    fixture_id: int
    home_team_name: str
    away_team_name: str
    actual_result: int
    predicted_result: int | None = None
    season_fixture_count: int | None = None

# Define API endpoint to get fixtures for a specific season and page number
@app.get("/fixtures/", response_model=List[FixtureListItem])
async def get_fixtures(season_id: int, page_number: int, db: Session = Depends(get_db)):
    fixtures = db.query(Fixture).filter(Fixture.season_id == season_id).offset((page_number - 1) * 10).limit(10).all()
    season_fixture_count = db.query(Fixture).filter(Fixture.season_id == season_id).count()
    fixture_data = []
    for fixture in fixtures:
        home_team = db.query(Team).filter(Team.team_id == fixture.home_team_id).first()
        away_team = db.query(Team).filter(Team.team_id == fixture.away_team_id).first()
        prediction = db.query(Prediction).filter(Prediction.fixture_id == fixture.fixture_id).first()
        predicted_result = prediction.predicted_result if prediction else None

        if fixture.winner_team_id == home_team.team_id:
            actual_result = 1
        elif fixture.winner_team_id == away_team.team_id:
            actual_result = 2
        else:
            actual_result = 0

        fixture_data.append({
            "fixture_id": fixture.fixture_id,
            "home_team_name": home_team.team_name if home_team else None,
            "away_team_name": away_team.team_name if away_team else None,
            "actual_result": actual_result,
            "predicted_result": predicted_result,
            "season_fixture_count": season_fixture_count
        })
    return fixture_data

# Run the FastAPI application using Uvicorn if the script is executed directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)