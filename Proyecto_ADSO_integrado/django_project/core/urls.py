from django.urls import path
from .views import HomeView, AdminHomeView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('admin/dashboard/', AdminHomeView.as_view(), name='admin_home'),
]
