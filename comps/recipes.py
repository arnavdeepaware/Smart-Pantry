import streamlit as st
import requests
from backend.controllers.recipe_generation import get_recipe_instructions

FLASK_API_URL = "http://127.0.0.1:5000"

# Define CSS styles
st.markdown("""
<style>
    .recipe-details {
        text-align: left !important;
        padding-left: 0 !important;
        margin-left: 0 !important;
    }
    .recipe-details p {
        text-align: left !important;
        padding-left: 0 !important;
        margin-left: 0 !important;
    }
</style>
""", unsafe_allow_html=True)

# Sample Data
test_ingredients = [
    {"name": "Eggs", "expiry_date": "2024-02-15"},
    {"name": "Milk", "expiry_date": "2024-02-12"},
    {"name": "Bread", "expiry_date": "2024-02-10"},
    {"name": "Rice", "expiry_date": "2024-03-01"},
    {"name": "Chicken", "expiry_date": "2024-02-11"},
    {"name": "Vegetables", "expiry_date": "2024-02-09"},
    {"name": "Soy Sauce", "expiry_date": "2024-05-01"},
    {"name": "Pasta", "expiry_date": "2024-04-01"}
]

past_recipes = [
    {
        "name": "Vegetable Stir Fry",
        "calories": 380,
        "instructions": "1. Chop vegetables\n2. Heat oil in pan\n3. Stir fry vegetables\n4. Add sauce",
        "ingredients": ["Mixed Vegetables", "Soy Sauce", "Rice"]
    },
    {
        "name": "Chicken Rice Bowl",
        "calories": 450,
        "instructions": "1. Cook rice\n2. Grill chicken\n3. Prepare vegetables\n4. Assemble bowl",
        "ingredients": ["Chicken", "Rice", "Vegetables"]
    },
    {
        "name": "Pasta Primavera",
        "calories": 420,
        "instructions": "1. Boil pasta\n2. Sauté vegetables\n3. Mix with sauce\n4. Garnish",
        "ingredients": ["Pasta", "Mixed Vegetables", "Olive Oil"]
    }
]

def show_recipes_board():
    st.title("Suggested Recipes")
    st.write("Check out some suggested recipes based on your pantry.")
    
    # Initialize session state to store recipes and selected recipe
    if 'recipes' not in st.session_state:
        st.session_state.recipes = []
    if 'selected_recipe' not in st.session_state:
        st.session_state.selected_recipe = None
    
    if st.button("Generate Recipe 🍳"):
        with st.spinner("Generating your recipe..."):
            try:
                recipe = get_recipe_instructions(
                    list_of_ingredients=test_ingredients,
                    meal_type="Lunch",
                    daily_calorie_intake=2000,
                    dietary_restrictions="None"
                )
                if recipe and recipe.get('recipes'):
                    st.success("Recipe Generated!")
                    st.session_state.recipes = []  # Clear previous recipes
                    
                    for r in recipe['recipes']:
                        recipe_dict = {
                            "name": r['name'],
                            "ingredients": r['ingredients_used'],
                            "instructions": r['instructions'],
                            "total_calories": r.get('total_calories', 'N/A'),
                            "cooking_time": r['cooking_time']
                        }
                        st.session_state.recipes.append(recipe_dict)
                else:
                    st.error("⚠️ No ingredients found in pantry.")
            except requests.exceptions.RequestException as e:
                st.error(f"Error: {e}")
    
    # Display recipe buttons if recipes exist
    if st.session_state.recipes:
        cols = st.columns(3)
        for idx, recipe in enumerate(st.session_state.recipes):
            with cols[idx]:
                if st.button(f"{recipe['name']}", key=f"recipe_{idx}"):
                    st.session_state.selected_recipe = recipe
    
    # Create recipe display container at the bottom
    st.write("---")  # Horizontal line separator
    recipe_container = st.container()
    with recipe_container:
        if not st.session_state.recipes:
            st.markdown("""
                <div style="text-align: left;">
                <h3>Your Recipe will appear here...</h3>
                <p>Click 'Generate Recipe' to get started!</p>
                </div>
            """, unsafe_allow_html=True)
        elif st.session_state.selected_recipe:
            recipe = st.session_state.selected_recipe
            st.markdown(f"""
                <div style="text-align: left;">
                <h3>{recipe['name']}</h3>
                <p><strong>Total Calories:</strong> {recipe['total_calories']}</p>
                <p><strong>Cooking Time:</strong> {recipe['cooking_time']}</p>
                <p><strong>Ingredients Used:</strong></p>
                </div>
            """, unsafe_allow_html=True)
            
            for ingredient in recipe["ingredients"]:
                st.markdown(f"""
                    <div style='text-align: left; margin-left: 20px;'>
                    • {ingredient['name']}: {ingredient['quantity']}
                    </div>
                """, unsafe_allow_html=True)
            
            st.markdown("""
                <div style="text-align: left;">
                <p><strong>Instructions:</strong></p>
                </div>
            """, unsafe_allow_html=True)
            
            for step in recipe["instructions"]:
                st.markdown(f"""
                    <div style='text-align: left; margin-left: 20px;'>
                    {step}
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
                <div style="text-align: left;">
                <h3>Select a recipe to view details</h3>
                </div>
            """, unsafe_allow_html=True)

    # Past Recipes Section
    st.write("---")
    with st.container():
        st.subheader("Past Recipes")
        
        for i, recipe in enumerate(past_recipes):
            with st.expander(f"🍽️ {recipe['name']} • {recipe['calories']} kcal"):
                st.markdown("""
                    <div style="text-align: left;">
                    <strong>Ingredients:</strong>
                    </div>
                """, unsafe_allow_html=True)
                for ingredient in recipe['ingredients']:
                    st.markdown(f"""
                        <div style='text-align: left; margin-left: 20px;'>
                        • {ingredient}
                        </div>
                    """, unsafe_allow_html=True)
                
                st.markdown("""
                    <div style="text-align: left;">
                    <strong>Instructions:</strong>
                    </div>
                """, unsafe_allow_html=True)
                
                instructions = recipe['instructions'].split('\n')
                for instruction in instructions:
                    st.markdown(f"""
                        <div style='text-align: left; margin-left: 20px;'>
                        {instruction}
                        </div>
                    """, unsafe_allow_html=True)

show_recipes_board()