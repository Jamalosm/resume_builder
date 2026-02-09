from django.shortcuts import render, redirect, get_object_or_404
from django.core.files.base import ContentFile
from .models import Resume
from .services.resume_parser import parse_resume
from .services.latex_renderer import render_latex
from .services.pdf_generator import generate_pdf

def create_resume(request):
    context = {}

    if request.method == "POST":
        action = request.POST.get("action")

        # AUTO-FILL
        if action == "autofill" and "uploaded_resume" in request.FILES:
            parsed = parse_resume(request.FILES["uploaded_resume"])
            context["data"] = parsed
            context["autofilled"] = True
            return render(request, "resumes/form.html", context)

        # GENERATE
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

        pdf_bytes = generate_pdf(render_latex(resume))
        resume.generated_pdf.save(
            f"{resume.full_name.replace(' ', '_')}.pdf",
            ContentFile(pdf_bytes),
            save=True
        )
        return redirect("preview", resume.id)

    return render(request, "resumes/form.html", context)


def preview(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id)
    return render(request, "resumes/preview.html", {"resume": resume})
