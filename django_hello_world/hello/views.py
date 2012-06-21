from annoying.decorators import render_to
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.views.generic import UpdateView

from .models import Owner, Request
from .forms import OwnerForm, RequestForm


@render_to('hello/home.html')
def home(request):
    try:
        owner = Owner.objects.get(active=True)
    except Owner.DoesNotExist:
        owner = None
    except Owner.MultipleObjectsReturned:
        owner = None
    return {'owner': owner}


@render_to('hello/last_requests.html')
def last_ten_requests(request):
    last_requests = Request.objects.order_by('-logged_date')[:10]
    return {'last_requests': last_requests}


class EditOwner(UpdateView):
    model = Owner
    form_class = OwnerForm
    success_url = '/'

class UpdateRequest(UpdateView):
    model = Request
    form_class = RequestForm
    success_url = '/'