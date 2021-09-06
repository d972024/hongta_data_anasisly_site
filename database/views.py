from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse

# Create your views here.
def reducecost(request):

    return render(request, 'database/table_reduceCost.html')