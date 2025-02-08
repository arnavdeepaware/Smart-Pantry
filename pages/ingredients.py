import streamlit as st


def show_ingredients():
    st.title("Ingredients")
    st.write("Welcome to the ingredients page!")
    
    st.subheader("My Ingredients")
    st.write("Here's a list of the ingredients currently in your pantry:")
    
    st.table({
        "Ingredient": ["Milk", "Eggs", "Spinach", "Chicken Breast"],
        "Quantity": [1, 12, 3, 2],
        "Calories": [150, 72, 23, 165],
        "Expiry Date": ["2024-01-10", "2024-02-01", "2024-02-05", "2024-01-20"],
        "Suggested Recipes": [
            "https://www.example.com/milk-recipes",
            "https://www.example.com/eggs-recipes",
            "https://www.example.com/spinach-recipes",
            "https://www.example.com/chicken-recipes",
        ],
        "Nearby Locations": [
            "https://www.example.com/nearby-milk-store",
            "https://www.example.com/nearby-eggs-store",
            "https://www.example.com/nearby-spinach-store",
            "https://www.example.com/nearby-chicken-store",
        ]
    })