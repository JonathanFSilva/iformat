"""iformats URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.conf.urls import url, include, handler400, handler403, handler404, handler500
from django.conf import settings

from django.contrib import admin
from django.contrib.auth import views


# handler400 = 'iformats.core.views.bad_request'
# handler403 = 'iformats.core.views.permission_denied'
# handler404 = 'iformats.core.views.page_not_found'
# handler500 = 'iformats.core.views.server_error'

urlpatterns = [
    url(r'^', include('iformats.core.urls')),
    url(r'^trabalhos/', include('iformats.trabalhos.urls')),

    url(r'oauth/', include('social_django.urls', namespace='social')),
    url(r'^logout/$', views.LogoutView.as_view(), name='logout'),

    url(r'^admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

