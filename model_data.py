import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import database
import fixture_manipulation

DATABASE_URL = "sqlite:///./football_predictor.db"  # SQLite database URL for local development
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = sqlalchemy.orm.declarative_base()

def build_training_data(db):
    rows = []

    for fixture in db.query(database.Fixture).all():
        home_fixtures = database.get_last_5_fixtures(db, fixture.home_team_id, fixture.date)
        home_form = fixture_manipulation.calculate_form_score(home_fixtures, fixture.home_team_id)
        away_fixtures = database.get_last_5_fixtures(db, fixture.away_team_id, fixture.date)
        away_form = fixture_manipulation.calculate_form_score(away_fixtures, fixture.away_team_id)
        h2hs = database.get_last_5_h2hs(db, fixture.home_team_id, fixture.away_team_id, fixture.date)
        h2h_score = fixture_manipulation.calculate_h2h_score(h2hs, fixture.home_team_id, fixture.away_team_id)
        if fixture.winner_team_id == fixture.home_team_id:
            actual_outcome = 1 # 1 for home team win
        elif fixture.winner_team_id == fixture.away_team_id:
            actual_outcome = 2 # 2 for away team win
        else:
            actual_outcome = 0 # 0 for draw
        rows.append((fixture.fixture_id, fixture.season_id, home_form, away_form, h2h_score, actual_outcome))
    return rows
        
        

if __name__ == "__main__":
    db = SessionLocal()
    try:
        build_training_data(db)
        pass
    finally:
        db.close()