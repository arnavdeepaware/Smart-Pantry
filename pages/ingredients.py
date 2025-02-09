import streamlit as st
import pandas as pd
from backend.views import get_ingredients_from_supabase

def show_ingredients():
    st.title("Ingredients")
    st.write("Welcome to the ingredients page!")
    
    st.subheader("My Ingredients")
    st.write("Here's a list of the ingredients currently in your pantry:")

    # Fetch ingredients from Supabase
    ingredients = get_ingredients_from_supabase()

    # If data is available, display it
    if ingredients:
        # Convert the fetched data to a pandas DataFrame
        df = pd.DataFrame(ingredients)
        
        # Ensure all data columns are present
        df = df[['item_name', 'quantity', 'unit', 'days_in_pantry']]
        
        # Rename columns to match the desired table format
        df.columns = ["Ingredient", "Quantity", "Unit", "Days in Pantry"]
        
        # Handle search functionality
        ingredient_search = st.text_input("Search for any item here... 🔍", "")
        if ingredient_search:
            df = df[df['Ingredient'].str.contains(ingredient_search, case=False)]
        
        # Show the table
        st.table(df)
    else:
        st.write("No ingredients found.")

    # Popup to add item
    def show_add_item_popup():
        with st.container():
            st.subheader("Add Item")
            item_name = st.text_input("Add Item Name")
            item_quantity = st.number_input("Add Item Quantity", min_value=1)
            item_unit = st.text_input("Add Item Unit")
            
            if st.button("Submit"):
                st.write(f"Item Name: {item_name}")
                st.write(f"Item Quantity: {item_quantity}")
                st.write(f"Item Unit: {item_unit}")
                st.success("Item Added!")
                # You can also implement the function to actually add the item to Supabase here.

    if st.button("Add Item"):
        show_add_item_popup()

    # Styling
    st.markdown(
    """ <style>
        table td, table th {
            text-align: center !important;
        }
        .align-right {
            display: flex;
            justify-content: flex-end;
        }
    </style> """, 
    unsafe_allow_html=True
    )

