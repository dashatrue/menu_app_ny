from django.urls import path
from . import views

#app_name = 'menu_app'

urlpatterns = [
    path('', views.MenuView.as_view(), name='menu'),
    path('order/', views.OrderSubmitView.as_view(), name='order_submit'),
]