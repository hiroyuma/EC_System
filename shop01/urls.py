from django.urls import path
from . import views

app_name = 'shop01'

urlpatterns = [
    path('login/', views.UserLogin.as_view(), name='login'),
    path('register_user/', views.UserCreate.as_view(), name='register_user'),
    path('register_user_comfirm', views.UserComfirm.as_view(), name='register_user_comfirm'),
    path('toppage/', views.Toppage.as_view(), name='toppage'),
    path('logout/', views.UserLogout.as_view(), name='logout'),
    path('user_info/', views.UserDetail.as_view(), name='user_info'),
    path('update_user', views.UpdataUser.as_view(), name='update_user'),
    path('update_user_comfirm', views.UpdateUserComfirm.as_view(), name='update_user_comfirm'),
    path('withdrawcomfirm', views.Withdraw.as_view(), name='withdrawcomfirm'),
    path('withdrawcommit', views.withdrawCommit.as_view(), name='withdrawcommit'),
    path('main/', views.SearchItem.as_view(), name = 'main'),
]