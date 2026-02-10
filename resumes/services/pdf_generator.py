import subprocess
import tempfile
from pathlib import Path


PDFLATEX_PATH = r"C:\Users\LENOVO\AppData\Local\Programs\MiKTeX\miktex\bin\x64\pdflatex.exe"


def generate_pdf(latex_code: str) -> bytes:
    if not latex_code or not latex_code.strip():
        raise ValueError("LaTeX code is empty")

    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp = Path(tmp_dir)

        tex_file = tmp / "resume.tex"
        tex_file.write_text(latex_code, encoding="utf-8")

        # Run pdflatex safely
        result = subprocess.run(
            [
                PDFLATEX_PATH,
                "-interaction=nonstopmode",
                "-halt-on-error",
                tex_file.name,
            ],
            cwd=tmp,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        # If LaTeX failed → show REAL error
        if result.returncode != 0:
            log_file = tmp / "resume.log"
            log_content = log_file.read_text(errors="ignore") if log_file.exists() else ""

            raise RuntimeError(
                "LaTeX compilation failed.\n\n"
                "----- STDOUT -----\n"
                f"{result.stdout}\n\n"
                "----- STDERR -----\n"
                f"{result.stderr}\n\n"
                "----- LOG FILE -----\n"
                f"{log_content}"
            )

        pdf_file = tmp / "resume.pdf"
        if not pdf_file.exists():
            raise RuntimeError("pdflatex finished but PDF was not generated")

        return pdf_file.read_bytes()
