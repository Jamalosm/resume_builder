import re

# =========================
# DATE RANGE REGEX
# =========================
DATE_RANGE_REGEX = re.compile(
    r"""
    (
        (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec|
         January|February|March|April|June|July|August|
         September|October|November|December)?
        \s*\d{4}
        \s*(–|-|--|to)\s*
        (Present|\d{4})
    )
    """,
    re.IGNORECASE | re.VERBOSE,
)

# =========================
# ITEMIZE
# =========================
def itemize(lines):
    items = "\n".join(f"\\item {l}" for l in lines)
    return f"""
\\begin{{itemize}}
{items}
\\end{{itemize}}
"""

# =========================
# SKILLS FORMATTER
# =========================
def format_skills(text: str) -> str:
    if not text:
        return ""

    out = []
    for line in text.split("\n"):
        line = line.strip()
        if not line:
            continue

        if ":" in line:
            h, v = line.split(":", 1)
            out.append(f"\\textbf{{{h.strip()}:}} {v.strip()} \\\\")
        else:
            out.append(line + " \\\\")

    return "\n".join(out)

# =========================
# EXPERIENCE / PROJECT FORMATTER
# =========================
def format_block(text: str) -> str:
    if not text:
        return ""

    # Normalize dash
    text = text.replace("–", "-").replace("—", "-")

    lines = [l.strip() for l in text.split("\n") if l.strip()]

    role = ""
    company = ""
    environment = ""
    date_range = ""
    bullets = []
    output = []

    def flush_bullets():
        nonlocal bullets
        if bullets:
            output.append(itemize(bullets))
            bullets = []

    for line in lines:

        # -------------------------
        # Date range detection
        # -------------------------
        m = DATE_RANGE_REGEX.search(line)
        if m:
            date_range = m.group(1)
            continue

        # -------------------------
        # Environment detection
        # -------------------------
        if line.startswith("(") and line.endswith(")"):
            environment = line.strip("()")
            continue

        # -------------------------
        # Role detection (only first line)
        # -------------------------
        if not role:
            role = line
            continue

        # -------------------------
        # Company detection
        # -------------------------
        if not company and "," in line:
            company = line
            continue

        # -------------------------
        # STRICT Project Name Detection
        # (only if explicitly separated by hyphen)
        # -------------------------
        if " - " in line and len(line.split()) <= 8:
            flush_bullets()
            output.append(f"\\textbf{{{line}}}")
            continue

        # -------------------------
        # Bullet lines
        # -------------------------
        clean = re.sub(r"^[•\\-–ˆ]\s*", "", line)
        bullets.append(clean)

    flush_bullets()

    # -------------------------
    # Header Section
    # -------------------------
    header = []

    if role:
        if date_range:
            header.append(
                f"\\textbf{{{role}}} \\hfill \\textbf{{{date_range}}}"
            )
        else:
            header.append(f"\\textbf{{{role}}}")

    if company:
        header.append(company)

    if environment:
        header.append(f"\\textit{{{environment}}}")

    return "\n\n".join(header + output)

