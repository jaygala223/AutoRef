import re
from pdfminer.high_level import extract_text

def extract_info_from_resume(pdf_path):
    # Extract text from PDF
    text = extract_text(pdf_path).lower()
    
    # Initialize variables
    name = None
    mobile = None
    email = None
    
    # Regular expressions for matching
    name_pattern = r'[a-z][a-z\-]+'
    mobile_patterns = [
    r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',  # (XXX) XXX-XXXX or XXX-XXX-XXXX
    r'\+\d{1,3}\s\d{3}[-.\s]?\d{4}[-.\s]?\d{2}',  # +XX XXX-XXXX-XX
    r'\+\d{2}[-\s]?\d{4}[-\s]?\d{3}[-\s]?\d{3}'  # +91-7827-328-869
    ]
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    
    # Split text into lines
    lines = text.split('\n')
    
    # Search for name (assume it's within the first 5 non-empty lines)
    for line in lines[:10]:
        line = line.strip()
        if line and not name and re.match(name_pattern, line):
            name = line
            break
    
    # Search for mobile and email
    for line in lines:
        line = line.strip()
        
        # Find mobile number
        if not mobile:
            for pattern in mobile_patterns:
                mobile_match = re.search(pattern, line)
                if mobile_match:
                    mobile = mobile_match.group()
                    break
        
        # Find email
        if not email:
            email_match = re.search(email_pattern, line)
            if email_match:
                email = email_match.group()
        
        # Break if both mobile and email are found
        if mobile and email:
            break
    
    return name,mobile,email

# Example usage
if __name__ == "__main__":
    pdf_path = './'
    result = extract_info_from_resume(pdf_path)
    print(result)