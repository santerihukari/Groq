import requests

# Define the API endpoint
API_URL = "http://127.0.0.1:8000/translate"  # Replace with your actual API URL if hosted remotely

# Ask the user for input
text_to_translate = input("Enter the text to translate: ")
target_language = input("Enter the target language (e.g., French, Spanish): ")

# Create the request payload
payload = {
    "text": text_to_translate,
    "target_language": target_language
}

# Send a POST request to the API
try:
    response = requests.post(API_URL, json=payload)
    response.raise_for_status()  # Raise an error for bad status codes

    # Parse the response JSON
    translated_text = response.json().get("translated_text")
    print(f"\nTranslated Text ({target_language}): {translated_text}")

except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")