from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
    path('executor/<int:executor_id>/', views.ReviewListView.as_view(), name='review_list'),
    path('create/<int:order_id>/', views.ReviewCreateView.as_view(), name='review_create'),
    path('<int:pk>/edit/', views.ReviewUpdateView.as_view(), name='review_update'),
    path('<int:pk>/respond/', views.executor_respond, name='executor_respond'),
]
