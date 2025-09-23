from django.contrib import admin
from .models import ( Signature,
                     Signer)
# Register your models here.
admin.site.register(Signature)
admin.site.register(Signer)