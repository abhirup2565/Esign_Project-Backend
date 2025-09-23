from django.contrib.auth import get_user_model
from .models import Signature, Signer

User = get_user_model()

def save_signature_response(response_data):
    """
    Save signature + signers into DB from Setu API response.
    """
    # 1. Create Signature
    signature = Signature.objects.create(
        document_id=response_data["documentId"],
        signature_id=response_data["id"],  # use "id" from API response as signature_id
        status=response_data["status"],
    )

    # 2. Create Signers
    for signer_data in response_data["signers"]:
        try:
            user = User.objects.get(username=signer_data["displayName"])
            Signer.objects.create(
                user=user,
                signature=signature,
                status=signer_data["status"],
                signer_url=signer_data["url"]
            )
        except User.DoesNotExist:
            # Skip if user not found
            print(f"User {signer_data['displayName']} not found, skipping signer creation.")
        
