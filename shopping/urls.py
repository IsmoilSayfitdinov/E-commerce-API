from django.urls import path
from . import views


urlpatterns = [
    path("list/", views.ProductsViewListApi.as_view()),
    path("<int:id>/detail/", views.ProductsViewDetailApi.as_view()),
    path("", views.ProductsSearchApi.as_view()),
    path("cart/", views.CartViewList.as_view()),
    path("cart/add/", views.CartItemCreateAPIView.as_view()),
    path("cart/<int:pk>/checkout/", views.CheckoutView.as_view()),
    path("order/list/", views.ListallOrder.as_view()),
    path('cart/plus/<int:pk>/', views.CartItemPlusView.as_view(), name='cart-item-plus'),
    path('cart/minus/<int:pk>/', views.CartItemMinusView.as_view(), name='cart-item-minus'),
    path('cart/remove/<int:pk>/', views.CartItemRemoveView.as_view(), name='cart-item-remove'),

]