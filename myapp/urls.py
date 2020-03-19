from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="homepage"),
    path('register/', views.register_request, name="register"),
    path('login/', views.login_request, name='login'),
    path('logout/', views.logout_request, name='logout'),
    path('vaccination_add/', views.add_vaccines, name="add_vaccine"),
    path('vaccine_list/', views.vaccine_list, name='vaccine_list')
]
