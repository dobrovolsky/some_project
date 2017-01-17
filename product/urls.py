"""test_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^(?P<page>[0-9]+)', views.ProductListView.as_view(), name='products_page'),
    url(r'^add_comment/(?P<slug>[\w-]+)', views.CommentView.as_view(), name='add_comment'),
    url(r'login', views.LoginView.as_view(), name='login'),
    url(r'logout', views.LogoutView.as_view(), name='logout'),
    url(r'like/(?P<slug>[\w-]+)', views.LikeView.as_view(), name='like'),
    url(r'^(?P<slug>[-\w]+)', views.ProductDetailView.as_view(), name='product_slug'),
    url(r'^', views.ProductListView.as_view(), name='products'),
]
