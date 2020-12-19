from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from . import views
from subscribe.views import TableView
urlpatterns = [
    # path('', views.subscribe, name = 'subscribe'),
    path('',TableView.as_view())
]
urlpatterns += staticfiles_urlpatterns()