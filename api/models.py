from django.db import models
from django.conf import settings


class Signature(models.Model):
    document_id = models.UUIDField(unique=True, editable=False) 
    signature_id = models.UUIDField(unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default="pending")
    complete = models.BooleanField(default=False)
    polling = models.BooleanField(default=False)

    def __str__(self):
        return f"Signature {self.signature_id} for Document {self.document_id}"


class Signer(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="signatures")
    signature = models.ForeignKey(Signature, on_delete=models.CASCADE, related_name="signers")
    signer_url = models.URLField(max_length=200)
    status = models.CharField(max_length=50, default="pending")

    def __str__(self):
        return f"{self.user.username} - {self.status} ({self.signature.signature_id})"
