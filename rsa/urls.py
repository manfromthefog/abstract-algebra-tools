from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='rsa-home'),
    path('generate/', views.generate_keys, name='rsa-generate'),
    path('encrypt', views.encrypt, name='rsa-encrypt'),
    path('decrypt/', views.decrypt, name='rsa-decrypt'),
]
