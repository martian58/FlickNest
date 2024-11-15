from django.shortcuts import render

# Create your views here.



def index(request):

    return render(request, 'index.html', {})


def dashboard_view(request):

    return render(request, 'dashboard.html', {})




def watch_movie(request):

    return render(request, 'watch.html', {})
