from django.urls import path
from . import views
urlpatterns = [
    path('<int:pk>/admin/detail/', views.ProductsAdminDetailView.as_view()),
    path('add/', views.ProductsAddView.as_view()),
    path("update/<int:pk>/", views.ProductsUpdateView.as_view()),
    path("<int:pk>/delete/", views.ProductsDelete.as_view()),
    path("users/", views.UserListView.as_view()),
    path("users/<int:pk>/", views.UserListDetailApiView.as_view()),
    path("orders/", views.ViewAllOrders.as_view()),
    path("user/<int:pk>/order/", views.ListOneUserOrders.as_view()),
    path("order/<int:pk>/update/", views.UserOrderUpdateView.as_view()),
]