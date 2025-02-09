import streamlit as st

st.title("Add New Ingredient")

with st.form(key="add_ingredient_form"):
    item_name = st.text_input("Ingredient Name*", placeholder="Enter ingredient name")
    
    col1, col2 = st.columns(2)
    with col1:
        quantity = st.number_input("Quantity*", min_value=0.0, step=0.5)
    with col2:
        unit = st.selectbox(
            "Unit*",
            options=["grams", "kg", "ml", "liters", "pieces", "cups", "tbsp", "tsp"]
        )
    
    expiry_date = st.date_input("Expiry Date")
    notes = st.text_area("Notes", placeholder="Add any additional notes (optional)")
    
    submit_button = st.form_submit_button(label="Add Ingredient")
    
    if submit_button:
        if item_name and quantity > 0:
            st.success(f"Added {quantity} {unit} of {item_name} to your pantry!")
            demo_data = {
                "item_name": item_name,
                "quantity": quantity,
                "unit": unit,
                "expiry_date": expiry_date,
                "notes": notes
            }
            st.json(demo_data)
        else:
            st.error("Please fill in all required fields marked with *")