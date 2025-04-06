# Requires OCR library (e.g., pytesseract)
#  Also might require Tesseract OCR engine installed separately
# pip install pytesseract
async def extract_text_from_image(content):
    #  Example using pytesseract (replace with actual logic)
    # text = pytesseract.image_to_string(content.original_upload.file_path)
    # return [{"note_id": "1", "text": text, "topic_id": "default", "version": 1}]
    print(f"Simulating extracting text from image: {content.original_upload.file_name}")
    return [{"note_id": "1", "text": "This is the text extracted from the image.", "topic_id": "default", "version": 1}]