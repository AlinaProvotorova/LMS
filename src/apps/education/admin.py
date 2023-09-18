from django.contrib import admin

from .models import (
    Answer, Education, Grade, Lecture, Section, Question, Schedule,
    Subject, Test
)


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ["grading_system_grade", "grading_system_grade_ABCDEF",
                    "grading_system_grade_in_words", "grade_100"]
    ordering = ["grade_100"]
    fields = ['grade_100']

    def grading_system_grade(self, obj):
        return obj.grading_system.grade

    def grading_system_grade_ABCDEF(self, obj):
        return obj.grading_system.grade_ABCDEF

    def grading_system_grade_in_words(self, obj):
        return obj.grading_system.grade_in_words


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 1


class QuestionInline(admin.StackedInline):
    model = Question
    inlines = [AnswerInline]
    extra = 1


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = [
        "id", "title", "description", "time", "date_added", "sequence"
    ]
    list_editable = ["title", "description", "time", "sequence"]
    ordering = ["id"]
    list_per_page = 10
    inlines = [QuestionInline]


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]


class SectionInline(admin.StackedInline):
    model = Section
    extra = 1


class LectureInline(admin.StackedInline):
    model = Lecture
    extra = 1


class SubjectInline(admin.StackedInline):
    model = Subject
    extra = 1
    inlines = [SectionInline]


class EducationAdmin(admin.ModelAdmin):
    list_display = [
        "title", "status", "is_online", "author", "date_added", "date_start", "id"
    ]
    list_editable = ["date_start"]
    ordering = ["id"]
    list_filter = ["author", "is_online", "status"]
    list_per_page = 20
    inlines = [SubjectInline]


class SubjectAdmin(admin.ModelAdmin):
    list_display = [
        "title", "education", "date_added", "studying_time", "sequence", "id",
    ]
    list_editable = ["studying_time", "sequence"]
    ordering = ["sequence"]
    list_per_page = 20
    list_filter = ["education"]
    inlines = [SectionInline]


class SectionAdmin(admin.ModelAdmin):
    list_display = ["title", "subject", "date_added", "id"]
    ordering = ["id"]
    list_filter = ["subject"]
    list_per_page = 20
    inlines = [LectureInline]


class LectureAdmin(admin.ModelAdmin):
    list_display = ["title", "section", "date_added", "id"]
    ordering = ["id"]
    list_filter = ["section"]
    list_per_page = 20


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ["id", "subject", "date", "time_lesson",
                    "where", "professor", "class_type"]
    list_editable = ["subject", "date", "time_lesson",
                     "where", "class_type"]
    ordering = ["id"]
    list_per_page = 10


admin.site.register(Education, EducationAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(Section, SectionAdmin)
admin.site.register(Lecture, LectureAdmin)
