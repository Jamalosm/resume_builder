import subprocess
import tempfile
from pathlib import Path

PDFLATEX_PATH = r"C:\Users\LENOVO\AppData\Local\Programs\MiKTeX\miktex\bin\x64\pdflatex.exe"

def generate_pdf(latex_code: str) -> bytes:
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        tex_file = tmp / "resume.tex"
        tex_file.write_text(latex_code, encoding="utf-8")

        subprocess.run(
            [PDFLATEX_PATH, "-interaction=nonstopmode", tex_file.name],
            cwd=tmp,
            check=True
        )

        return (tmp / "resume.pdf").read_bytes()
