from django.urls import path
from .views import (Create_Document,
                    Get_Document,
                    Create_Signature,
                    Signature_Status,
                    StatusView,
                    DashboardView)

urlpatterns = [
    path("documents/", Create_Document.as_view(), name="create_document"),
    path("signature/", Create_Signature.as_view(), name="create-signature"),
    path("signature/<str:signature_id>/", Signature_Status.as_view(), name="signature-status"),
    path("download/<str:signature_id>/", Get_Document.as_view(), name="download_document"),
    path("status/", StatusView.as_view(), name="Status_View"),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    
]