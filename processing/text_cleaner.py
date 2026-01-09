import re

def clean_text(text):
    """
    Cleans raw text without losing information
    """
    if not text:
        return ""

    
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    
    text = re.sub(r"[ \t]+", " ", text)

    
    text = re.sub(r"\n{2,}", "\n\n", text)

    
    text = re.sub(r"[^\x09\x0A\x0D\x20-\x7E]", "", text)

    return text.strip()
