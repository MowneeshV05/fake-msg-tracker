# ocr_reader.py - Optical Character Recognition (OCR) engine for screenshot messages
# Works on both Linux (Streamlit Cloud) using Tesseract and Windows using winocr.

from PIL import Image

NO_TEXT_MESSAGE = "No text could be detected in this image. Please ensure the screenshot is clear."


def _ocr_with_tesseract(pil_image):
    """Cross-platform OCR using Tesseract (needs 'tesseract-ocr' in packages.txt on the cloud)."""
    import pytesseract
    return pytesseract.image_to_string(pil_image).strip()


def _ocr_with_winocr(pil_image):
    """Windows-only OCR using the built-in Windows engine (used as a fallback on your PC)."""
    import winocr
    ocr_result = winocr.recognize_pil_sync(pil_image)
    return ocr_result.get("text", "").strip()


def extract_text_from_image(image_file):
    # Step 1: Open the uploaded file using Pillow
    try:
        pil_image = Image.open(image_file)

        # Convert image to RGB format in case it is RGBA or grayscale
        if pil_image.mode != "RGB":
            pil_image = pil_image.convert("RGB")

    except Exception as error:
        return f"Error reading image: {str(error)}"

    # Step 2: Try Tesseract first (works on the cloud), then Windows OCR (works on your PC)
    extracted_text = None
    errors = []

    for engine in (_ocr_with_tesseract, _ocr_with_winocr):
        try:
            extracted_text = engine(pil_image)
            break
        except Exception as error:
            errors.append(f"{engine.__name__}: {error}")

    if extracted_text is None:
        return "OCR processing failed: " + " | ".join(errors)

    if len(extracted_text) == 0:
        return NO_TEXT_MESSAGE

    return extracted_text
