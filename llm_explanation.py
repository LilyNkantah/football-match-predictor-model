import anthropic
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY) 

def explain_prediction(prediction, htn, atn):
    if prediction.predicted_result == 1:
        predicted_result = "Home team win"
    elif prediction.predicted_result == 2:
        predicted_result = "Away team win"
    else:
        predicted_result = "Draw"

    prompt = f"""You are explaining a football match prediction to a casual fan.

    Predicted result: {predicted_result}
    Home Team: {htn}
    Away Team: {atn}
    Home form: {prediction.home_form}
    Away form: {prediction.away_form}
    Home H2H form: {prediction.home_h2h_score}
    Away H2H form: {prediction.away_h2h_score}

    Write a short, 1-2 sentence explanation of why the model made this prediction.
    Do not invent any facts beyond what's given above. Respond in plain text only, 
    no markdown formatting, no headers. Use the team names where appropriate."""

    response = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=200,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text