from django.db import models
import os
from apps.account.models import User
from apps.shared.models import BaseModel
import mammoth
from django.core.files import File
from django.conf import settings
import aspose.words as aw


class Education(BaseModel):
    class Meta:
        verbose_name = "Программа обучения"
        verbose_name_plural = "Программы обучения"

    NOT_ACCESSIBLE = 0
    IN_DEVELOPMENT = 1
    FILLING = 2
    ACCESS = 3
    STATUS_CHOICES = [
        (NOT_ACCESSIBLE, "Недоступен"),
        (IN_DEVELOPMENT, "В разработке"),
        (FILLING, "Заполняется"),
        (ACCESS, "Доступно"),
    ]
    title = models.CharField('Название', max_length=150, blank=False)
    description = models.TextField('Описание', blank=True)
    status = models.IntegerField(
        'Статус', choices=STATUS_CHOICES, default=IN_DEVELOPMENT
    )
    date_added = models.DateField('Дата создания', blank=False)
    date_start = models.DateField('Дата старта', blank=True)
    is_online = models.BooleanField('Онлайн', default=True)
    author = models.ForeignKey(
        'account.User', on_delete=models.PROTECT, null=True,
        related_name='author_educations', verbose_name='Автор курса'
    )

    def get_program_type(self):
        return 'Курс' if self.is_online else 'Программа обучения'

    def __str__(self):
        return f'{self.title}({self.get_program_type()})'


class Subject(models.Model):
    class Meta:
        verbose_name = "Дисциплина"
        verbose_name_plural = "Дисциплины"
        ordering = ['sequence']

    title = models.CharField('Название', max_length=150, blank=False)
    description = models.TextField('Описание', blank=True)
    date_added = models.DateField('Дата добавления', blank=False)
    studying_time = models.DateField('Время изучения', blank=True)
    sequence = models.PositiveSmallIntegerField('Порядок', blank=True)
    education = models.ForeignKey(
        Education, on_delete=models.CASCADE, related_name='education_subjects',
        verbose_name='Программа обучения'
    )
    teachers = models.ManyToManyField(
        'account.User', related_name='teacher_educations', verbose_name='Учителя'
    )

    def __str__(self):
        return f'{self.education.title}-->{self.title}'


class Section(BaseModel):
    class Meta:
        verbose_name = "Раздел"
        verbose_name_plural = "Разделы"

    title = models.CharField('Название', max_length=150, blank=False)
    description = models.TextField('Описание', blank=True)
    date_added = models.DateField('Дата создания', blank=False)
    subject = models.ForeignKey(
        Subject, on_delete=models.PROTECT, blank=False, related_name='sections',
        verbose_name='Дисциплина'
    )

    def __str__(self):
        return f'{self.subject.education.title}-->{self.subject.title}-->{self.title}'


class Lecture(BaseModel):
    class Meta:
        verbose_name = "Лекция"
        verbose_name_plural = "Лекции"

    def get_dir_path(self, filename):
        return 'education/%s/%s/%s/Лекции/%s' % (
            self.section.subject.education.title,
            self.section.subject.title,
            self.section.title,
            filename
        )

    title = models.CharField('Название', max_length=150, blank=False)
    content = models.FileField('Контент', upload_to=get_dir_path, blank=True, null=True, max_length=255)
    date_added = models.DateField('Дата создания', blank=False)
    section = models.ForeignKey(
        Section, on_delete=models.PROTECT, null=True, related_name='lectures',
        verbose_name='Раздел'
    )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.content:
            html_path = self.convert_docx_to_html(self.content.path)
            self.content = html_path
            self.save()
            # with open(html_path, 'rb') as html_file:
            #     new_content = File(html_file)
            #     self.content = new_content
            #     self.save()

    def convert_docx_to_html(self, content):
        # Load the document from the disc.
        doc = aw.Document(content)
        html = doc.save(self.get_dir_path(self.content.name))
        print(html.path)
        # Save the document to HTML format.
        # with open(content, "rb") as docx_file:
        #     result = mammoth.convert_to_html(docx_file)
        # html_abs_path = self.content.path.replace(".docx", ".html")
        # with open(html_abs_path, "a", encoding='UTF-8') as html_file:
        #     html_file.write(result.value)
        return html


