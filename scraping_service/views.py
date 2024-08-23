import datetime
from django.shortcuts import render


def home(request):
    date = datetime.datetime.now().date()
    name = "Adolf"
    zalupa = {"date": date, "name": name}
    return render(request, "home.html", zalupa)
