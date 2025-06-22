from django.contrib import admin
from django.urls import path
from gateapp import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login_view, name='login'),
    path('guard/', views.guard_dashboard, name='guard_dashboard'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
]