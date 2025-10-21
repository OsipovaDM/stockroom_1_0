from django.urls import path

from . import views

app_name = 'data'

urlpatterns = [
    path('cells/', views.CellListView.as_view(), name='cell_list'),
    path('cells/create/', views.CellCreateView.as_view(), name='cell_create'),
    path('cells/<int:pk>/edit/', views.CellUpdateView.as_view(), name='cell_edit'),
    path('cells/<int:pk>/delete/', views.CellDeleteView.as_view(), name='cell_delete'),
    # path('cells/<int:id>/', views.CellListView.as_view(), name='cell_detail'),

    path('profile/list/', views.ProfileListView.as_view(), name='profile_list'),
    path('profile/<int:pk>/', views.ProfileDetailView.as_view(), name='profile_detail'),
    path('profile/<int:pk>/edit/', views.ProfileUpdateView.as_view(), name='profile_edit'),
    path('profile/<int:pk>/delete/', views.ProfileDeleteView.as_view(), name='profile_delete'),

    path('tariffs/', views.TariffListView.as_view(), name='tariff_list'),
    path('tariffs/create/', views.TariffCreateView.as_view(), name='tariff_create'),
    path('tariffs/<int:pk>/edit/', views.TariffUpdateView.as_view(), name='tariff_edit'),
    path('tariffs/<int:pk>/delete/', views.TariffDeleteView.as_view(), name='tariff_delete'),

    path('promotions/', views.PromotionListView.as_view(), name='promotion_list'),
    path('promotions/create/', views.PromotionCreateView.as_view(), name='promotion_create'),
    path('promotions/<int:pk>/edit/', views.PromotionUpdateView.as_view(), name='promotion_edit'),
    path('promotions/<int:pk>/delete/', views.PromotionDeleteView.as_view(), name='promotion_delete'),

    # path('orders/', views.orders, name='orders'),
    # path('orders/create/', views.order_create, name='order_create'),
    # path('orders/<int:id>/', views.order_detail, name='order_detail'),
    # path('orders/<int:id>/edit/', views.order_edit, name='order_edit'),
    # path('orders/<int:id>/delete/', views.order_delete, name='order_delete'),
    # path('me/', views.account, name='account'),
    # path('', views.index, name='index'),
    # path('promotions/', views.promotions, name='promotions'),
    # path('/', views., name=''),
    # path('/', views., name=''),
    # path('/', views., name=''),
    # path('/', views., name=''),
    ]
