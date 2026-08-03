import 'bootstrap/dist/css/bootstrap.min.css';

export default function App() {
    const fixtures = [
        { fixture_id: 867946, season_id: 1, date: '2022-08-05 19:00:00.000000', home_team_id: 52, away_team_id: 42, winner_team_id: 42, home_goals_scored: 0, away_goals_scored: 2 },
        { fixture_id: 867947, season_id: 1, date: '2022-08-06 11:30:00.000000', home_team_id: 36, away_team_id: 40, winner_team_id: null, home_goals_scored: 2, away_goals_scored: 2 },
        { fixture_id: 867948, season_id: 1, date: '2022-08-06 14:00:00.000000', home_team_id: 35, away_team_id: 66, winner_team_id: 35, home_goals_scored: 2, away_goals_scored: 0 },
    ];

    
    return (
    <div className="container">
        <h1>Football Match Predictor</h1>
    </div>
    );
}