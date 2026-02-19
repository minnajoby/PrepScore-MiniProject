import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_file):
    """
    Extracts raw text string from an uploaded PDF file.
    
    Args:
        pdf_file: An opened file-like object (e.g., from request.FILES) or path.
        
    Returns:
        str: The extracted text content.
    """
    text = ""
    try:
        # Open the PDF from the file stream or path
        # If it's a file-like object from Django (InMemoryUploadedFile), we can read its content
        if hasattr(pdf_file, 'read'):
            # It's a file stream, read bytes
            pdf_bytes = pdf_file.read()
            doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        else:
            # It's a path
            doc = fitz.open(pdf_file)
            
        for page in doc:
            text += page.get_text()
            
        doc.close()
    except Exception as e:
        print(f"Error extracting PDF text: {e}")
        return ""
        
    return text
