"""
URL configuration for web_application project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from web_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.SignUpPage,name='signup'),
    path('login/',views.LoginPage,name='login'),
    path('home/',views.HomePage,name='home'),
    path('home/dash/',views.INDEX,name='admin'),
    path('add/',views.ADD,name='add'),
    path('edit/',views.Edit,name='edit'),
    path('update/<str:id>', views.Update, name='update'),
    path('delete/<str:id>',views.Delete),
    path('logout/',views.LogoutPage,name='logout'),
]
