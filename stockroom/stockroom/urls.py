from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView
from django.contrib import admin
from django.urls import include, path, reverse_lazy

urlpatterns = [
    path('', include('data.urls')),
    path('admin/', admin.site.urls),
    path(
        'auth/registration/',
        CreateView.as_view(
            template_name='registration/registration_form.html',
            form_class=UserCreationForm,
            success_url=reverse_lazy('data:cell_list'),
        ),
        name='registration',
    ),
    path('auth/', include('django.contrib.auth.urls')),
]
