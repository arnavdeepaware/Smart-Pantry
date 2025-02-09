import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import numpy as np
from PIL import Image
from backend.recognize import extract_food_items_with_gemini, extract_text
import streamlit as st


def img_to_food_items(uploaded_file):

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        img_array = np.array(image)
        
        st.image(image, caption="Uploaded Receipt", use_container_width=True)
        
        extracted_text = extract_text(img_array)        
        food_items = extract_food_items_with_gemini(extracted_text)
        return food_items
