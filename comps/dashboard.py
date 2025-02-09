import streamlit as st
import pandas as pd  # Add this with your other imports  


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
    st.markdown(f"<div style='text-align: left;'>Welcome, {user.name}!</div>", unsafe_allow_html=True)


    st.markdown("""
    <style>
        .metrics-container {
            border: 2px solid #e6e6e6;  # Changed from #white to #e6e6e6
            border-radius: 10px;
            padding: 20px;
            margin: 10px 0;
            opacity: 0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        /* Remove default container spacing */
        .element-container {
            margin-bottom: 0 !important;
            padding-bottom: 0 !important;
        }
        
        /* Adjust stContainer spacing */
        .stContainer {
            padding-top: 0 !important;
            padding-bottom: 0 !important;
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
        
        /* Style for expanders */
        .streamlit-expanderHeader {
            font-size: 1em;
            color: #333333;
            background-color: #f8f9fa;
            border-radius: 5px;
        }
        
        .streamlit-expanderContent {
            background-color: #ffffff;
            padding: 10px;
            border-radius: 0 0 5px 5px;
            text-align: left;  /* Add this line */
        }

        /* Add these new styles */
        .streamlit-expanderContent p {
            text-align: left !important;
            margin-left: 0 !important;
            padding-left: 0 !important;
        }
        
        /* Ensure bullet points align properly */
        .streamlit-expanderContent ul {
            text-align: left !important;
            padding-left: 20px !important;
        }
        
        /* Custom button width styles */
        .edit-btn {
            width: 80px !important;
        }
        .add-btn {
            width: 70px !important;
        }
        .view-all-btn {
            width: 100px !important;
        }
        .more-btn {
            width: 80px !important;
        }
        
        /* Ensure buttons stay right-aligned */
        div.row-widget.stButton {
            width: auto !important;
            min-width: auto !important;
        }

        /* Updated button width styles */
        .stButton > button {
            min-width: 120px !important;  /* Increased from 110px to 120px */
            white-space: nowrap !important;
            padding: 0.25rem 0.5rem !important;  /* Reduce padding to save space */
            text-align: center !important;
        }
        
        /* Remove the custom button width classes since we're using a consistent width */
        .edit-btn, .add-btn, .view-all-btn, .more-btn {
            display: none;
        }
    </style>
    """, unsafe_allow_html=True)



    # Metrics Widget
    with st.container():
        st.markdown('<div class="metrics-container">', unsafe_allow_html=True)
        col1, col2 = st.columns([0.88, 0.12])  # More space for "Edit" button
        with col1:
            st.subheader("Your Health Goals")
        with col2:
            if st.button("Edit", key="edit_metrics", help="Edit goals", use_container_width=False):
                st.switch_page("page", "Profile")
        
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
        col1, col2, col3 = st.columns([0.76, 0.12, 0.12])  # Equal space for "Add" and "View All"
        with col1:
            st.subheader("Pantry Overview")
        with col2:
            st.button("Add", key="add_pantry", help="Add items", use_container_width=False)
        with col3:
            st.button("View All", key="view_pantry", help="View all items", use_container_width=False)
            
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

    # Recipes Display
    with st.container():
        st.markdown('<div class="metrics-container">', unsafe_allow_html=True)
        col1, col2 = st.columns([0.88, 0.12])  # More space for "More" button
        with col1:
            st.subheader("My Recipes")
        with col2:
            st.button("More", key="view_recipes", help="View more recipes", use_container_width=False)
        
        # Sample recipes data - Remove dates from display
        recipes = [
            {
                "name": "Chicken Stir Fry",
                "calories": 450,
                "instructions": "1. Cut chicken\n2. Heat oil\n3. Stir fry vegetables\n4. Add sauce",
                "ingredients": ["Chicken", "Vegetables", "Soy Sauce"]
            },
            {
                "name": "Quinoa Bowl",
                "calories": 380,
                "instructions": "1. Cook quinoa\n2. Prepare vegetables\n3. Mix together",
                "ingredients": ["Quinoa", "Vegetables", "Olive Oil"]
            },
            {
                "name": "Greek Salad",
                "calories": 320,
                "instructions": "1. Chop vegetables\n2. Add feta\n3. Dress with olive oil",
                "ingredients": ["Cucumber", "Tomatoes", "Feta"]
            }
        ]
        
        for i, recipe in enumerate(recipes):
            with st.expander(f"🍽️ {recipe['name']} • {recipe['calories']} kcal"):
                st.markdown("""
                    <div style="text-align: left;">
                    <strong>Ingredients:</strong>
                    </div>
                """, unsafe_allow_html=True)
                for ingredient in recipe['ingredients']:
                    st.markdown(f"<div style='text-align: left; margin-left: 20px;'>• {ingredient}</div>", unsafe_allow_html=True)
                st.markdown("""
                    <div style="text-align: left;">
                    <strong>Instructions:</strong>
                    </div>
                """, unsafe_allow_html=True)
                instructions = recipe['instructions'].split('\n')
                for instruction in instructions:
                    st.markdown(f"<div style='text-align: left; margin-left: 20px;'>{instruction}</div>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)