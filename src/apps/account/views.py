from django import forms
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, View, ListView, DetailView, FormView, UpdateView
from extra_views import ModelFormSetView

from apps.education.models import Education, Subject, Section, Lecture
from apps.education.models import Grade
from .forms import (
    DocumentsForm, StudentsWorksForm, UserRegistrationForm, PortfolioStudentForm
)
from .mixins import MessageValidFormMixin, RoleContextMixin, RoleSuccessUrlMixin, EducationsListMixin
from .models import Portfolio
from .models import User


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
    LoginRequiredMixin, RoleContextMixin, RoleSuccessUrlMixin, UpdateView,
    MessageValidFormMixin
):
    """
    View для редактирования профиля пользователя.
    """

    template_name = 'account/base/profile_edit.html'
    success_message = 'Профиль успешно обновлен'
    error_message = 'Ошибка при обновлении вашего профиля'
    url_name = 'edit'
    fields = (
        'first_name', 'reporting', 'last_name', 'email',
        'date_of_birth', 'photo', 'telephone'
    )

    def get_object(self, queryset=None):
        return self.request.user


class EducationsView(EducationsListMixin, LoginRequiredMixin, ListView):
    """
    Отображение всех программ обучения студента
    """

    def get_template_names(self):
        return f"account/{self.kwargs['role']}/educations_list.html"


class SubjectsView(RoleContextMixin, LoginRequiredMixin, ListView):
    """
    Отображение всех программ обучения студента
    """

    context_object_name = 'subjects'

    def get_template_names(self):
        return f"account/{self.kwargs['role']}/my_subjects.html"

    def get_queryset(self):
        return self.request.user.teacher_educations.all()


class EducationView(LoginRequiredMixin, RoleContextMixin, DetailView):
    """
    Отображение одной программы обучения пользователя и дисциплин
    """
    model = Education
    context_object_name = 'education'
    pk_url_kwarg = 'id_education'

    def get_template_names(self):
        return f"account/{self.kwargs['role']}/education_detail.html"


class EducationOflineView(LoginRequiredMixin, RoleContextMixin, DetailView):
    """
    Отображение одной программы обучения пользователя и дисциплин
    """
    model = Education
    context_object_name = 'education'
    pk_url_kwarg = 'id_education'

    def get_template_names(self):
        return f"account/{self.kwargs['role']}/education_ofline_detail.html"


class SubjectView(LoginRequiredMixin, RoleContextMixin, DetailView):
    """
    Отображение одной дисциплины и разделов
    """
    model = Subject
    context_object_name = 'subject'
    pk_url_kwarg = 'id_subject'

    def get_template_names(self):
        return f"account/{self.kwargs['role']}/subject_detail.html"


class SectionView(LoginRequiredMixin, RoleContextMixin, DetailView):
    """
    Отображение одного раздела и лекции
    """
    model = Section
    context_object_name = 'section'
    pk_url_kwarg = 'id_section'

    def get_template_names(self):
        return f"account/{self.kwargs['role']}/section_detail.html"


class LectureView(LoginRequiredMixin, RoleContextMixin, DetailView):
    """
    Отображение одной лекции
    """
    model = Lecture
    context_object_name = 'lecture'
    pk_url_kwarg = 'id_lecture'

    def get_template_names(self):
        return f"account/{self.kwargs['role']}/lecture_detail.html"


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
    form_class = PortfolioStudentForm
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


class StudentsWorksView(LoginRequiredMixin, RoleContextMixin, ModelFormSetView):
    """
    Отображение портфолио пользователя
    """
    model = Portfolio
    form_class = StudentsWorksForm
    template_name = 'account/teacher/students_works.html'
    fields = ['file', 'grade']
    factory_kwargs = {
        'extra': 0,
        'edit_only': True,

        'widgets': {
            'grade': forms.NumberInput(attrs={'required': False}),
            'file': forms.FileInput(attrs={'required': False})
        }
    }

    def get_queryset(self):
        user = self.request.user
        return Portfolio.objects.filter(teacher=user).order_by('date_added')

    def formset_valid(self, formset):
        for form in formset:
            if form.cleaned_data.get('grade_value') and not form.instance.grade:
                g = Grade(grade_100=form.cleaned_data['grade_value'])
                g.save()
                form.instance.grade = g
                form.save()
        return redirect('students_works', role=self.kwargs['role'])

    def formset_invalid(self, formset):
        print(formset.errors)

        return JsonResponse({})
