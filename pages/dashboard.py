import streamlit as st

def show_dashboard():
    st.title("Dashboard")
    st.write("Welcome to the dashboard!")
    
    # Add more dashboard components here
    st.subheader("Quick Statistics")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(label="Total Items", value="25")
    with col2:
        st.metric(label="Low Stock Items", value="3")
    with col3:
        st.metric(label="Expiring Soon", value="5")