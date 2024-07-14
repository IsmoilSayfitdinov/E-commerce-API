from django.urls import path
from . import views


urlpatterns = [
    path("list/", views.ProductsViewListApi.as_view()),
    path("<int:id>/detail/", views.ProductsViewDetailApi.as_view()),
    path("", views.ProductsSearchApi.as_view()),
    path('cart/', views.CartListApiView.as_view(), name='cart-list'),
    path('cart/add/', views.AddToCartAPIView.as_view(), name='cart-add'),
    path('cart/<int:pk>/checkout/', views.CartCheckoutAPIView.as_view(), name='cart-checkout'),
    path('order/list/', views.OrderListAPIView.as_view(), name='order-list'),
    path('cart/plus/<int:pk>/', views.CartPlusProductAPIView.as_view(), name='cart-plus'),
    path('cart/minus/<int:pk>/', views.CartMinusProductAPIView.as_view(), name='cart-minus'),
    path('cart/remove/<int:pk>/', views.CartRemoveProductAPIView.as_view(), name='cart-remove'),

]