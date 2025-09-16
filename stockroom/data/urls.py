from django.urls import path

from . import views

app_name = 'data'

urlpatterns = [
    # path('', views.index, name='index'),
    # path('tariffs/', views.tariffs, name='tariffs'),
    # path('promotions/', views.promotions, name='promotions'),
    path('cells/', views.CellListView.as_view(), name='cell_list'),
    path('cells/create/', views.CellCreateView.as_view(), name='cell_create'),
    # path('cells/<int:id>/', views.CellListView.as_view(), name='cell_detail'),
    path('cells/<int:pk>/edit/', views.CellUpdateView.as_view(), name='cell_edit'),
    path('cells/<int:pk>/delete/', views.CellDeleteView.as_view(), name='cell_delete'),
    # path('orders/', views.orders, name='orders'),
    # path('orders/create/', views.order_create, name='order_create'),
    # path('orders/<int:id>/', views.order_detail, name='order_detail'),
    # path('orders/<int:id>/edit/', views.order_edit, name='order_edit'),
    # path('orders/<int:id>/delete/', views.order_delete, name='order_delete'),
    # path('me/', views.account, name='account'),
    path('profile/<int:pk>/', views.ProfileDetailView.as_view(), name='profile_detail'),
    path('profile/<int:pk>/edit/', views.ProfileUpdateView.as_view(), name='profile_edit'),
    path('profile/<int:pk>/delete/', views.ProfileDeleteView.as_view(), name='profile_delete'),
    # path('/', views., name=''),
    # path('/', views., name=''),
    # path('/', views., name=''),
    # path('/', views., name=''),
    ]
