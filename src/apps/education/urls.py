from django.urls import path

from .views import AllEducationView, PageEducation, AllCoursesView, PageCourse, test, add_test

urlpatterns = [
    path('', AllEducationView.as_view(), name='educations'),
    path('<pk>', PageEducation.as_view(), name='page_education'),
    path('courses/', AllCoursesView.as_view(), name='courses'),
    path('courses/<pk>', PageCourse.as_view(), name='page_course'),
    path('test/<id_test>', test, name='tests'),
    path('test/add/', add_test, name='add_test'),
    path('test/all/done', add_test, name='add_test_done'),
]
