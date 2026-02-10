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
# LATEX SANITIZER
# =========================
def tex_escape(text: str) -> str:
    if not text:
        return ""

    replacements = {
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }

    for k, v in replacements.items():
        text = text.replace(k, v)

    # Normalize unicode dashes
    text = text.replace("–", "--").replace("—", "--")

    return text


# =========================
# ITEMIZE
# =========================
def itemize(lines):
    items = "\n".join(f"\\item {tex_escape(l)}" for l in lines)
    return (
        "\\begin{itemize}\n"
        f"{items}\n"
        "\\end{itemize}"
    )


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
            out.append(
                f"\\textbf{{{tex_escape(h.strip())}:}} "
                f"{tex_escape(v.strip())} \\\\"
            )
        else:
            out.append(tex_escape(line) + " \\\\")

    return "\n".join(out)


# =========================
# EXPERIENCE / PROJECT FORMATTER
# =========================
def format_block(text: str) -> str:
    if not text:
        return ""

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
        # Date range
        m = DATE_RANGE_REGEX.search(line)
        if m:
            date_range = m.group(1)
            continue

        # Environment
        if line.startswith("(") and line.endswith(")"):
            environment = line.strip("()")
            continue

        # Role
        if not role and len(line.split()) <= 6 and not line.endswith("."):
            role = line
            continue

        # Company
        if "," in line and not line.endswith("."):
            company = line
            continue

        # Project title
        if line[0].isupper() and not line.endswith("."):
            flush_bullets()
            output.append(f"\\textbf{{{tex_escape(line)}}}")
            continue

        # Bullet
        clean = re.sub(r"^[•\-–]\s*", "", line)
        bullets.append(clean)

    flush_bullets()

    header_lines = []

    if role:
        if date_range:
            header_lines.append(
                f"\\textbf{{{tex_escape(role)}}} "
                f"\\hfill \\textbf{{{tex_escape(date_range)}}}"
            )
        else:
            header_lines.append(f"\\textbf{{{tex_escape(role)}}}")

    if company:
        header_lines.append(f"\\textbf{{{tex_escape(company)}}}")

    if environment:
        header_lines.append(f"\\textit{{{tex_escape(environment)}}}")

    header = " \\\\\n".join(header_lines)

    return "\n".join([header] + output)
