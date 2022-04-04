"""
Definition of urls for DjangoWeb.
"""

from datetime import datetime
from django.urls import path
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from app import forms, views
from django.conf.urls import url
from app.views import IrisTrain,IrisPredict

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.home, name='home'),
    path('blog/', views.blog, name='blog'),
    path('blog/<int:pk>/',views.posting, name="posting"),
    path('blog/new_post/', views.new_post),
    path('blog/<int:pk>/remove/', views.remove_post),
        
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    url(r'^Train/', views.Train, name='Train'),

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
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)