from bboard.models import Rubric


def my_middleware(next):
    # Здесь можно выполнить какую-либо инициализацию
    def core_middleware(request):
        # Здесь выполняется обработка клиентского запроса
        response = next(request)
        # Здесь выполняется обработка ответа
        return response

    return core_middleware


class MyMiddleware:
    def __init__(self, next):
        self.next = next

    # Здесь можно выполнить какую-либо инициализацию
    def __call__(self, request):
        # Здесь выполняется обработка клиентского запроса
        response = self.next(request)
        # Здесь выполняется обработка ответа
        return response


class RubricsMiddleware:

    def init(self, get_response):
        self.get_response = get_response

    def call(self, request):
        return self.get_response(request)

    def process_template_response(self, request, response):
        response.context_data['rubrics'] = Rubric.objects.all()
        return response
