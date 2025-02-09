import streamlit as st
import numpy as np
from PIL import Image
import backend.recognize as recognize

st.title("Receipt Scanner")

uploaded_file = st.file_uploader("Upload a receipt image", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    img_array = np.array(image)
    
    st.image(image, caption="Uploaded Receipt", use_container_width=True)
    
    extracted_text = recognize.extract_text(img_array)
    st.subheader("Extracted Text")
    st.text(extracted_text)
    
    food_items = recognize.extract_food_items_with_gemini(extracted_text)

    
    st.subheader("Extracted Food Items")
    if isinstance(food_items, list) and food_items:
        st.text("\n".join(food_items))
    else:
        st.text(food_items)
