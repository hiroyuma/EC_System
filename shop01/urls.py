from django.urls import path
from . import views

app_name = 'shop01'

urlpatterns = [
    path('login/', views.UserLogin.as_view(), name='login'),
    path('register_user/', views.UserCreate.as_view(), name='register_user'),
    path('register_user_confirm/', views.UserConfirm.as_view(), name='register_user_confirm'),
    path('', views.Toppage.as_view(), name='toppage'),
    path('logout/', views.UserLogout.as_view(), name='logout'),
    path('user_info/', views.UserDetail.as_view(), name='user_info'),
    path('update_user', views.UpdataUser.as_view(), name='update_user'),
    path('update_user_confirm/', views.UpdateUserConfirm.as_view(), name='update_user_confirm'),
    path('withdraw_confirm/', views.Withdraw.as_view(), name='withdrawconfirm'),
    path('withdraw_commit/', views.withdrawCommit.as_view(), name='withdrawcommit'),
    path('search_result/', views.SearchResult.as_view(), name='search_result'),
    path('item_detail/<int:item_id>/', views.ItemDetail.as_view(), name='item_detail'),
    path('cart/', views.Cart.as_view(), name='cart'),
    path('update_cart/', views.UpdateCart.as_view(), name = 'update_cart'),
    path('delete_cart/', views.DeleteCart.as_view(), name = 'delete_cart'),
    path('main/', views.SearchItem.as_view(), name = 'main'),
    path('manager/main/', views.AdminMain.as_view(), name='admin_main'),
    path('manager/item/create/', views.AdminItemCreate.as_view(), name='admin_item_create'),
    path('manager/item/<int:item_id>/delete/', views.AdminItemDelete.as_view(), name='admin_item_delete'),
    path('manager/item/<int:item_id>/recommend/', views.AdminRecommendToggle.as_view(), name='admin_item_recommend'),
    path('manager/main/', views.AdminMain.as_view(), name='admin_main'),
    path('manager/purchase/<int:purchase_id>/cancel/', views.AdminPurchaseCancel.as_view(), name='admin_purchase_cancel'),
    path("admin_login", views.AdminLogin.as_view(), name = 'admin_login'),
    path('manager/main/', views.AdminMain.as_view(), name='admin_main'),
    path('purchase/', views.PurchaseView.as_view(), name='purchase'),
    path('purchase/commit/', views.PurchaseCommitView.as_view(), name='purchase_commit'),
    path('purchase/history/', views.PurchaseHistoryView.as_view(), name='purchase_history'),
]