class GradingSystem(BaseModel):
    class Meta:
        verbose_name = "Cистема оценивания"
        verbose_name_plural = "Cистема оценивания"

    grade = models.PositiveSmallIntegerField(default=0)
    grade_ABCDEF = models.CharField(max_length=1, primary_key=True)
    grade_in_words = models.CharField(max_length=20)


class Grade(BaseModel):
    class Meta:
        verbose_name = "Оценка"
        verbose_name_plural = "Оценки"

    grading_system = models.ForeignKey(
        GradingSystem, on_delete=models.CASCADE, null=True,
        blank=True, related_name='grades'
    )
    grade_100 = models.PositiveIntegerField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.grade_100 is not None:
            if self.grade_100 < 55:
                grading_system = GradingSystem.objects.get(pk='F')
                self.grading_system = grading_system
            elif self.grade_100 < 65:
                grading_system = GradingSystem.objects.get(pk='E')
                self.grading_system = grading_system
            elif self.grade_100 < 75:
                grading_system = GradingSystem.objects.get(pk='D')
                self.grading_system = grading_system
            elif self.grade_100 < 85:
                grading_system = GradingSystem.objects.get(pk='C')
                self.grading_system = grading_system
            elif self.grade_100 < 95:
                grading_system = GradingSystem.objects.get(pk='В')
                self.grading_system = grading_system
            elif self.grade_100 <= 100:
                grading_system = GradingSystem.objects.get(pk='A')
                self.grading_system = grading_system

            super().save(*args, **kwargs)

    def __str__(self):
        return self.grading_system.grade_in_words


class Test(BaseModel):
    class Meta:
        verbose_name = "Тесты"
        verbose_name_plural = "Тесты"

    title = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=500)
    time = models.IntegerField(help_text="Время для теста в минутах")
    date_added = models.DateField(auto_now=True)
    lecture = models.ForeignKey(
        Lecture, on_delete=models.PROTECT, related_name='tests'
    )
    sequence = models.PositiveSmallIntegerField(blank=True)


class Question(BaseModel):
    class Meta:
        verbose_name = "Вопросы для теста"
        verbose_name_plural = "Вопросы для теста"

    test = models.ForeignKey(Test, on_delete=models.CASCADE, null=True)
    question = models.CharField(max_length=200)


class Answer(BaseModel):
    class Meta:
        verbose_name = "Ответы для теста"
        verbose_name_plural = "Ответы для теста"

    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True)
    answer = models.CharField(max_length=200)
    correct_answer = models.BooleanField(default=False)

    def __str__(self):
        return self.answer


class Schedule(BaseModel):
    class Meta:
        verbose_name = "Расписание"
        verbose_name_plural = "Расписания"

    LECTURE = 'Л'
    LABORATORY = 'ЛП'
    EXAM = 'ЭКЗ'
    WEBINAR = 'В'
    CLASS_CHOICES = [
        (LECTURE, "Лекция"),
        (LABORATORY, "Лабораторный практикум"),
        (EXAM, "Экзамен"),
        (WEBINAR, "Вебинар"),
    ]
    professor = models.ForeignKey(
        User, on_delete=models.PROTECT, blank=True, verbose_name='Преподаватель'
    )
    date = models.DateField('Дата')
    time_lesson = models.DateField('Время')
    where = models.CharField('Место проведения', max_length=10, blank=False)
    subject = models.ForeignKey(
        Subject, on_delete=models.CASCADE, related_name='subject_schedule', null=True,
        verbose_name='Дисциплина'
    )
    class_type = models.CharField('Тип занятия', max_length=3, choices=CLASS_CHOICES)
