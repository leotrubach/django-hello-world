from annoying.decorators import render_to
from django.contrib.auth.models import User
from django.views.generic import UpdateView, ListView

from .models import Owner, Request
from .forms import OwnerForm, PriorityForm


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


class RequestList(ListView):
    model = Request
    template_name = 'hello/last_requests.html'
    context_object_name = 'last_requests'
    paginate_by = 20

    def __init__(self, *args, **kwargs):
        super(ListView, self).__init__(*args, **kwargs)
        self.priority = 1

    def get_context_data(self, **kwargs):
        context = super(RequestList, self).get_context_data(**kwargs)
        context['form'] = PriorityForm(initial={'priority': self.priority})
        context['priority'] = self.priority
        return context

    def get_queryset(self):
        if self.request.method == 'GET':
            # default priority is 1 = descending
            f = PriorityForm(self.request.GET)
            if f.is_valid():
                self.priority = f.cleaned_data.get('priority', 1)
            else:
                self.priority = 1
            if self.priority == 1:
                queryset = Request.objects.order_by('-logged_date')
            else:
                queryset = Request.objects.order_by('logged_date')
            return queryset


class EditOwner(UpdateView):
    model = Owner
    form_class = OwnerForm
    success_url = '/'
