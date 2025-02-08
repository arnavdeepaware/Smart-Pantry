import streamlit as st
import pandas as pd
from datetime import datetime

products_data = {
    "Product": ["Milk", "Eggs", "Spinach", "Chicken Breast"],
    "Purchase Date": ["2024-01-10", "2024-02-01", "2024-02-05", "2024-01-20"],
    "Quantity": [1, 12, 3, 2], 
    "Calories": [150, 72, 23, 165],  
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
}

df = pd.DataFrame(products_data)
df["Purchase Date"] = pd.to_datetime(df["Purchase Date"])

def calculate_days_ago(purchase_date):
    return (datetime.today() - purchase_date).days

df["Days Ago Purchased"] = df["Purchase Date"].apply(calculate_days_ago)
df = df.drop(columns=["Purchase Date"]) 

def pantry_dashboard():
    st.title("My Pantry Dashboard")
    st.write("Welcome to your pantry! Here's a list of the products currently in your fridge:")

    if "quantities" not in st.session_state:
        st.session_state.quantities = df["Quantity"].tolist()

    st.write("### Pantry Items")
    
    cols = st.columns([2, 2, 3, 2, 3, 3])  
    headers = ["Product", "Days Ago Purchased", "Quantity", "Calories", "Suggested Recipes", "Nearby Locations"]
    
    for col, header in zip(cols, headers):
        col.write(f"**{header}**") 

    for index, row in df.iterrows():
        cols = st.columns([2, 2, 3, 2, 3, 3])  
        
        cols[0].write(row["Product"])
        cols[1].write(row["Days Ago Purchased"])
        
        with cols[2]:  
            if st.button("➖", key=f"decrease_{index}"):
                if st.session_state.quantities[index] > 0:
                    st.session_state.quantities[index] -= 1
            
            st.write(st.session_state.quantities[index]) 
            
            if st.button("➕", key=f"increase_{index}"):
                st.session_state.quantities[index] += 1

        cols[3].write(f"{row['Calories']} kcal")
        cols[4].write(f"[Recipe]({row['Suggested Recipes']})")
        cols[5].write(f"[Store]({row['Nearby Locations']})")

def main():
    st.sidebar.title("Smart Pantry")
    options = ["My Pantry Dashboard"]
    choice = st.sidebar.radio("Select a Page", options)

    if choice == "My Pantry Dashboard":
        pantry_dashboard()

if __name__ == "__main__":
    main()
