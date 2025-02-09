import easyocr

reader = easyocr.Reader(['en'])

def extract_text(image):
    result = reader.readtext(image, detail=0)  # Extract text (no bounding box details)
    return "\n".join(result) if result else "No text detected."
