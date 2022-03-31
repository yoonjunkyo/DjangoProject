"""
Definition of urls for DjangoWeb.
"""

from datetime import datetime
from django.urls import path
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from app import forms, views
from django.conf.urls import url

from app.views import IrisTrain
from app.views import IrisPredict

urlpatterns = [
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    url(r'^Train$', views.Train, name='Train'),
    url(r'^Predict/',views.Predict,name="Predict"),

    url(r'^IrisTrain/',IrisTrain.as_view(),name="IrisTrain"),
    url(r'^IrisPredict/',IrisPredict.as_view(),name="IrisPredict"),

    path('login/',
         LoginView.as_view
         (
             template_name='app/login.html',
             authentication_form=forms.BootstrapAuthenticationForm,
             extra_context=
             {
                 'title': 'Log in',
                 'year' : datetime.now().year,
             }
         ),
         name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('admin/', admin.site.urls)
]
