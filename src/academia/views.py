from django.shortcuts import render

# Create your views here.

def home_view(request):
    return render(request, "pages/home.html", {})


def detail_view(request, id):
    return render(request, "pages/topic_detail.html", {})