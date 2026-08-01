from datetime import datetime

from sqlalchemy import DateTime, create_engine, Column, Integer, String
import sqlalchemy
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel

import db_dictionaries
import fixture_manipulation

# Create a FastAPI application instance and configure the database connection using SQLAlchemy.
#app = FastAPI()
DATABASE_URL = "sqlite:///./football_predictor.db"  # SQLite database URL for local development
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = sqlalchemy.orm.declarative_base()

# Define the database model

# TEAMS
class Team(Base):
    __tablename__ = "teams"
    id = Column(Integer, primary_key=True, index=True)
    team_id = Column(Integer, unique=True, index=True)
    team_name = Column(String, index=True)

# SEASONS
class Season(Base):
    __tablename__ = "seasons"
    id = Column(Integer, primary_key=True, index=True)
    start_year = Column(Integer, index=True)
    end_year = Column(Integer, index=True)

# SEASONS PLAYED
class SeasonPlayed(Base):
    __tablename__ = "seasons_played"
    team_id = Column(Integer, sqlalchemy.ForeignKey("teams.team_id"), primary_key=True)
    season_id = Column(Integer, sqlalchemy.ForeignKey("seasons.id"), primary_key=True)

# FIXTURES
class Fixture(Base):
    __tablename__ = "fixtures"
    fixture_id = Column(Integer, primary_key=True, index=True)
    season_id = Column(Integer, sqlalchemy.ForeignKey("seasons.id"))
    date = Column(DateTime, index=True)
    home_team_id = Column(Integer, sqlalchemy.ForeignKey("teams.team_id"))
    away_team_id = Column(Integer, sqlalchemy.ForeignKey("teams.team_id"))
    winner_team_id = Column(Integer, sqlalchemy.ForeignKey("teams.team_id"), nullable=True)  # Nullable to allow for draws or unplayed matches
    home_goals_scored = Column(Integer, nullable=True)  # Nullable to allow for unplayed matches
    away_goals_scored = Column(Integer, nullable=True)  # Nullable to allow for unplayed matches

# HEAD TO HEADS
class HeadToHead(Base):
    __tablename__ = "head_to_heads"
    id = Column(Integer, primary_key=True, index=True)
    current_fixture_id = Column(Integer, sqlalchemy.ForeignKey("fixtures.fixture_id"))
    past_fixture_date = Column(DateTime, index=True)
    team1_id = Column(Integer, sqlalchemy.ForeignKey("teams.team_id"))
    team2_id = Column(Integer, sqlalchemy.ForeignKey("teams.team_id"))
    season_id = Column(Integer, sqlalchemy.ForeignKey("seasons.id"))
    winner_team_id = Column(Integer, sqlalchemy.ForeignKey("teams.team_id"), nullable=True) 
    team1_goals_scored = Column(Integer, nullable=True) 
    team2_goals_scored = Column(Integer, nullable=True)

# Create the database tables
Base.metadata.create_all(bind=engine)

# Define Pydantic models for request and response data validation

# TEAMS
class TeamCreate(BaseModel):
    team_id: int
    team_name: str

class TeamResponse(TeamCreate):
    id: int
    team_id: int
    team_name: str

# SEASONS
class SeasonCreate(BaseModel):
    start_year: int
    end_year: int

class SeasonResponse(SeasonCreate):
    id: int
    start_year: int
    end_year: int

# SEASONS PLAYED
class SeasonPlayedCreate(BaseModel):
    team_id: int
    season_id: int

class SeasonPlayedResponse(SeasonPlayedCreate):
    team_id: int
    season_id: int

# FIXTURES
class FixtureCreate(BaseModel):
    fixture_id: int
    season_id: int
    date: datetime
    home_team_id: int
    away_team_id: int
    winner_team_id: int | None = None  # Optional field to allow for draws or unplayed matches
    home_goals_scored: int | None = None  # Optional field to allow for unplayed matches
    away_goals_scored: int | None = None

class FixtureResponse(FixtureCreate):
    fixture_id: int
    season_id: int
    date: datetime
    home_team_id: int
    away_team_id: int
    winner_team_id: int | None = None
    home_goals_scored: int | None = None
    away_goals_scored: int | None = None

# HEAD TO HEADS
class HeadToHeadCreate(BaseModel):
    current_fixture_id: int
    past_fixture_date: datetime
    team1_id: int
    team2_id: int
    season_id: int
    winner_team_id: int | None = None
    team1_goals_scored: int | None = None
    team2_goals_scored: int | None = None

class HeadToHeadResponse(HeadToHeadCreate):
    id: int
    current_fixture_id: int
    past_fixture_date: datetime
    team1_id: int
    team2_id: int
    season_id: int
    winner_team_id: int | None = None
    team1_goals_scored: int | None = None
    team2_goals_scored: int | None = None

