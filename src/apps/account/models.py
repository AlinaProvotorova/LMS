from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models

from apps.shared.models import BaseModel


class UserRole(BaseModel):
    STUDENT = 'student'
    TEACHER = 'teacher'
    MANAGER = 'manager'
    STAGE_CHOICES = [
        (STUDENT, "Студент"),
        (TEACHER, "Учитель"),
        (MANAGER, "Менеджер"),
    ]
    name = models.CharField(max_length=50, choices=STAGE_CHOICES)

    def __str__(self):
        return self.get_name_display()


class User(AbstractUser):
    class Meta:
        verbose_name = "Пользователи"
        verbose_name_plural = "Пользователи"

    def get_user_dir_path(self, filename):
        return 'account/%s/photo/%s' % (self.username, filename)

    first_name = models.CharField('Имя', max_length=150, blank=True)
    reporting = models.CharField('Отчество', max_length=200, blank=True)
    last_name = models.CharField('Фамилия', max_length=150, blank=True)
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField('Дата рождения', blank=True, null=True)
    telephone = models.CharField('Телефон', max_length=15, blank=True)
    photo = models.ImageField(
        'Фото', upload_to=get_user_dir_path, default='avatar.png'
    )
    roles = models.ManyToManyField(UserRole)

    def full_name(self):
        return f'{self.first_name} {self.reporting} {self.last_name}'


class TeacherEducation(BaseModel):
    class Meta:
        verbose_name = "Программа обучения преподавателя"
        verbose_name_plural = "Программы обучения  преподавателя"

    teacher = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='educations_teacher', verbose_name='Учитель'
    )
    education = models.ForeignKey(
        'education.Education', on_delete=models.CASCADE,
        related_name='teachers_education', verbose_name='Программа обучения'
    )

    def clean(self):
        if not self.teacher.roles.filter(name=UserRole.TEACHER).exists():
            raise ValidationError(
                "Нельзя привязать студента к программе обучения."
            )
        super().clean()


class StudentEducation(BaseModel):
    class Meta:
        verbose_name = "Программа обучения студента"
        verbose_name_plural = "Программы обучения студента"

    student = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='educations_student', verbose_name='Студент'
    )
    education = models.ForeignKey(
        'education.Education', on_delete=models.CASCADE,
        related_name='students_education', verbose_name='Программа обучения'
    )
    date = models.DateField()

    def clean(self):
        if not self.student.roles.filter(name=UserRole.STUDENT).exists():
            raise ValidationError(
                "Нельзя привязать учителя к программе обучения."
            )
        super().clean()


class Portfolio(BaseModel):
    """
    Модель портфолио пользователя
    """

    def get_user_dir_path(self, filename):
        return 'account/%s/portfolio/%s' % (self.user.username, filename)

    class Meta:
        verbose_name = "Портфолио"
        verbose_name_plural = "Портфолио"

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, unique=False,
        verbose_name='Пользователь', related_name='portfolio'
    )
    title = models.CharField('Название', max_length=150, blank=False)
    file = models.FileField('Файл', upload_to=get_user_dir_path, null=True)
    date_added = models.DateField('Дата добавления', auto_now_add=True)
    teacher = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="student_portfolio",
        verbose_name='Преподаватель', null=True
    )
    subject = models.ForeignKey(
        'education.Subject', on_delete=models.PROTECT, related_name="subject_portfolio",
        verbose_name='Дисциплина', null=True
    )
    grade = models.ForeignKey(
        'education.Grade', on_delete=models.PROTECT, verbose_name='Оценка', null=True
    )


class DocumentsUser(BaseModel):

    def get_user_dir_path(self, filename):
        return 'account/%s/documents/%s' % (self.user.username, filename)

    class Meta:
        verbose_name = "Документ пользователя"
        verbose_name_plural = "Документы пользователей"

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True, unique=False,
        verbose_name='Пользователь', related_name='documents'
    )
    title = models.CharField('Название', max_length=150, blank=False)
    file = models.FileField('Файл', upload_to=get_user_dir_path, null=True)
    date_added = models.DateField('Дата добавления', auto_now_add=True)

# class UsersEducationsLink(BaseModel):
#     """
#     Модель связи программы обучения и пользователя
#     """
#
#     user = models.ForeignKey(User,
#                              on_delete=models.PROTECT, blank=False, related_name="users_educations")
#     id_course = models.ForeignKey(Educations,
#                                   on_delete=models.PROTECT, blank=False, related_name="custom_educations")
#
#
# class TestsGradesLink(BaseModel):
#     user = models.ForeignKey(User,
#                              on_delete=models.PROTECT, blank=False)
#     id_test = models.ForeignKey(Tests,
#                                 on_delete=models.PROTECT, blank=False)
#     id_grade = models.ForeignKey(Grades,
#                                  on_delete=models.PROTECT, blank=False)
#     date_added = models.DateField(blank=False)
#
#
# class UsersGradesLink(BaseModel):
#     user = models.ForeignKey(User,
#                              on_delete=models.PROTECT, blank=False)
#     id_subject = models.ForeignKey(Subjects,
#                                    on_delete=models.PROTECT, blank=False)
#     id_grade = models.ForeignKey(Grades,
#                                  on_delete=models.PROTECT, blank=False)
#     date_added = models.DateField(blank=False)

# python manage.py shell_plus
