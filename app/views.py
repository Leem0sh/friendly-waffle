# Create your views here.
from datetime import datetime

from django.http import HttpResponse


def ping(request):
    return HttpResponse(f"✅ Pong {datetime.now().isoformat()}")


def index(request):
    return HttpResponse("<a href='/api/applift/docs'> How about trying the API docs?</a>"
                        "<br>"
                        "<a href='/ping'> Or wanna play ping pong?</a>")
