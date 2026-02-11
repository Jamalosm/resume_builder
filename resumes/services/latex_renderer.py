from .latex_utils import format_skills, format_block


# =========================
# SAFE LATEX ESCAPER
# =========================
def escape_latex(text: str) -> str:
    if not text:
        return ""

    # Normalize unicode dashes
    text = text.replace("–", "-")
    text = text.replace("—", "-")

    replacements = {
        "\\": r"\textbackslash{}",
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

    return text


# =========================
# LATEX TEMPLATE (SAFE)
# =========================
LATEX_TEMPLATE = r"""
\documentclass[10pt]{{article}}

\usepackage[utf8]{{inputenc}}
\usepackage[T1]{{fontenc}}
\usepackage[a4paper,margin=0.6in]{{geometry}}
\usepackage{{enumitem}}
\usepackage[hidelinks]{{hyperref}}
\usepackage{{titlesec}}

\pagenumbering{{gobble}}

\titleformat{{\section}}
{{\large\bfseries}}
{{}}
{{0em}}
{{}}
[\titlerule]

\titlespacing*{{\section}}{{0pt}}{{6pt}}{{6pt}}

\setlist[itemize]{{noitemsep, topsep=2pt, leftmargin=*}}

\begin{{document}}

\begin{{center}}
{{\LARGE \textbf{{{full_name}}}}} \\  
\textbf{{{title}}} \\
\vspace{{3pt}}
\href{{mailto:{email}}}{{{email}}} \;|\;
{phone} \;|\;
\href{{{linkedin}}}{{LinkedIn}} \;|\;
\href{{{github}}}{{GitHub}}
\end{{center}}

\section*{{Professional Summary}}
{summary}

\section*{{Technical Skills}}
{skills}

\section*{{Professional Experience}}
{experience}

\section*{{Key Projects}}
{projects}

\section*{{Education}}
{education}

\end{{document}}
"""


# =========================
# FINAL RENDER FUNCTION
# =========================
def render_latex(resume):
    return LATEX_TEMPLATE.format(
        full_name=escape_latex(resume.full_name),
        title=escape_latex(resume.title),
        email=escape_latex(resume.email),
        phone=escape_latex(resume.phone),
        linkedin=escape_latex(resume.linkedin),
        github=escape_latex(resume.github),

        summary=escape_latex(resume.summary),
        skills=format_skills(escape_latex(resume.skills)),

        experience=format_block(
            escape_latex(resume.experience)
        ),

        projects=format_block(
            escape_latex(resume.projects)
        ),

        education=format_block(
            escape_latex(resume.education)
        ),
    )
