from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView
)
from django.urls import reverse_lazy

from .models import Cell, Tariff


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
    paginate_by = 5


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


'''
class PromotionMixin:
    model = Promotion
    success_url = reverse_lazy('data:promotions')


class PromotionFormMixin:
    template_name = 'promotion/create.html'
    fields = 


class PromotionCreateView(PromotionMixin, PromotionFormMixin, CreateView):
    pass

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PromotionUpdateView(PromotionMixin, PromotionFormMixin, UpdateView):
    pass


class PostDeleteView(PromotionMixin, DeleteView):
    pass


class OrderMixin:
    model = Order
    success_url = reverse_lazy('data:Orders')


class OrderFormMixin:
    template_name = 'Order/create.html'
    fields = 


class OrderCreateView(OrderMixin, OrderFormMixin, CreateView):
    pass

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class OrderUpdateView(OrderMixin, OrderFormMixin, UpdateView):
    pass


class OrderDeleteView(OrderMixin, DeleteView):
    pass
'''