# INSERTING HISTORICAL DATA INTO THE TABLES
def add_teams_to_db(db):
    for t_id, t_name in db_dictionaries.teams.items():
        if db.query(Team).filter(Team.team_id == t_id).first() is None:
            db_team = Team(team_id=t_id, team_name=t_name)
            db.add(db_team)
            db.commit()
            db.refresh(db_team)
        else:
            print("Team already exists in database.")
    print("Teams added to database successfully.")

def add_seasons_to_db(db):
    for s_year, e_year in db_dictionaries.seasons.values():
        if db.query(Season).filter(Season.start_year == s_year).first() is None:
            db_season = Season(start_year=s_year, end_year=e_year)
            db.add(db_season)
            db.commit()
            db.refresh(db_season)
        else:
            print("Season already exists in database.")
    print("Seasons added to database successfully.")

def add_seasons_played_to_db(db):
    for t_id, s_list in db_dictionaries.seasons_played.items():
        for s in s_list:
            db_season_played = db.query(Season).filter(Season.start_year == s).first()
            if not db_season_played is None: 
                db_season_played_id = db_season_played.id
                if db.query(SeasonPlayed).filter(SeasonPlayed.team_id == t_id, SeasonPlayed.season_id == db_season_played_id).first() is None:
                    db_team_played = SeasonPlayed(team_id=t_id, season_id=db_season_played_id)
                    db.add(db_team_played)
                    db.commit()
                    db.refresh(db_team_played)
                else:
                    print("Season played by this team already exists in database.")
        print(f"Seasons played by team with ID {t_id} added to database successfully.")

def add_fixtures_to_db(db):
    fix_info_2022 = fixture_manipulation.extract_fixture_info_for_db(2022)
    fix_info_2023 = fixture_manipulation.extract_fixture_info_for_db(2023)
    fix_info_2024 = fixture_manipulation.extract_fixture_info_for_db(2024)
    infos = [fix_info_2022, fix_info_2023, fix_info_2024]

    for inf in infos:
        for fix in inf:
            # query into season table to get s_id for each season
            if not db.query(Season).filter(Season.start_year == fix[1]).first() is None:
                s_id = (db.query(Season).filter(Season.start_year == fix[1]).first()).id
                if db.query(Fixture).filter(Fixture.date == fix[2], Fixture.home_team_id == fix[3], Fixture.away_team_id == fix[4]).first() is None:
                    db_fixture = Fixture(fixture_id=fix[0], season_id=s_id, date=fix[2], home_team_id=fix[3], 
                                        away_team_id=fix[4], winner_team_id=fix[5], 
                                        home_goals_scored=fix[6], away_goals_scored=fix[7])
                    db.add(db_fixture)
                    db.commit()
                    db.refresh(db_fixture)
                else:
                    print("Fixture already exists in database.")
        print("Fixtures for season added to database successfully.")

def add_h2hs_to_db(db):
    # get list of all fixtures from fixture table
    fixtures = db.query(Fixture).all()
    
    for fixture in fixtures:
        current_f_id = fixture.fixture_id
        # calculate which season the fixture belongs to
        dy = (fixture.date.year) % 100
        dm = fixture.date.month
        if dm < 7:
            start_year = dy - 1
            end_year = dy
        else:
            start_year = dy
            end_year = dy + 1

        h2h_info = fixture_manipulation.extract_h2h_info_for_db(start_year, end_year, fixture.home_team_id, 
                                                                fixture.away_team_id, fixture.date)

        # input data into h2h table
        for h2h in h2h_info:
            if db.query(HeadToHead).filter(HeadToHead.past_fixture_date == h2h[0]).first() is None:
                db_h2h = HeadToHead(current_fixture_id=current_f_id, past_fixture_date=h2h[0], 
                                    team1_id=h2h[1], team2_id=h2h[2], season_id=h2h[3], winner_team_id=h2h[4], 
                                    team1_goals_scored=h2h[5], team2_goals_scored=h2h[6])
                db.add(db_h2h)
                db.commit()
                db.refresh(db_h2h)
            else:
                print("H2H for this matchup already exists in database.")
        print("H2Hs added to database successfully.")

# QUERIES    
# for use in calculating recent form score
def get_last_5_fixtures(db, tid, fdate):
    fixtures = db.query(Fixture).filter(Fixture.date < fdate, 
                                        sqlalchemy.or_(Fixture.home_team_id == tid, 
                                        Fixture.away_team_id == tid)
                                        ).order_by(Fixture.date).all()
    fixtures = fixtures[-5:]
    return fixtures

# for use in calculating h2h score
def get_last_5_h2hs(db, t1id, t2id, fdate):
    h2hs = db.query(HeadToHead).filter(HeadToHead.past_fixture_date < fdate, 
                                       sqlalchemy.and_(HeadToHead.team1_id == t1id, 
                                                       HeadToHead.team2_id == t2id)
                                                       ).order_by(HeadToHead.past_fixture_date).all()
    h2hs = h2hs[-5:]
    return h2hs
