# yourappname/views.py
from django.shortcuts import render

def my_view(request):
    return render(request, 'yourappname/my_template.html')
