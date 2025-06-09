import requests # For making HTTP requests (e.g., to the Gemini API)
import json     # For working with JSON data (serializing requests, parsing responses)
import os       # For potentially getting API key from environment variables (more secure)

def translate_english_to_japanese(english_text: str, api_key: str) -> str:
    """
    Translates English text to Japanese using the Google Gemini API.

    Args:
        english_text: The English text to be translated.
        api_key: Your Google Gemini API Key.

    Returns:
        The Japanese translation as a string, or an error message if translation fails.
    """
    # Define the API endpoint for the Gemini API's text generation.
    # We're using the 'gemini-2.0-flash' model as an example.
    # Note: In a real application, consider using environment variables for the API key
    # instead of concatenating it directly into the URL for better security.
    api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"

    # Construct the JSON payload for the API request.
    # We instruct the model to translate the given English text to Japanese.
    # The prompt specifically asks for only the Japanese text to simplify parsing.
    request_payload = {
        "contents": [
            {
                "role": "user",
                "parts": [
                    {
                        "text": f"Translate the following English text to Japanese (only provide the Japanese text):\n\n\"{english_text}\""
                    }
                ]
            }
        ]
    }

    # Define the HTTP headers, specifying that we are sending and expecting JSON.
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    try:
        # Make the POST request to the Gemini API.
        # json=request_payload automatically serializes the dict to JSON.
        response = requests.post(api_url, headers=headers, json=request_payload)

        # Raise an exception for bad status codes (4xx or 5xx)
        response.raise_for_status()

        # Parse the JSON response from the API.
        response_json = response.json()

        # Navigate through the JSON structure to extract the translated text.
        # The typical path for Gemini API's generateContent response is:
        # response_json["candidates"][0]["content"]["parts"][0]["text"]
        if (response_json and
            "candidates" in response_json and
            len(response_json["candidates"]) > 0 and
            "content" in response_json["candidates"][0] and
            "parts" in response_json["candidates"][0]["content"] and
            len(response_json["candidates"][0]["content"]["parts"]) > 0 and
            "text" in response_json["candidates"][0]["content"]["parts"][0]):
            
            # Return the extracted Japanese text
            return response_json["candidates"][0]["content"]["parts"][0]["text"]
        else:
            # If the expected structure is not found, print the full response for debugging.
            print(f"Error: Unexpected API response structure. Raw response:\n{response_json}")
            return "Translation failed: API response structure was unexpected."

    except requests.exceptions.RequestException as e:
        # Catch network-related errors (e.g., connection refused, timeouts)
        print(f"Error: Network or HTTP request failed: {e}")
        return "Translation failed due to network error."
    except json.JSONDecodeError as e:
        # Catch errors during JSON parsing
        print(f"Error: Failed to parse JSON response: {e}")
        print(f"Raw response received: {response.text if 'response' in locals() else 'No response'}")
        return "Translation failed: Invalid JSON response from API."
    except Exception as e:
        # Catch any other unexpected errors
        print(f"An unexpected error occurred: {e}")
        return "Translation failed due to an unexpected error."

if __name__ == "__main__":
    print("--- English to Japanese Translator ---")
    print("This program uses the Google Gemini API for translation.")

    # It's more secure to get the API key from an environment variable.
    # As a fallback, it will prompt the user if the environment variable is not set.
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        api_key = input("Please enter your Google Gemini API Key: ")
    else:
        print("Using API key from GEMINI_API_KEY environment variable.")

    print("\nEnter English text to translate (type 'exit' to quit):")

    # Loop to continuously accept English input and provide Japanese translation
    while True:
        english_input = input("\nEnglish: ")

        # Check if the user wants to exit
        if english_input.lower() == "exit":
            break

        # Check if the input is empty
        if not english_input.strip():
            print("Please enter some text to translate.")
            continue

        # Call the translation function
        japanese_translation = translate_english_to_japanese(english_input, api_key)
        print(f"Japanese: {japanese_translation}")

    print("\nExiting translator. Goodbye!")
