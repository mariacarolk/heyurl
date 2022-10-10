from django.urls import path, re_path

from heyurl import views

urlpatterns = [
    path('', views.short_url, name='short_url'),
    path('metrics/', views.metrics, name='metrics'), #CACAU NOVA
]

handler404 = "heyurl.views.handler404"