# from django.urls import path
from django.conf.urls import include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from . import views
from subscribe.views import TableView
urlpatterns = [
    # path('', views.subscribe, name = 'subscribe'),
    url('',TableView.as_view())
]
urlpatterns += staticfiles_urlpatterns()


# urlpatterns = [
#     url(r'^$', include('subscribe.urls')),
#     url(r'^admin/', admin.site.urls),
# ]