import re
import fitz  # PyMuPDF

EMAIL_REGEX = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"
PHONE_REGEX = r"(\+91[\s-]?)?[6-9]\d{9}"

def parse_resume(pdf_file):
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    text = ""

    for page in doc:
        text += page.get_text()

    lines = [l.strip() for l in text.split("\n") if l.strip()]

    email = re.search(EMAIL_REGEX, text)
    phone = re.search(PHONE_REGEX, text)

    return {
        "full_name": lines[0] if lines else "",
        "email": email.group() if email else "",
        "phone": phone.group() if phone else "",
        "summary": " ".join(lines[1:5]) if len(lines) > 5 else "",
    }
