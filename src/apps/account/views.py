from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, View, ListView, DetailView, FormView

from .forms import (
    DocumentsForm, PortfolioForm, UserEditForm, UserRegistrationForm
)
from .models import User
from apps.education.models import Education


class RoleContextMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['role'] = self.kwargs['role']
        return context


class RoleSuccessUrlMixin:
    url_name = ''

    def get_success_url(self):
        role = self.kwargs['role']
        return reverse_lazy(self.url_name, kwargs={'role': role})


class MessageValidFormMixin:
    success_message = ''
    error_message = ''

    def form_valid(self, form):
        form.save()
        messages.success(self.request, self.success_message)
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, self.error_message)
        return super().form_invalid(form)


class RegisterView(CreateView):
    """
    View для регистрации пользователя.
    """
    form_class = UserRegistrationForm
    model = User
    template_name = 'registration/register_form.html'
    success_url = reverse_lazy('register_done')

    def form_valid(self, form):
        new_user = form.save(commit=False)
        new_user.set_password(form.cleaned_data['password'])
        new_user.save()
        return super().form_valid(form)


class ProfileView(LoginRequiredMixin, View):
    """
    View для отображения страницы личного кабинета пользователя.
    """

    def get(self, request, role=None):
        user = request.user
        roles = user.roles.all()
        if role is None:
            role = roles.first().name if user.roles.exists() else None
        if role:
            return render(
                request, "account/base/profile.html",
                context={'user': user, 'role': role}
            )
        return render(request, 'registration/login.html')


class EditProfileView(
    LoginRequiredMixin, RoleContextMixin, RoleSuccessUrlMixin, FormView,
    MessageValidFormMixin
):
    """
    View для редактирования профиля пользователя.
    """

    template_name = 'account/base/profile_edit.html'
    form_class = UserEditForm
    success_message = 'Профиль успешно обновлен'
    error_message = 'Ошибка при обновлении вашего профиля'
    url_name = 'edit'


class EducationsListView(LoginRequiredMixin, RoleContextMixin, ListView):
    """
    Отображение списка курсов или программ обучения пользователя
    """

    context_object_name = 'educations'
    is_online = None

    def get_queryset(self):
        user = self.request.user
        if self.kwargs['role'] == 'teacher':
            queryset = user.educations_teacher.filter(
                education__is_online=self.is_online
            )
        else:
            queryset = user.educations_student.filter(
                education__is_online=self.is_online
            )
        return queryset


class CoursesView(EducationsListView):
    """
    Отображение всех курсов пользователя
    """

    template_name = "account/student/courses_list.html"
    is_online = True


class EducationsView(EducationsListView):
    """
    Отображение всех программ обучения пользователя
    """

    template_name = "account/student/educations_list.html"
    is_online = False


class StudentCourseView(LoginRequiredMixin, RoleContextMixin, DetailView):
    """
    Отображение одного курса пользователя
    """
    model = Education
    context_object_name = 'education'
    pk_url_kwarg = 'id_education'
    template_name = "account/student/course_detail.html"


class StudentEducationView(LoginRequiredMixin, RoleContextMixin, DetailView):
    """
    Отображение одной программы обучения пользователя
    """
    model = Education
    context_object_name = 'education'
    pk_url_kwarg = 'id_education'
    template_name = "account/student/education_detail.html"


class ScheduleView(View):
    """
    Отображение расписания пользователя
    """

    def get(self, request, role):
        return render(request, 'account/student/schedule.html', {'role': role})


class StudentPortfolioView(LoginRequiredMixin, RoleContextMixin, ListView):
    """
    Отображение портфолио пользователя
    """

    template_name = 'account/student/portfolio.html'
    context_object_name = 'portfolio_list'

    def get_queryset(self):
        user = self.request.user
        return user.portfolio.all()


class DocumentsUserView(LoginRequiredMixin, RoleContextMixin, ListView):
    """
    Отображение портфолио пользователя
    """

    template_name = "account/base/documents_user.html"
    context_object_name = 'documents_list'

    def get_queryset(self):
        user = self.request.user
        return user.documents.all()


class UploadPortfolioView(
    LoginRequiredMixin, RoleContextMixin, RoleSuccessUrlMixin, CreateView,
    MessageValidFormMixin
):
    """
    View для загрузки портфолио.
    """
    form_class = PortfolioForm
    template_name = 'account/student/add_portfolio.html'
    url_name = 'add_portfolio'
    success_message = 'Портфолио успешно загружено.'
    error_message = 'Ошибка при загрузке портфолио.'

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        messages.success(self.request, self.success_message)
        return super().form_valid(form)


class AddDocumentsView(
    LoginRequiredMixin, RoleContextMixin, RoleSuccessUrlMixin, CreateView,
    MessageValidFormMixin
):
    """
    View для добавления документов.
    """
    form_class = DocumentsForm
    template_name = 'account/base/add_document.html'
    url_name = 'add_documents'
    success_message = 'Документ успешно загружен.'
    error_message = 'Ошибка при загрузке документа.'

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        messages.success(self.request, self.success_message)
        return super().form_valid(form)


class StudentsWorksView(View):
    def get(self, request, role):
        return render(
            request, "account/teacher/students_works.html",
            context={'role': role}
        )
