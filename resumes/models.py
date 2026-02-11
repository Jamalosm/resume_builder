from django.db import models

class Resume(models.Model):
    full_name = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    linkedin = models.URLField(blank=True)
    github = models.URLField(blank=True)

    summary = models.TextField()

    skills = models.TextField(help_text="Comma separated")

    experience = models.TextField()
    projects = models.TextField()
    education = models.TextField()

    uploaded_resume = models.FileField(upload_to="resumes/", blank=True, null=True)
    generated_pdf = models.FileField(upload_to="generated/", blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name

class ResumeAnalysis(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    jd_text = models.TextField()
    result_json = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
