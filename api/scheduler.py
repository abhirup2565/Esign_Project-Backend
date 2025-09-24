import atexit
import requests
from apscheduler.schedulers.background import BackgroundScheduler
from django.contrib.auth import get_user_model
from .models import Signature, Signer

scheduler = BackgroundScheduler()
User = get_user_model()

def poll_signature():
    print("Polling signature")
    signatures = Signature.objects.filter(complete=False)  # only check incomplete ones
    for signature in signatures:
        try:
            resp = requests.get(
                f"https://dg-sandbox.setu.co/api/signature/{signature.signature_id}/",
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
    # Schedule polling every 5 minutes
    scheduler.add_job(poll_signature, 'interval', seconds=5)
    scheduler.start()
    # Shut down gracefully on exit
    atexit.register(lambda: scheduler.shutdown())