from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.db.models import Exists, OuterRef, Q
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView
)
from django.urls import reverse_lazy
from django.utils import timezone

from .models import Cell, Tariff, Promotion, Order


class WorkerMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        user = self.request.user
        return user.is_staff or user.is_superuser


class AuthorWorkerMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        obj = self.get_object()
        user = self.request.user
        return obj.author == user or user.is_staff or user.is_superuser


class AuthorMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        obj = self.get_object()
        user = self.request.user
        return obj.author == user or user.is_superuser


class MeMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        obj = self.get_object()
        return obj == self.request.user or self.request.user.is_superuser


class CellMixin:
    model = Cell
    success_url = reverse_lazy('data:cell_list')
    template_name = 'data/cell_form.html'


class CellFormMixin:
    fields = 'number', 'size'


class CellListView(ListView):
    model = Cell
    ordering = 'number'
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset()

        today = timezone.now().date()
        active_orders = Order.objects.filter(
            cell=OuterRef('pk'),
            rental_start_date__lte=today,
            rental_end_date__gte=today,
            is_active=True
        )

        return queryset.annotate(
            is_free=~Exists(active_orders)
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        free_cells = self.object_list.filter(is_free=True)

        context['size_stats'] = {
            'small': free_cells.filter(size='small').count(),
            'medium': free_cells.filter(size='medium').count(),
            'large': free_cells.filter(size='large').count(),
        }

        user = self.request.user
        if not user.is_authenticated or not (user.is_staff or user.is_superuser):
            size_stats = context['size_stats']
            context.clear()
            context['size_stats'] = size_stats

        return context


class CellCreateView(WorkerMixin, CellMixin, CellFormMixin, CreateView):
    pass

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class CellUpdateView(AuthorMixin, CellMixin, CellFormMixin, UpdateView):
    pass


class CellDeleteView(AuthorMixin, CellMixin, DeleteView):
    pass


class ProfileMixin:
    model = User
    template_name = 'data/profile_form.html'
    success_url = reverse_lazy('data:cell_list')


class ProfileListView(WorkerMixin, ListView):
    model = User
    ordering = 'username'
    paginate_by = 5
    template_name = 'data/profile_list.html'


class ProfileDetailView(MeMixin, WorkerMixin, DetailView):
    model = User
    template_name = 'data/profile_detail.html'


class ProfileUpdateView(MeMixin, WorkerMixin, ProfileMixin, UpdateView):
    fields = 'username', 'first_name', 'last_name', 'email'


class ProfileDeleteView(MeMixin, ProfileMixin, DeleteView):
    pass


class TariffMixin:
    model = Tariff
    success_url = reverse_lazy('data:tariff_list')
    template_name = 'data/tariff_form.html'


class TariffFormMixin:
    fields = 'name', 'cell_size', 'duration', 'cost'


class TariffListView(ListView):
    model = Tariff
    ordering = 'name'
    paginate_by = 5


class TariffCreateView(WorkerMixin, TariffMixin, TariffFormMixin, CreateView):
    pass

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TariffUpdateView(AuthorMixin, TariffMixin, TariffFormMixin, UpdateView):
    pass


class TariffDeleteView(AuthorMixin, TariffMixin, DeleteView):
    pass


class PromotionMixin:
    model = Promotion
    success_url = reverse_lazy('data:promotion_list')
    template_name = 'data/promotion_form.html'


class PromotionFormMixin:
    fields = 'name', 'discount_percentage', 'start_date', 'end_date', 'description', 'promotion_type', 'target_user'


class PromotionListView(ListView):
    model = Promotion
    ordering = '-promotion_type'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()

        today = timezone.now().date()
        active_promotions = Promotion.objects.filter(
            id=OuterRef('pk'),
            start_date__lte=today,
            end_date__gte=today,
            is_active=True
        )

        queryset = queryset.annotate(
            is_current=Exists(active_promotions)
        )

        user = self.request.user
        if not (user.is_staff and user.is_superuser):
            if user.is_anonymous:
                queryset = queryset.filter(promotion_type='general')
            else:
                queryset = queryset.filter(
                    Q(target_user=self.request.user) |
                    Q(promotion_type='general')
                )

        return queryset


class PromotionCreateView(WorkerMixin, PromotionMixin, PromotionFormMixin, CreateView):
    pass

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PromotionUpdateView(AuthorMixin, PromotionMixin, PromotionFormMixin, UpdateView):
    pass


class PromotionDeleteView(AuthorMixin, PromotionMixin, DeleteView):
    pass


class OrderMixin:
    model = Order
    success_url = reverse_lazy('data:order_list')
    template_name = 'data/order_form.html'


class OrderFormMixin:
    fields = [
        'client', 'cell', 'tariff', 'promotion', 'rental_duration',
        'rental_start_date', 'content_description']


class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    ordering = '-rental_start_date'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        if not (self.request.user.is_staff and self.request.user.is_superuser):
            queryset = queryset.filter(author=self.request.user)
        return queryset


class OrderCreateView(WorkerMixin, OrderMixin, OrderFormMixin, CreateView):
    pass

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class OrderUpdateView(AuthorMixin, OrderMixin, OrderFormMixin, UpdateView):
    pass


class OrderDeleteView(AuthorMixin, OrderMixin, DeleteView):
    pass
