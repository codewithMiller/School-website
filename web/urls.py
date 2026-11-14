from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('academics/', views.academics, name='academics'),
    path('admissions/', views.admissions, name='admissions'),
    path('apply/', views.apply, name='apply'),
    path('apply/success/', views.apply_success, name='apply_success'),
    path('news/', views.news_list, name='news_list'),
    path('news/<int:pk>/', views.news_detail, name='news_detail'),
    path('gallery/', views.gallery, name='gallery'),
    path('staff/', views.staff, name='staff'),
    path('contact/', views.contact, name='contact'),

    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]