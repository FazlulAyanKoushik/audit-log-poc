from auditlog.registry import auditlog
from django.contrib.auth.models import User
from django.db import models


class Document(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="documents")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class DocumentAccess(models.Model):
    """
    Defines which user has access to which document.
    Access type can be VIEW, EDIT, or DELETE.
    """
    VIEW = "view"
    EDIT = "edit"
    DELETE = "delete"

    ACCESS_CHOICES = [
        (VIEW, "View"),
        (EDIT, "Edit"),
        (DELETE, "Delete"),
    ]

    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name="accesses")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="doc_accesses")
    access_type = models.CharField(max_length=10, choices=ACCESS_CHOICES, default=VIEW)

    class Meta:
        unique_together = ("document", "user")

    def __str__(self):
        return f"{self.user.username} -> {self.document.title} ({self.access_type})"



# Register models with auditlog
auditlog.register(Document)
auditlog.register(DocumentAccess)
