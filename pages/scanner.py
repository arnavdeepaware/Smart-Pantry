import streamlit as st
import numpy as np
from PIL import Image
import backend.recognize

st.title("Receipt Scanner")

uploaded_file = st.file_uploader("Upload a receipt image", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    img_array = np.array(image)

    st.image(image, caption="Uploaded Receipt", use_column_width=True)

    text = backend.recognize.extract_text(img_array)

    st.subheader("Extracted Text")
    st.text(text)
