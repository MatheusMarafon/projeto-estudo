from django.http import HttpResponse


# Create your views here.
def django_view(request):
    return HttpResponse("<h1>Hello from the Django View!</h1>")
