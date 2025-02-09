import os
from dotenv import load_dotenv
from supabase import create_client
import streamlit as st
from flask import Flask, jsonify
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def get_ingredients_from_supabase():
    pantry_data = supabase.table('pantry').select('item_name', 'quantity', 'unit', 'days_in_pantry').execute()
    if pantry_data.data:
        return pantry_data.data
    else:
        return []

app = Flask(__name__)

# recipe generation
def generate_recipe(ingredients):
    ingredients_list = ", ".join([f"{item['quantity']} {item['unit']} {item['item_name']}" for item in ingredients])
    try:
        response = genai.generate_content(
            model="gemini-pro",
            messages=[{"role": "system", "content": f"Generate a recipe using the following ingredients: {ingredients_list}"}]
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"Error generating recipe: {str(e)}"

# Example to test recipe generation (you can remove this later)
print(generate_recipe([{"item_name": "milk", "quantity": 1, "unit": "cup", "days_in_pantry": 5}]))

@app.route('/get-recipe', methods=['GET'])
def get_recipe():
    ingredients = get_ingredients_from_supabase()
    if not ingredients:
        return jsonify({"error": "No ingredients found in pantry."}), 400
    recipe = generate_recipe(ingredients)
    return jsonify({"recipe": recipe})

if __name__ == "__main__":
    app.run(debug=True)
