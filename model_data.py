import database
import fixture_manipulation


def build_training_data(db):
    """Assemble one feature row per fixture (form, H2H, goals, and outcome) for use in training and predicting with the model."""
    rows = []

    for fixture in db.query(database.Fixture).all():
        home_fixtures = database.get_last_5_fixtures(
            db, fixture.home_team_id, fixture.date
        )
        # recent form
        home_form = fixture_manipulation.calculate_form_score(
            home_fixtures, fixture.home_team_id
        )
        away_fixtures = database.get_last_5_fixtures(
            db, fixture.away_team_id, fixture.date
        )
        away_form = fixture_manipulation.calculate_form_score(
            away_fixtures, fixture.away_team_id
        )
        # h2h performance
        h2hs = database.get_last_5_h2hs(
            db, fixture.home_team_id, fixture.away_team_id, fixture.date
        )
        t1_h2h_score = fixture_manipulation.calculate_h2h_score(
            h2hs, fixture.home_team_id
        )
        t2_h2h_score = fixture_manipulation.calculate_h2h_score(
            h2hs, fixture.away_team_id
        )
        # goals scored/conceded across last 5 fixtures
        [t1_home_form_gs, t1_home_form_gc, t1_away_form_gs, t1_away_form_gc] = (
            fixture_manipulation.calculate_goals_for_form(
                home_fixtures, fixture.home_team_id
            )
        )
        [t2_home_form_gs, t2_home_form_gc, t2_away_form_gs, t2_away_form_gc] = (
            fixture_manipulation.calculate_goals_for_form(
                away_fixtures, fixture.away_team_id
            )
        )
        # goals scored/conceded across last 5 h2hs
        [t1_home_h2h_gs, t1_home_h2h_gc, t1_away_h2h_gs, t1_away_h2h_gc] = (
            fixture_manipulation.calculate_goals_for_h2h(h2hs, fixture.home_team_id)
        )
        [t2_home_h2h_gs, t2_home_h2h_gc, t2_away_h2h_gs, t2_away_h2h_gc] = (
            fixture_manipulation.calculate_goals_for_h2h(h2hs, fixture.away_team_id)
        )
        # actual label model needs to predict - match outcome
        if fixture.winner_team_id == fixture.home_team_id:
            actual_outcome = 1  # 1 for home team win
        elif fixture.winner_team_id == fixture.away_team_id:
            actual_outcome = 2  # 2 for away team win
        else:
            actual_outcome = 0  # 0 for draw
        rows.append(
            (
                fixture.fixture_id,
                fixture.season_id,
                home_form,
                away_form,
                t1_h2h_score,
                t2_h2h_score,
                t1_home_form_gs,
                t1_home_form_gc,
                t1_away_form_gs,
                t1_away_form_gc,
                t2_home_form_gs,
                t2_home_form_gc,
                t2_away_form_gs,
                t2_away_form_gc,
                t1_home_h2h_gs,
                t1_home_h2h_gc,
                t1_away_h2h_gs,
                t1_away_h2h_gc,
                t2_home_h2h_gs,
                t2_home_h2h_gc,
                t2_away_h2h_gs,
                t2_away_h2h_gc,
                actual_outcome,
            )
        )
    return rows
