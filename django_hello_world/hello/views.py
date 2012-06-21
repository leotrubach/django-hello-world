from annoying.decorators import render_to
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import UpdateView, ListView

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


class RequestList(ListView):
    model = Request
    template_name = 'hello/last_requests.html'
    context_object_name = 'last_requests'
    paginate_by = 20

    def __init__(self, **kwargs):
        super(ListView, self).__init__(**kwargs)
        self.order = 'desc'

    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        context['order'] = self.order
        return context

    def get_queryset(self):
        if self.request.method == 'GET':
            # default ordering is descending
            order = self.request.GET.get('order', 'desc')
            if order == 'desc':
                queryset = Request.objects.order_by('-priority', '-logged_date')
                self.order = 'desc'
            else:
                queryset = Request.objects.order_by('priority', '-logged_date')
                self.order = 'asc'
            return queryset


class EditOwner(UpdateView):
    model = Owner
    form_class = OwnerForm
    success_url = '/'


class UpdateRequest(UpdateView):
    model = Request
    form_class = RequestForm

    def form_valid(self, form):
        self.object = form.save()
        return HttpResponse('OK')
