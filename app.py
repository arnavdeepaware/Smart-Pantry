import streamlit as st
import pandas as pd
from datetime import datetime


if 'page' not in st.session_state:
    st.session_state.page = "Dashboard"

