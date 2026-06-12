from django.urls import path
from . import views

app_name = 'shop01'

urlpatterns = [
    path('login/', views.AccoutLogin.as_view(), name='login'),
    path('register_user/', views.AccountCreate.as_view(), name='register_user'),
    path('register_user_comfirm', views.AccountComfirm.as_view(), name='register_user_comfirm'),
    path('toppage/', views.Toppage.as_view(), name='toppage'),
]