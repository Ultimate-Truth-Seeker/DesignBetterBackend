# python manage.py shell
import os
from django.conf import settings
from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp
try:
    from dotenv import load_dotenv; load_dotenv()
except Exception:
    pass

CID = os.getenv("GOOGLE_CLIENT_ID")
SEC = os.getenv("GOOGLE_CLIENT_SECRET")
if not CID or not SEC:
    raise RuntimeError("Define GOOGLE_CLIENT_ID y GOOGLE_CLIENT_SECRET en .env")

site = Site.objects.get(id=getattr(settings, "SITE_ID"))
app, _ = SocialApp.objects.get_or_create(provider="google", defaults={"name": "Google", "client_id": CID, "secret": SEC})
app.name = "Google"
app.client_id = CID
app.secret = SEC
app.save()
if site not in app.sites.all():
    app.sites.add(site)
print("Listo:", app.id, app.client_id[:8], "site", site.id)