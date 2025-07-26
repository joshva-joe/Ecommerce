from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    # Admin URLs
    path('', views.adminsignup, name='adminsignup'),
    path('adminlogin/', views.adminlogin, name='adminlogin'),
    path('admin/', views.admin, name='admin_dashboard'),

    # Seller URLs
    path('seller/profile/', views.seller_profile, name='seller_profile'),
    path('selleradd/', views.selleradddata, name='seller_add'),

    # Product Management
    path('addproduct/', views.productadd, name='add_product'),
    path('editproduct/<str:product_id>/', views.edit_product, name='edit_product'),  # ✅ fixed route
    path('deleteproduct/<str:product_id>/', views.delete_product, name='delete_product'),
    path('deleteadmin/<str:product_id>/', views.admindelete_product, name='admin_delete_product'),

    # Customer, Seller, Product Listings (Admin View)
    path('customer/', views.customer, name='homepage'),
    path('products/', views.products, name='products'),
    path('sellers/', views.sellers, name='sellers'),
    path('customers/', views.customershow, name='customershow'),
    path('orders/', views.ordershow, name='orders'),

    # Admin Delete Routes
    path('adminseller/<str:sellername>/', views.admindelete_seller, name='admin_delete_seller'),
    path('admincustomer/<str:customer_name>/', views.admindelete_customer, name='admin_delete_customer'),
    path('adminorder/<str:product_id>/', views.admindelete_orders, name='admin_delete_order'),

    # Order and Purchase
    path('buyproduct/<str:product_id>/', views.buyproduct, name='buy_product'),
    path('orderpage/<str:product_id>/', views.productorder, name='order'),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
