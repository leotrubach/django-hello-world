import json

from annoying.decorators import render_to
from django.http import HttpResponse
from django.views.generic import UpdateView, ListView
from django.template import RequestContext
from django.template.loader import render_to_string

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
    template_name = 'hello/requests.html'
    context_object_name = 'requests'
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
                queryset = Request.objects.order_by(
                    '-priority', '-logged_date')
                self.order = 'desc'
            else:
                queryset = Request.objects.order_by(
                    'priority', '-logged_date')
                self.order = 'asc'
            return queryset


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


class UpdateRequest(UpdateView):
    model = Request
    form_class = RequestForm

    def form_valid(self, form):
        self.object = form.save()
        return HttpResponse('OK')
