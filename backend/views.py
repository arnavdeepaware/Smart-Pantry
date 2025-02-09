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
@app.route('/user/<uuid:user_id>', methods=['GET'])
def get_user(user_id):
    user = supabase.table('users').select('*').eq('auth_id', user_id).execute()
    return jsonify(user.data)

@app.route('/user/update/<uuid:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.json
    # Fetch current user data
    current_user = supabase.table('users').select('*').eq('auth_id', user_id).execute()
    
    if not current_user.data:
        return jsonify({"error": "User not found"}), 404

    current_user_data = current_user.data[0]

    # Update only the fields provided in the input
    updated_data = {**current_user_data, **data}

    # Ensure data types are correct
    if 'current_weight' in updated_data:
        updated_data['current_weight'] = int(updated_data['current_weight'])
    if 'target_weight' in updated_data:
        updated_data['target_weight'] = float(updated_data['target_weight'])
    if 'current_height' in updated_data:
        updated_data['current_height'] = float(updated_data['current_height'])
    if 'age' in updated_data:
        updated_data['age'] = int(updated_data['age'])

    # Remove 'id' field if present to avoid updating the primary key
    if 'id' in updated_data:
        del updated_data['id']

    response = supabase.table('users').update(updated_data).eq('auth_id', user_id).execute()
    return jsonify(response.data)

#OTHERS
@app.route('/user-receipts/<int:user_id>', methods=['GET'])
def get_user_receipts(user_id):
    receipts = supabase.table('receipts').select('*').eq('user_id', user_id).execute()
    return jsonify(receipts.data)

@app.route('/receipt-items/<int:receipt_id>', methods=['GET'])
def get_receiptItems(receipt_id):
    items = supabase.table('receipt_items').select('*').eq('receipt_id', receipt_id).execute()
    return jsonify(items.data)

def get_user_id():
    user_id = supabase.table('users').select('*').eq('email', email).execute()
    print(user_id)


if __name__ == "__main__":
    app.run(debug=True)

