

from django.http import HttpResponse

def home(request):
    print(request.user)
    return HttpResponse('Game_Feed')
    