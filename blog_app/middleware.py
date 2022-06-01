
class HeaderMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.token = request.META.get('HTTP_X_API_TOKEN', None)   
        
        response = self.get_response(request)

        return response