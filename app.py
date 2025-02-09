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

if 'page' not in st.session_state:
    st.session_state.page = "Dashboard"

