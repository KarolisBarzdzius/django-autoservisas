from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('cars/', views.cars, name='cars'),
    path('cars/<int:car_id>',views.car,name='car'),
    path('orders/',views.OrdersListView.as_view(),name='orders'),
    path('orders/<int:pk>',views.OrderDetailView.as_view(),name='order'),
    path('search/', views.search, name='search'),
    path('search/<int:car_id>', views.car, name='car'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('myorders/', views.OrdersByUserListView.as_view(), name='my_orders'),
    path('myorders/new', views.OrdersByUserCreateView.as_view(), name='my_orders_new'),
    path('myorders/<int:pk>/delete', views.OrdersByUserDeleteView.as_view(), name='my_order_delete'),
    path('myorders/<int:pk>/update', views.OrdersByUserUpdateView.as_view(), name='my_order_update'),



]
