from annoying.decorators import render_to
from django.contrib.auth.models import User

from .models import Owner

@render_to('hello/home.html')
def home(request):
    owner = Owner.objects.get(active=True)
    return {'owner': owner}
