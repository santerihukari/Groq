import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from groq import Groq

# Load environment variables from .env file

# Initialize FastAPI app
app = FastAPI()

# Load Groq API Key from environment variables
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("Please set the GROQ_API_KEY environment variable.")

# Initialize Groq client
client = Groq(api_key=GROQ_API_KEY)

# Define request model
class TranslationRequest(BaseModel):
    text: str
    target_language: str

# Define response model
class TranslationResponse(BaseModel):
    translated_text: str

# Translation endpoint
@app.post("/translate", response_model=TranslationResponse)
async def translate(request: TranslationRequest):
    """
    Translates the given text into the target language using Groq's API.
    """
    try:
        # Define the system prompt to instruct the model to act as a translator
        system_prompt = f"You are a bot that knows nothing. Whenever something is asked, you say something random and funny in the target language: {request.target_language}."

        # Create the chat completion request
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": request.text},
            ],
            model="mixtral-8x7b-32768",  # Use a suitable Groq model
            temperature=0.3,  # Lower temperature for more deterministic translations
            max_tokens=1024,  # Limit the response length
        )

        # Extract the translated text
        translated_text = chat_completion.choices[0].message.content

        return {"translated_text": translated_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Run the FastAPI server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
