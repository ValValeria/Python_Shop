"""hello URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path,re_path,include
from firstapp import views

urlpatterns = [
    re_path(r"^$",views.Home.as_view()),
    path('admin/', admin.site.urls),
    re_path(r'^public/(?P<folder>\w+)/(?P<filename>\w+)',views.Files.as_view()),
    re_path(r"^signup",views.SignUp.as_view(),name="signup"),
    re_path(r'^logout',views.logOut),
    re_path(r'^login',views.Login.as_view()),
   
    re_path(r"^auth/dash/(?P<id>\d+)",views.Dash.as_view()),
    re_path(r"^delete_user/(?P<pk>\d+)",views.DeleteUser.as_view()),
    re_path(r"^addnewuser",views.AddUser.as_view()),
    re_path(r"^product/(?P<pk>\d+)",views.Product.as_view(),name="product"),
    re_path(r"^order/(?P<pk>\d+)",views.Order.as_view()),
    re_path(r'^data',views.DataNews.as_view()),
    re_path(r'^categories/(?P<category>\w+)/(?P<p>\d+)',views.ShowCategory.as_view()),
    re_path(r'^find$',views.Cat.as_view()),

    re_path(r"",views.findFile),


]
