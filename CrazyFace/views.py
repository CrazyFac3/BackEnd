from django.http import HttpResponse


def main_page(request):
    return HttpResponse('<h1>Main Page!</h1>')