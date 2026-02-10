import re
import fitz  # PyMuPDF

EMAIL_REGEX = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"

# FIX: allow spaces inside phone number
PHONE_REGEX = r"(\+91[\s-]?)?([6-9]\d{4}[\s-]?\d{5})"

SECTION_HEADERS = {
    "summary": ["professional summary", "summary"],
    "skills": ["technical skills", "skills"],
    "experience": ["professional experience", "experience"],
    "projects": ["key projects", "projects"],
    "education": ["education"],
}

def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip().lower()

def parse_resume(pdf_file):
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")

    raw_text = ""
    for page in doc:
        raw_text += page.get_text()

    lines = [l.strip() for l in raw_text.split("\n") if l.strip()]

    email = re.search(EMAIL_REGEX, raw_text)
    phone = re.search(PHONE_REGEX, raw_text)

    data = {
        "full_name": "",
        "title": "",
        "email": email.group() if email else "",
        "phone": phone.group().replace(" ", "") if phone else "",
        "summary": "",
        "skills": "",
        "experience": "",
        "projects": "",
        "education": "",
    }

    if not lines:
        return data

    # -------------------------
    # NAME & TITLE (TOP BLOCK)
    # -------------------------
    data["full_name"] = lines[0]

    if len(lines) > 1 and "@" not in lines[1]:
        data["title"] = lines[1]

    # -------------------------
    # SECTION PARSING
    # -------------------------
    current_section = None
    section_buffer = {k: [] for k in SECTION_HEADERS}

    for line in lines:
        lower = normalize(line)

        # Detect section header
        header_matched = False
        for section, keywords in SECTION_HEADERS.items():
            if any(lower == k for k in keywords):
                current_section = section
                header_matched = True
                break

        # Skip header line itself
        if header_matched:
            continue

        # Append content
        if current_section:
            section_buffer[current_section].append(line)

    # -------------------------
    # FINAL CLEAN JOIN
    # -------------------------
    for section, content in section_buffer.items():
        if section == "summary":
            # Summary = paragraph, not bullets
            data[section] = " ".join(content)
        else:
            data[section] = "\n".join(content)

    return data
