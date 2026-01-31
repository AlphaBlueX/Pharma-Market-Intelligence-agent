import re

def clean_text(text: str) -> str:
    """
    Cleans the input text by removing extra whitespace, HTML tags, and non-ASCII characters.
    """
    if not text:
        return ""
    
    # Remove HTML tags
    text = re.sub(r'<.*?>', '', text)
    
    # Remove non-ASCII characters
    text = text.encode("ascii", "ignore").decode()
    
    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text
