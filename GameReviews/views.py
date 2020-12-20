from django.shortcuts import render
from myproject.settings import EMAIL_HOST_USER
from . import forms
from django.core.mail import send_mail
import requests
import django_tables2 as tables
from .models import Reviews
from .tables import ReviewsTable
from .filters import ReviewsFilter
from .forms import ReviewsListFormHelper
from .utils import PagedFilteredTableView

# Create your views here.
class TableView(PagedFilteredTableView):
    model = Reviews
    table_class = ReviewsTable
    template_name = 'subscribe/index.html'
    filter_class = ReviewsFilter
    formhelper_class = ReviewsListFormHelper

def subscribe(request):
    '''Currently not in use. Used for email subscription button'''

    tmpStr = ''
    data = Reviews.objects.all()
    sub = forms.Subscribe()
    if request.method == 'POST':
        # x = requestReviews(tmpStr) #Outdated, if I decide to re-enable email later I will need to pull from database instead of a GET request
        x = ''
        tmpStr += x
        sub = forms.Subscribe(request.POST)
        subject = 'Game Reviews for the Week' 
        message = 'What\'s up gamer,\n    Here are your game reviews for the week:\n\n' + tmpStr
        recepient = str(sub['Email'].value())
        send_mail(subject, 
            message, EMAIL_HOST_USER, [recepient], fail_silently = False)
        return render(request, 'subscribe/success.html', {'recepient': recepient})
    return render(request, 'subscribe/index.html', {'form':sub, "link": data})
