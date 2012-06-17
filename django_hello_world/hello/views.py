from annoying.decorators import render_to
from django.contrib.auth.models import User

from .models import Owner, Request


@render_to('hello/home.html')
def home(request):
    try:
        owner = Owner.objects.get(active=True)
    except Owner.DoesNotExist:
        owner = None
    except Owner.MultipleObjectsReturned:
        owner = None
    last_requests = Request.objects.order_by('-dt_request')[:10]
    return {'owner': owner, 'last_requests': last_requests}
