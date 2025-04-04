from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('product/<int:id>/', views.product_detail, name='product_detail'),
    path('product/add/', views.product_create, name='product_create'),
    path('product/<int:id>/edit/', views.product_edit, name='product_edit'),
    path('delete-product/<int:product_id>/', views.delete_product, name='delete_product'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_view, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('admin-panel/', views.admin_panel, name='admin_panel'),
    path('manage-users/', views.manage_users, name='manage_users'),  # добавлен маршрут
    path('manage-users/', views.manage_users, name='manage_users'),
    path('delete-user/<int:user_id>/', views.delete_user, name='delete_user'),  # Маршрут для удаления
]
