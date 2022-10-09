from django.urls import path, re_path

from heyurl import views

urlpatterns = [
    path('', views.short_url, name='short_url'),
    path('metrics/', views.metrics, name='metrics'),
]
