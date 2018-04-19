from django.conf.urls import url

from . import views

app_name = 'iformat.trabalhos'
urlpatterns = [
    url(r'^$', views.trabalhos, name='trabalhos'),

    url(r'^novo/$', views.preambulo, name='preambulo'),
    url(r'^(?P<trabalho_id>[0-9]+)/dados/editar/$', views.editar_preambulo, name='editar_preambulo'),
    url(r'^(?P<trabalho_id>[0-9]+)/excluir/$', views.excluir_trabalho, name='excluir_trabalho'),

    url(r'^(?P<trabalho_id>[0-9]+)/topico/novo/$', views.topico, name='topico'),
    url(r'^(?P<trabalho_id>[0-9]+)/topico/(?P<topico_id>[0-9]+)/editar/$', views.editar_topico, name='editar_topico'),
    url(r'^(?P<trabalho_id>[0-9]+)/topico/(?P<topico_id>[0-9]+)/excluir/$', views.editar_topico, name='excluir_topico'),

    url(r'^(?P<trabalho_id>[0-9]+)/inicio/$', views.inicio, name='inicio'),
    url(r'^(?P<trabalho_id>[0-9]+)/download/$', views.download_pdf, name='download'),
    url(r'^(?P<trabalho_id>[0-9]+)/visualizar/$', views.view_pdf, name='visualizar'),
]