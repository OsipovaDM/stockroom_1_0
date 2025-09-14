from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, DeleteView, UpdateView, ListView
from django.urls import reverse_lazy

from .models import Cell


class AuthorMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user or self.request.user.is_admin


class CellMixin:
    model = Cell
    success_url = reverse_lazy('data:cell_list')
    template_name = 'data/cell_form.html'


class CellFormMixin:
    fields = 'number', 'size'


class CellListView(ListView):
    model = Cell
    ordering = 'number'
    paginated_by = 10


class CellCreateView(LoginRequiredMixin, CellMixin, CellFormMixin, CreateView):
    pass

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class CellUpdateView(AuthorMixin, CellMixin, CellFormMixin, UpdateView):
    pass


class CellDeleteView(AuthorMixin, CellMixin, DeleteView):
    pass




'''


class TariffMixin:
    model = Tariff
    success_url = reverse_lazy('data:tariffs')


class TariffFormMixin:
    template_name = 'tariff/create.html'
    fields = 'name', 'cell_size', 'duration', 'cost', 'is_active', 'author'


class TariffListView(ListVieW):
    model = Tariff
    ordering = 'cost'
    paginate_by = 10


class TariffCreateView(TariffMixin, TariffFormMixin, CreateView):
    pass

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TariffUpdateView(TariffMixin, TariffFormMixin, UpdateView):
    pass


class TariffDeleteView(TariffMixin, DeleteView):
    pass
    

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