from django.contrib import messages
from django.urls import reverse_lazy


class RoleContextMixin:
    """ Mixin для добавления роли в контекст"""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['role'] = self.kwargs['role']
        return context


class RoleSuccessUrlMixin:
    """ Mixin для передачи роли """

    url_name = ''

    def get_success_url(self):
        role = self.kwargs['role']
        return reverse_lazy(self.url_name, kwargs={'role': role})


class MessageValidFormMixin:
    """ Mixin для валидации"""
    success_message = ''
    error_message = ''

    def form_valid(self, form):
        form.save()
        messages.success(self.request, self.success_message)
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, self.error_message)
        return super().form_invalid(form)


class EducationsListMixin(RoleContextMixin):
    """
    Mixin для отображение списка курсов или программ обучения пользователя
    """

    context_object_name = 'educations'

    def get_queryset(self):
        user = self.request.user
        if self.kwargs['role'] == 'teacher':
            queryset = user.author_educations.all()
        else:
            queryset = user.educations_student.filter(
                education__is_online=self.request.GET.get('is_online')
            )
        return queryset
