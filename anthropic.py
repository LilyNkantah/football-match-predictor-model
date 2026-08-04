import anthropic
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY) 

def explain_prediction(prediction_data):
    # check if llm_explanation already exists
    if prediction_data.llm_explanation is not None:
        return prediction_data.llm_explanation
    else: # generate llm_explanation using anthropic API
        if prediction_data[1] == 1:
            predicted_result = "Home team win"
        elif prediction_data[1] == 2:
            predicted_result = "Away team win"
        else:
            predicted_result = "Draw"
        prompt = f"""You are explaining a football match prediction to a casual fan.
        
        
        Predicted result: {predicted_result}
        Home form: {prediction_data[2]}
        Away form: {prediction_data[3]}
        Home H2H form: {prediction_data[4]}
        Away H2H form: {prediction_data[5]}
        Other features: {prediction_data[6:-1]}
        
        Write a short, 1-2 sentence explanation of why the model made this prediction. 
        Do not invent any facts beyond what's given above.""" # constrain the model to only the structured data I hand it

        response = client.messages.create(
            model="claude-haiku-4-5",
            max_tokens=200,
            messages=[{"role": "user", "content": prompt}]
        )

        return response.content[0].text