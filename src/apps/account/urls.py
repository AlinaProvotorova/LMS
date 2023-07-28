from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views
from django.urls import path
from django.views.generic.base import TemplateView

from .views import (
    AddDocumentsView, DocumentsUserView, EditProfileView, ProfileView,
    RegisterView, ScheduleView, StudentCourseView, CoursesStudentView,
    EducationView, EducationsView, StudentPortfolioView,
    UploadPortfolioView, SubjectView, SectionView,
    LectureView, StudentsWorksView, SubjectsView
)

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('register/done/',
         TemplateView.as_view(template_name='registration/register_done.html'),
         name='register_done'
         ),
    path(
        'password-change/', views.PasswordChangeView.as_view(),
        name='password_change'
    ),
    path(
        'password-change/done/', views.PasswordChangeDoneView.as_view(),
        name='password_change_done'
    ),
    path(
        'password-reset/', views.PasswordResetView.as_view(),
        name='password_reset'
    ),
    path(
        'password-reset/done/', views.PasswordResetDoneView.as_view(),
        name='password_reset_done'
    ),
    path(
        'reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(),
        name='password_reset_confirm'
    ),
    path(
        'reset/done/', views.PasswordResetCompleteView.as_view(),
        name='password_reset_complete'
    ),

    path('', ProfileView.as_view(), name='dashboard'),
    path('<str:role>/', ProfileView.as_view(), name='profile'),
    path('<str:role>/edit/', EditProfileView.as_view(), name='edit'),
    path('<str:role>/course', CoursesStudentView.as_view(), name='courses_list'),
    path('<str:role>/education', EducationsView.as_view(), name='educations'),
    path('<str:role>/subjects', SubjectsView.as_view(), name='subjects'),
    path('<str:role>/schedule', ScheduleView.as_view(), name='schedule'),
    path(
        '<str:role>/portfolio', StudentPortfolioView.as_view(),
        name='portfolio'
    ),
    path(
        '<str:role>/documents', DocumentsUserView.as_view(),
        name='documents_user'
    ),
    path(
        '<str:role>/course/<id_education>', StudentCourseView.as_view(),
        name='student_course_detail'
    ),
    path(
        '<str:role>/education/<id_education>', EducationView.as_view(),
        name='education_detail'
    ),
    path(
        '<str:role>/subject/<id_subject>', SubjectView.as_view(),
        name='subject_detail'
    ),
    path(
        '<str:role>/section/<id_section>', SectionView.as_view(),
        name='section_detail'
    ),
    path(
        '<str:role>/lecture/<id_lecture>', LectureView.as_view(),
        name='lecture_detail'
    ),
    path(
        '<str:role>/add-portfolio/', UploadPortfolioView.as_view(),
        name='add_portfolio'
    ),
    path(
        '<str:role>/add-documents/', AddDocumentsView.as_view(),
        name='add_documents'
    ),

    path(
        '<str:role>/students_works', StudentsWorksView.as_view(),
        name='students_works'
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
