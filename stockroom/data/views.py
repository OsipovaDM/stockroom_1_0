from django.views.generic import ListView, DetailView, CreateView, TemplateView

from .models import Cell, Tariff, Promotion, Order
from django.contrib.auth.models import User


class TariffListView(ListView):
    """
    Представление списка тарифов
    """
    model = Tariff
    ordering = 'id'
    paginate_by = 10


class PromotionListView(ListView):
    """
    Представление списка общих акций
    """
    model = Promotion
    ordering = 'end_date'
    paginate_by = 10
