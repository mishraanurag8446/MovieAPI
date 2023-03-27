from django.utils import timezone
# from MovieAPI.collection.models import RequestCounter


class RequestCounterMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # if request.path.startswith('/'):
        #     # Only count requests to the admin site
        #     return response
        #
        # # Get current date and time
        # current_time = timezone.now()
        #
        # # Get or create the RequestCounter object for the current date
        # request_counter, created = RequestCounter.objects.get_or_create(date=current_time.date())
        #
        # # Increment the request count and save the object
        # request_counter.count += 1
        # request_counter.save()
        #
        return response
