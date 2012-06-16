from .models import Request

class StoreRequestMiddleware:
    def process_request(self, request):
        r = Request()
        r.method = request.method
        r.path = request.path
        r.save()
