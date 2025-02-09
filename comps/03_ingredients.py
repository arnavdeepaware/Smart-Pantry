import streamlit as st
import pandas as pd


def show_ingredients():
    st.title("Ingredients")
    st.write("Welcome to the ingredients page!")
    
    st.subheader("My Ingredients")
    st.write("Here's a list of the ingredients currently in your pantry:")

    ingredient_search = st.text_input("Search for any item here... 🔍", "")
    if ingredient_search:
        df = df[df['Ingredient'].str.contains(ingredient_search, case=False)]
        st.table(df)

    #Popup

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
    
    if st.button("Add Item"):
        show_add_item_popup()


    
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


    st.table({
        "Ingredient": ["Milk", "Eggs", "Spinach", "Chicken Breast"],
        "Quantity": [1, 12, 3, 2],
        "Unit": ["kg", "mL", "L", "mL"],
        "Days in Pantry": ["6", "2", "9", "3"],
        
    })
    


  