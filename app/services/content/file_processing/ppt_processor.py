# Requires a library to handle PPT files (e.g., python-pptx)
# pip install python-pptx
async def extract_text_from_ppt(content):
    # Example using python-pptx (replace with actual logic)
    # from pptx import Presentation
    # prs = Presentation(content.original_upload.file_path)
    # text = ""
    # for slide in prs.slides:
    #     for shape in slide.shapes:
    #         if hasattr(shape, "text"):
    #             text += shape.text
    # return [{"note_id": "1", "text": text, "topic_id": "default", "version": 1}]
    print(f"Simulating extracting text from PPT: {content.original_upload.file_name}")
    return [{"note_id": "1", "text": "This is the text extracted from the presentation.", "topic_id": "default", "version": 1}]