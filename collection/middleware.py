from datetime import datetime

from .models import RequestCounter


class RequestCounterMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.path.startswith('/admin/'):
            return response

        date = datetime.now().date()
        request_counter, created = RequestCounter.objects.get_or_create(id=1)
        request_counter.count += 1
        request_counter.save()

        return response
