import os
from dotenv import load_dotenv
from supabase import create_client
import streamlit as st
from flask import Flask, jsonify, request
import google.generativeai as genai
import requests

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

#NON API FUNCTIONS

def get_ingredients_from_supabase():
    pantry_data = supabase.table('pantry').select('item_name', 'quantity', 'unit', 'days_in_pantry').execute()
    if pantry_data.data:
        return pantry_data.data
    else:
        return []

def ingredientsToDB(food_items):
    for item in food_items:
        data = {
            "item_name": item,
            "quantity": 1,
            "unit": "",
            "days_in_pantry": 7
        }
        print(f"Inserting item: {item}")
        try:
            response = supabase.table('pantry').insert(data).execute()
            print(f"Insert response: {response}")
            if response.status_code != 201:
                print(f"Failed to insert item: {response.content}")
            else:
                print(f"Inserted {item} into pantry successfully!")
        except Exception as e:
            print(f"Error inserting {item}: {e}")


app = Flask(__name__)

#USER API FUNCTIONS
'''
    - One to fetch all information
    - One to update information
'''

#Get All user information
@app.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = supabase.table('users').select('*').eq('id', user_id).execute()
    return jsonify(user.data)


@app.route('/get-recipe', methods=['GET'])
def get_recipe():
    ingredients = get_ingredients_from_supabase()
    if not ingredients:
        return jsonify({"error": "No ingredients found in pantry."}), 400
    recipe = generate_recipe(ingredients)
    return jsonify({"recipe": recipe})

@app.route('/user-receipts/<int:user_id>', methods=['GET'])
def get_user_receipts(user_id):
    receipts = supabase.table('receipts').select('*').eq('user_id', user_id).execute()
    return jsonify(receipts.data)

@app.route('/receipt-items/<int:receipt_id>', methods=['GET'])
def get_receiptItems(receipt_id):
    items = supabase.table('receipt_items').select('*').eq('receipt_id', receipt_id).execute()
    return jsonify(items.data)

if __name__ == "__main__":
    app.run(debug=True)
    print(get_user_info(26)) 
