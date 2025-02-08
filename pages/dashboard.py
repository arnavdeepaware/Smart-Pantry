import streamlit as st

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
        st.subheader("Your Health Goals")
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

