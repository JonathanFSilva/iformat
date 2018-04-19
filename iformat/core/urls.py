from django.conf.urls import url

from . import views

app_name = 'iformat.core'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    # url(r'^home/$', views.home, name='home'),
    url(r'^contact/$', views.contact, name='contact'),
]