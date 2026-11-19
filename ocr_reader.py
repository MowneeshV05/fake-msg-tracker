# ocr_reader.py - Optical Character Recognition (OCR) engine for screenshot messages

from PIL import Image

def extract_text_from_image(image_file):
    # Step 1: Open the uploaded file using Pillow
    try:
        pil_image = Image.open(image_file)
        
        # Convert image to RGB format in case it is RGBA or grayscale
        if pil_image.mode != "RGB":
            pil_image = pil_image.convert("RGB")
            
    except Exception as error:
        return f"Error reading image: {str(error)}"
        
    # Step 2: Run Windows Native OCR using winocr
    try:
        import winocr
        
        # Recognize text synchronously from the Pillow image
        ocr_result = winocr.recognize_pil_sync(pil_image)
        
        # Extract the concatenated text
        extracted_text = ocr_result.get("text", "").strip()
        
        if len(extracted_text) == 0:
            return "No text could be detected in this image. Please ensure the screenshot is clear."
            
        return extracted_text
        
    except Exception as error:
        return f"OCR processing failed: {str(error)}"
