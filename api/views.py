import requests
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import status
from django.contrib.auth import get_user_model
from users.permissions import IsManager
from .serializers import SignatureSerializer
from .models import Signature

User = get_user_model()

SETU_BASE_URL = "https://dg-sandbox.setu.co/api"
SETU_API_KEY = "your_setu_api_key_here"

headers = {
    'x-client-id': '6faa7c17-2977-437a-8c73-30bf40c2edff',
    'x-client-secret': 'GqNvWr5md8LYTrIQTnAzygNQrtvIXpMR',
    'x-product-instance-id': '07451d5a-6091-4e58-8f25-30771aaccb96'
}

class ProtectedView(APIView):
    def get(self, request):
        return Response({"message": f"Hello {request.user.username}, you are authenticated!"})


class Create_Document(APIView):
    permission_classes = [IsManager]
    def post(self,request):
        """
        Uploads a document to Setu API
        """
        try:
            # Get fields
            name = request.data.get("name")
            file = request.FILES.get("document")
            if not file:
                return Response({"error": "No file provided"}, status=400)
            if not name:
                return Response({"error": "No Name provided"}, status=400)
            # Prepare multipart payload
            files = {
                "document": (file.name, file.read(), file.content_type)
            }
            data = {
                "name": name
            }
            # Forward request to Setu
            response = requests.post(
                f"{SETU_BASE_URL}/documents",
                data=data,
                files=files,
                headers=headers
            )
            return Response(response.json(), status=response.status_code)

        except Exception as e:
            print("SIGNATURE ERROR:", e)
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class Create_Signature(APIView):
    permission_classes = [IsManager]
    def post(self,request):
        """
        Creates a signature request for uploaded document
        """
        from .utils import save_signature_response
        try:
            payload = request.data  # should contain: documentId,signers[]
            response = requests.post(
                f"{SETU_BASE_URL}/signature",
                json=payload,
                headers={**headers, "Content-Type": "application/json"}
            )
            response_data = response.json()
            save_signature_response(response_data)
            return Response(response.json(), status=response.status_code)

        except Exception as e:
            print("SIGNATURE ERROR:", e)
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class Signature_Status(APIView):
    permission_classes = [AllowAny]
    def get(self,request, signature_id):
        """
        Fetches the status of a signature request
        """
        try:
            response = requests.get(
                f"{SETU_BASE_URL}/signature/{signature_id}",
                headers=headers
            )
            return Response(response.json(), status=response.status_code)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class Get_Document(APIView):
    permission_classes = [AllowAny]
    def get(self,request, signature_id):
        """
        Download link for signed document
        """
        try:
            response = requests.get(
                f"{SETU_BASE_URL}/signature/{signature_id}/download",
                headers=headers
            )
            return Response(response.json(), status=response.status_code)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class StatusView(generics.ListAPIView):
    queryset = Signature.objects.all()
    serializer_class = SignatureSerializer
    permission_classes = [IsManager]

class DashboardView(generics.ListAPIView):
    serializer_class = SignatureSerializer

    def get_queryset(self):
        user = self.request.user  # get the logged-in user
        return Signature.objects.filter(signers__user=user)