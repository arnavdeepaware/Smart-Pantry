import streamlit as st
import pandas as pd
from backend.views import get_ingredients_from_supabase
from comps.add_ingredient import show_add_ingredient
import numpy as np
from PIL import Image
import backend.recognize as recognize  # Add this import

if 'sub_page' not in st.session_state:
    st.session_state.sub_page = None

# Add these session state initializations at the top after imports
if 'add_clicked' not in st.session_state:
    st.session_state.add_clicked = False
if 'manual_add_clicked' not in st.session_state:
    st.session_state.manual_add_clicked = False

def show_scanner_container():
    with st.container():
        st.subheader("Receipt Scanner Test")
        
        uploaded_file = st.file_uploader("Upload a receipt image", type=["png", "jpg", "jpeg"])

        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            img_array = np.array(image)
            
            st.image(image, caption="Uploaded Receipt", use_container_width=True)
            
            extracted_text = recognize.extract_text(img_array)
            st.subheader("Extracted Text")
            st.text(extracted_text)
            
            food_items = recognize.extract_food_items_with_gemini(extracted_text)
            
            st.subheader("Extracted Food Items")
            if isinstance(food_items, list) and food_items:
                st.text("\n".join(food_items))
            else:
                st.text(food_items)

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
    col1, col2, col3, col4 = st.columns([0.64, 0.12, 0.12, 0.12])  # Adjusted ratio to accommodate new button
    with col1:
        st.subheader("Ingredients List")
    with col2:
        if st.button("Add", key="add_ingredient", help="Add items", use_container_width=False):
            st.session_state.add_clicked = not st.session_state.add_clicked
            st.session_state.manual_add_clicked = False  # Reset nested button state
    with col3:
        if st.button("Edit", key="edit_ingredient", help="Edit items", use_container_width=False):
            st.info("Edit functionality coming soon!")
    test_clicked = False
    with col4:
        test_clicked = st.button("Test", key="test_ingredient", help="Test items", use_container_width=False)

    # Replace the add_clicked section with this:
    if st.session_state.add_clicked:
        option_col1, option_col2 = st.columns(2)
        
        with option_col1:
            if st.button("Add Items Manually", use_container_width=True, key="manual_add"):
                st.session_state.manual_add_clicked = not st.session_state.manual_add_clicked
                
        with option_col2:
            if st.button("Upload Image", use_container_width=True, key="image_upload"):
                show_scanner_container()
                
    # Show the form when manual add is clicked
    if st.session_state.add_clicked and st.session_state.manual_add_clicked:
        st.markdown("---")
        show_add_ingredient()
        
        # Add a back button to reset the state
        if st.button("Back to Ingredients"):
            st.session_state.add_clicked = False
            st.session_state.manual_add_clicked = False
            st.rerun()

    # Show scanner if Test is clicked
    if test_clicked:
        show_scanner_container()

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

