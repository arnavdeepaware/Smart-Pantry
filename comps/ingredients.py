import streamlit as st
import pandas as pd
from backend.views import get_ingredients_from_supabase

def manual_entry_form():
    form_col, image_col = st.columns(2)
    
    with form_col:
        st.write("Add items manually")
        item_name = st.text_input("Item Name")
        item_quantity = st.number_input("Quantity", min_value=1)
        item_unit = st.text_input("Unit")
        
        if st.button("Submit", key="submit_manual_item"):
            if item_name and item_unit:
                # TODO: Add Supabase integration here
                st.success("Item Added!")
                st.session_state.pantry_form_mode = None
                st.rerun()
    
    with image_col:
        st.markdown('<div style="padding: 20% 0;">', unsafe_allow_html=True)
        uploaded_file = st.file_uploader(
            "Upload an image of your item", 
            type=['png', 'jpg', 'jpeg'],
            help="Optional: Add an image of your ingredient"
        )
        st.markdown('</div>', unsafe_allow_html=True)

def bill_upload_form():
    upload_col1, upload_col2 = st.columns(2)
    
    with upload_col1:
        st.write("Upload your grocery bills")
        uploaded_file = st.file_uploader(
            "Upload your grocery bill", 
            type=['png', 'jpg', 'jpeg', 'pdf'],
            help="Upload your grocery bill to automatically extract items"
        )
        if uploaded_file:
            st.info("Bill processing functionality coming soon!")
            st.image(uploaded_file, caption="Uploaded Bill", use_column_width=True)
    
    with upload_col2:
        st.markdown('<div style="padding: 20% 0;">', unsafe_allow_html=True)
        if st.button("Upload from Phone", use_container_width=True):
            st.info("Phone upload functionality coming soon!")
        st.markdown('</div>', unsafe_allow_html=True)

def show_add_item_form():
    option_col1, option_col2 = st.columns(2)
    
    with option_col1:
        if st.button("Add Items Manually", use_container_width=True, key="manual_add"):
            manual_entry_form()
            st.button("Back", key="back_manual")
            
    with option_col2:
        if st.button("Upload Grocery Bills", use_container_width=True, key="bill_upload"):
            bill_upload_form()
            st.button("Back", key="back_upload")

def show_ingredients():
    # Fetch ingredients from Supabase
    ingredients = get_ingredients_from_supabase()

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
    col1, col2, col3 = st.columns([0.76, 0.12, 0.12])  # Same ratio as dashboard.py
    with col1:
        st.subheader("Ingredients List")
    with col2:
        add_clicked = st.button("Add", key="add_ingredient", help="Add items", use_container_width=False)
    with col3:
        if st.button("Edit", key="edit_ingredient", help="Edit items", use_container_width=False):
            st.info("Edit functionality coming soon!")

    # Show add item form if 'Add' button is clicked
    if add_clicked:
        show_add_item_form()

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

