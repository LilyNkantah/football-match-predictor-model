import database
import fixture_manipulation


def build_training_data(db):
    rows = []

    for fixture in db.query(database.Fixture).all():
        home_fixtures = database.get_last_5_fixtures(db, fixture.home_team_id, fixture.date)
        # recent form
        home_form = fixture_manipulation.calculate_form_score(home_fixtures, fixture.home_team_id)
        away_fixtures = database.get_last_5_fixtures(db, fixture.away_team_id, fixture.date)
        away_form = fixture_manipulation.calculate_form_score(away_fixtures, fixture.away_team_id)
        # h2h performance
        h2hs = database.get_last_5_h2hs(db, fixture.home_team_id, fixture.away_team_id, fixture.date)
        t1_h2h_score = fixture_manipulation.calculate_h2h_score(h2hs, fixture.home_team_id)
        t2_h2h_score = fixture_manipulation.calculate_h2h_score(h2hs, fixture.away_team_id)
        # goals scored/conceded across h2hs

        # actual label model needs to predict - match outcome
        if fixture.winner_team_id == fixture.home_team_id:
            actual_outcome = 1 # 1 for home team win
        elif fixture.winner_team_id == fixture.away_team_id:
            actual_outcome = 2 # 2 for away team win
        else:
            actual_outcome = 0 # 0 for draw
        rows.append((fixture.fixture_id, fixture.season_id, home_form, away_form, t1_h2h_score, t2_h2h_score, actual_outcome))
    return rows
        