import os
import easyocr
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

reader = easyocr.Reader(['en'])

def extract_text(image):
    result = reader.readtext(image, detail=0)
    text = "\n".join(result) if result else "No text detected."
    return text

def extract_food_items_with_gemini(text):
    prompt = (
        "Extract only the names of food items from the following text. "
        "Do not include quantities, prices, or extra words. Just return a comma-separated list of food names.\n\n"
        f"Text: '''{text}'''"
    )

    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt)
        result = response.text.strip()
        food_items = [item.strip() for item in result.split(",") if item.strip()]
        return food_items
    except Exception as e:
        return f"Error extracting food items: {e}"
