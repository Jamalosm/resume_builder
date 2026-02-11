from django.shortcuts import render, redirect, get_object_or_404
from django.core.files.base import ContentFile
import json

from .models import Resume
from .services.resume_parser import parse_resume
from .services.latex_renderer import render_latex
from .services.pdf_generator import generate_pdf
from .services.llm.jd_alignment import align_resume_to_jd


def create_resume(request):
    context = {}

    if request.method == "POST":
        action = request.POST.get("action")

        # =========================
        # AUTO FILL
        # =========================
        if action == "autofill":
            if "uploaded_resume" in request.FILES:
                parsed = parse_resume(request.FILES["uploaded_resume"])
                context["data"] = parsed
                context["autofilled"] = True
            return render(request, "resumes/form.html", context)

        # =========================
        # GENERATE PDF
        # =========================
        if action == "generate":
            resume = Resume.objects.create(
                full_name=request.POST.get("full_name", ""),
                title=request.POST.get("title", ""),
                email=request.POST.get("email", ""),
                phone=request.POST.get("phone", ""),
                linkedin=request.POST.get("linkedin", ""),
                github=request.POST.get("github", ""),
                summary=request.POST.get("summary", ""),
                skills=request.POST.get("skills", ""),
                experience=request.POST.get("experience", ""),
                projects=request.POST.get("projects", ""),
                education=request.POST.get("education", ""),
                uploaded_resume=request.FILES.get("uploaded_resume"),
            )

            latex_code = render_latex(resume)
            pdf_bytes = generate_pdf(latex_code)

            resume.generated_pdf.save(
                f"{resume.full_name.replace(' ', '_')}.pdf",
                ContentFile(pdf_bytes),
                save=True
            )

            return redirect("preview", resume.id)

        # =========================
        # AI ANALYZE (FAST + OPTIMIZED)
        # =========================
        if action == "analyze":
            jd_text = request.POST.get("jd_text", "")

            resume_text = "\n".join([
                request.POST.get("summary", ""),
                request.POST.get("skills", ""),
                request.POST.get("experience", ""),
                request.POST.get("projects", ""),
                request.POST.get("education", "")
            ])

            # 🔥 SPEED OPTIMIZATION
            resume_text = resume_text[:600]
            jd_text = jd_text[:600]

            try:
                raw_response = align_resume_to_jd(
                    resume_text,
                    jd_text
                )

                # Try parsing JSON safely
                try:
                    result_json = align_resume_to_jd(resume_text, jd_text)
                except Exception as e:
                    result_json = {
                        "error": str(e)
                                    }


            except Exception as e:
                result_json = {
                    "error": str(e)
                }

            context["analysis"] = result_json
            context["jd_text"] = jd_text
            context["data"] = request.POST

            return render(request, "resumes/form.html", context)

    return render(request, "resumes/form.html", context)


def preview(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id)
    return render(request, "resumes/preview.html", {"resume": resume})
