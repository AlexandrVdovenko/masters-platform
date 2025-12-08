from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('', views.OrderListView.as_view(), name='order_list'),
    path('my/', views.MyOrdersView.as_view(), name='my_orders'),
    path('create/', views.OrderCreateView.as_view(), name='order_create'),
    path('<int:pk>/', views.OrderDetailView.as_view(), name='order_detail'),
    path('<int:pk>/edit/', views.OrderUpdateView.as_view(), name='order_update'),
    path('<int:pk>/delete/', views.OrderDeleteView.as_view(), name='order_delete'),
    path('<int:pk>/respond/', views.ResponseCreateView.as_view(), name='response_create'),
    path('response/<int:pk>/accept/', views.response_accept, name='response_accept'),
    path('response/<int:pk>/reject/', views.response_reject, name='response_reject'),
]
