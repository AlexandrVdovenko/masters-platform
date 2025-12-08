from django.urls import path
from . import views

app_name = 'portfolio'

urlpatterns = [
    path('<int:user_id>/', views.PortfolioListView.as_view(), name='portfolio_list'),
    path('create/', views.PortfolioCreateView.as_view(), name='portfolio_create'),
    path('<int:pk>/edit/', views.PortfolioUpdateView.as_view(), name='portfolio_update'),
    path('<int:pk>/delete/', views.PortfolioDeleteView.as_view(), name='portfolio_delete'),
]
