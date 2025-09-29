import atexit
import requests
from apscheduler.schedulers.background import BackgroundScheduler
from django.contrib.auth import get_user_model
from django.conf import settings
from .models import Signature, Signer

scheduler = BackgroundScheduler()
User = get_user_model()
SETU_BASE_URL = settings.SETU_BASE_URL

headers = {
    'x-client-id': settings.X_CLIENT_ID,
    'x-client-secret': settings.X_CLIENT_SECRET,
    'x-product-instance-id': settings.X_PRODUCT_INSTANCE_ID
}

def poll_signature():
    signatures = Signature.objects.filter(complete=False)  # only check incomplete ones
    for signature in signatures:
        try:
            resp = requests.get(
                f"{SETU_BASE_URL}/signature/{signature.signature_id}/",
                headers={
                    'x-client-id': '6faa7c17-2977-437a-8c73-30bf40c2edff',
                    'x-client-secret': 'GqNvWr5md8LYTrIQTnAzygNQrtvIXpMR',
                    'x-product-instance-id': '07451d5a-6091-4e58-8f25-30771aaccb96'
                }
            )
            resp.raise_for_status()
            data = resp.json()
            # Updating value in Signature db
            signature.status = data["status"]
            signature.complete = (data["status"] == "sign_complete")
            signature.save()
            # Updating value in Signer db
            for signer_data in data["signers"]:
                try:
                    user = User.objects.get(username=signer_data["displayName"])
                except User.DoesNotExist:
                    print("Error: User not found while updating Signer db")
                    continue
                Signer.objects.update_or_create(
                    signature=signature,
                    user=user,
                    defaults={
                        "signer_url": signer_data["url"],
                        "status": signer_data["status"],
                    }
                )
        except Exception as e:
            print(f"Error polling {signature.signature_id}: {e}")

def start_scheduler():
    """
    If you are running locally on SQLite, avoid using very short intervals (e.g., below 15 seconds). SQLite does not handle concurrent writes well, which can lead to database locking issues. For production, a more robust database like PostgreSQL is recommended.
    """
    # Schedule polling every 10 seconds
    scheduler.add_job(poll_signature, 'interval', seconds=10)
    scheduler.start()

    # Shut down gracefully on exit
    atexit.register(lambda: scheduler.shutdown())