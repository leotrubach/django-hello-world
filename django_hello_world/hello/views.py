import json

from annoying.decorators import render_to
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.template import RequestContext
from django.template.loader import render_to_string
from django.views.generic import UpdateView

from .models import Owner, Request
from .forms import OwnerForm


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

    def form_invalid(self, form):
        if not self.request.is_ajax():
            return super(EditOwner, self).form_invalid(form)
        return HttpResponse(
            json.dumps({
                'status': 'error',
                'form_html': render_to_string(
                    'hello/owner_form_inner.html',
                    {'form': form},
                    RequestContext(self.request, self.get_context_data())
                )}),
            content_type='application/javascript; charset=utf8'
        )

    def form_valid(self, form):
        if not self.request.is_ajax():
            return super(EditOwner, self).form_valid(form)
        self.object = form.save()
        return HttpResponse(
            json.dumps({'status': 'success'}),
            content_type='application/javascript; charset=utf8'
        )
