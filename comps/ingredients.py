import streamlit as st
import pandas as pd
from backend.views import get_ingredients_from_supabase
from comps.add_ingredient import show_add_ingredient
import numpy as np
from PIL import Image
import backend.recognize as recognize  # Add this import
from comps.scanner import img_to_food_items
import os
from dotenv import load_dotenv
from supabase import create_client


load_dotenv()

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


if 'sub_page' not in st.session_state:
    st.session_state.sub_page = None
if 'add_clicked' not in st.session_state:
    st.session_state.add_clicked = False
if 'manual_add_clicked' not in st.session_state:
    st.session_state.manual_add_clicked = False
if 'upload_window_open' not in st.session_state:
    st.session_state.upload_window_open = False

# Modify the show_scanner_container function


def show_scanner_container():
    with st.container():
        st.subheader("Receipt Scanner")
        uploaded_file = st.file_uploader("Upload a receipt image", type=["png", "jpg", "jpeg"])
        if uploaded_file:
            # Process the image
            with st.spinner('Processing receipt...'):
                food_items = img_to_food_items(uploaded_file)
                if food_items:
                    st.success('Receipt processed successfully! 🎉')

                    # Parse food items
                    parsed_items = []
                    for item in food_items:
                        try:
                            parts = item.rsplit(' ', 2)
                            if len(parts) == 3:
                                food_name, price, unit = parts
                                quantity = 1
                            elif len(parts) == 2:
                                food_name, price = parts
                                unit = None
                                quantity = 1
                            else:
                                continue

                            parsed_items.append((food_name, float(price), quantity, unit))
                        except ValueError:
                            st.warning(f"Skipping invalid item: {item}")
                            continue

                    if parsed_items:
                        try:
                            response = supabase.table("receipt_items").insert(
                                [{"item_name": food_name, "quantity": quantity, "unit": unit} for food_name, price, quantity, unit in parsed_items]
                            ).execute()

                            if response.status_code == 201:
                                st.success("Food items successfully added to the database!")
                            else:
                                st.error(f"Failed to add items to the database. Status: {response.status_code}")
                        except Exception as e:
                            st.error(f"Error inserting into database: {e}")
                    else:
                        st.warning("No valid food items to add.")
                else:
                    st.error("No food items found in the receipt.")

def show_ingredients():
    # Add this at the beginning of your show_ingredients function or at the top of the file
    if 'add_clicked' not in st.session_state:
        st.session_state.add_clicked = False

    # Fetch ingredients from Supabase
    ingredients = get_ingredients_from_supabase()

    # Check if we're in a sub-page
    if st.session_state.sub_page == "add_ingredient":
        show_add_ingredient()
        if st.button("Back to Ingredients"):
            st.session_state.sub_page = None
            st.rerun()
        return  # Exit the function here if we're showing the add ingredient form

    st.title("Pantry")

    # Create a container for buttons with custom styling
    st.markdown("""
        <style>
        .stButton > button {
            min-width: 120px !important;
            white-space: nowrap !important;
            padding: 0.25rem 0.5rem !important;
            text-align: center !important;
        }
        </style>
    """, unsafe_allow_html=True)

    # Create horizontal layout for buttons
    col1, col2, col3 = st.columns([0.76, 0.12, 0.12])  # Adjusted ratio for two buttons
    with col1:
        st.subheader("Ingredients List")
    with col2:
        if st.button("Add", key="add_ingredient", help="Add items", use_container_width=False):
            st.session_state.add_clicked = not st.session_state.add_clicked
    with col3:
        if st.button("Edit", key="edit_ingredient", help="Edit items", use_container_width=False):
            st.info("Edit functionality coming soon!")

    # Add clicked section remains the same
    if st.session_state.add_clicked:
        option_col1, option_col2 = st.columns(2)
        
        with option_col1:
            if st.button("Add Items Manually", use_container_width=True, key="manual_add"):
                st.session_state.manual_add_clicked = True
                st.session_state.upload_window_open = False
                
        with option_col2:
            if st.button("Upload Image", use_container_width=True, key="image_upload"):
                st.session_state.upload_window_open = True
                st.session_state.manual_add_clicked = False
        
        # Show scanner if upload window is open
        if st.session_state.upload_window_open:
            food_items = show_scanner_container()
            if st.button("Close Upload Window", key="close_upload"):
                st.session_state.upload_window_open = False
                st.rerun()
                
    # Show the form when manual add is clicked
    if st.session_state.add_clicked and st.session_state.manual_add_clicked:
        st.markdown("---")
        show_add_ingredient()
        
        # Add a back button to reset the state
        if st.button("Back to Ingredients"):
            st.session_state.add_clicked = False
            st.session_state.manual_add_clicked = False
            st.rerun()

    # If data is available, display it
    if ingredients:
        # Handle search functionality
        ingredient_search = st.text_input("Search for any item here... 🔍", "")
        
        # Convert the fetched data to a pandas DataFrame
        df = pd.DataFrame(ingredients)
        
        # Ensure all data columns are present
        df = df[['item_name', 'quantity', 'unit', 'days_in_pantry']]
        
        # Rename columns to match the desired table format
        df.columns = ["Ingredient", "Quantity", "Unit", "Days in Pantry"]
        
        if ingredient_search:
            df = df[df['Ingredient'].str.contains(ingredient_search, case=False)]
        
        # Show the table
        st.table(df)
    else:
        st.write("No ingredients found.")


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

