import streamlit as st
import requests

FLASK_API_URL = "http://127.0.0.1:5000"

#st.set_page_config(page_title="Suggested Recipes", page_icon="🍽️", layout="centered")

def show_recipes_board():
    
    st.title("Suggested Recipes")
    st.write("Check out some suggested recipes based on your pantry.")
    
    if st.button("Generate Recipe 🍳"):
        with st.spinner("Generating your recipe..."):
            try:
                api_response = requests.get(f"{FLASK_API_URL}/get-recipe")
                if api_response.status_code == 200:
                    recipe = api_response.json().get("recipe", "No recipe found.")
                    st.success("Recipe Generated!")
                    st.write(recipe)
                else:
                    st.error("⚠️ No ingredients found in pantry.")
            except requests.exceptions.RequestException as e:
                st.error(f"Error: {e}")

show_recipes_board()
