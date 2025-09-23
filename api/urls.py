from django.urls import path
from .views import (Create_Document,
                    Get_Document,
                    Create_Signature,
                    Signature_Status,
                    ProtectedView,
                    StatusView)

urlpatterns = [
    path("documents/", Create_Document.as_view(), name="create_document"),
    path("signature/", Create_Signature.as_view(), name="create-signature"),
    path("signature/<str:signature_id>/", Signature_Status.as_view(), name="signature-status"),
    path("documents/<str:signature_id>/", Get_Document.as_view(), name="get_document"),
    path("protected/", ProtectedView.as_view(), name="protected_view"),
    path("status/", StatusView.as_view(), name="Status_View"),
    
]