import streamlit as st
import pandas as pd  # Add this with your other imports

st.markdown("""
<style>
    .metrics-container {
        border: 2px solid #e6e6e6;  # Changed from #white to #e6e6e6
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
        background-color: #ffffff;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    /* Add spacing between containers */
    .metrics-container + .metrics-container {
        margin-top: 20px;
    }
    
    /* Style for dataframe */
    .stDataFrame {
        border: 1px solid #f0f0f0;
        border-radius: 5px;
    }
    
    /* Style for recipe items */
    .recipe-item {
        padding: 10px 0;
        border-bottom: 1px solid #f0f0f0;
    }
    .recipe-item:last-child {
        border-bottom: none;
    }
</style>
""", unsafe_allow_html=True)

#Sample Data
class User:
    def __init__(self, name):
        self.name = name
        # Adding sample metrics data
        self.current_weight = 75.0  # in kg
        self.target_weight = 70.0   # in kg
        self.target_time = "2025-06-01"  # YYYY-MM-DD
        self.daily_calorie_target = 2000  # in calories

def show_dashboard():
    user = User("John Doe")
    st.title("Dashboard")
    st.write(f"Welcome, {user.name}!")
    
    # Metrics Widget
    with st.container():
        st.markdown('<div class="metrics-container">', unsafe_allow_html=True)
        
        # Create columns for header and button
        header_col, button_col = st.columns([0.85, 0.15])
        with header_col:
            st.subheader("Your Health Goals")
        with button_col:
            st.button("Edit", key="edit_metrics")
            
        # Existing metrics columns
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric(
                label="Current Weight",
                value=f"{user.current_weight} kg",
                delta=f"{user.target_weight - user.current_weight} kg to goal"
            )
            st.metric(
                label="Target Time",
                value=user.target_time
            )
        
        with col2:
            st.metric(
                label="Target Weight",
                value=f"{user.target_weight} kg"
            )
            st.metric(
                label="Daily Calorie Target",
                value=f"{user.daily_calorie_target} kcal"
            )
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Pantry Quick View
    with st.container():
        st.markdown('<div class="metrics-container">', unsafe_allow_html=True)
        col1, col2 = st.columns([0.85, 0.15])
        with col1:
            st.subheader("Pantry Overview")
        with col2:
            st.button("View All", key="view_pantry")
            
        # Sample pantry data - Replace with actual data from your database
        pantry_df = pd.DataFrame({
            'Item': ['Eggs', 'Milk', 'Bread', 'Rice'],
            'Quantity': [12, 1, 2, 1.5],
            'Unit': ['pcs', 'L', 'loaf', 'kg'],
            'Expiry': ['2025-02-15', '2025-02-12', '2025-02-10', '2025-05-01']
        })
        st.dataframe(
            pantry_df,
            hide_index=True,
            height=150,
            use_container_width=True
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Recent Recipes
    with st.container():
        st.markdown('<div class="metrics-container">', unsafe_allow_html=True)
        st.subheader("Recent Recipes")
        
        # Sample recipes data - Replace with actual data
        recipes = [
            {"name": "Chicken Stir Fry", "calories": 450, "date": "2025-02-07"},
            {"name": "Quinoa Bowl", "calories": 380, "date": "2025-02-06"},
            {"name": "Greek Salad", "calories": 320, "date": "2025-02-05"}
        ]
        
        for recipe in recipes:
            col1, col2, col3 = st.columns([0.5, 0.25, 0.25])
            with col1:
                st.write(recipe["name"])
            with col2:
                st.write(f"{recipe['calories']} kcal")
            with col3:
                st.write(recipe["date"])
        st.markdown('</div>', unsafe_allow_html=True)

