from django import forms
from django.forms import formset_factory

from .models import Test, Question, Answer


class TestForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = ("title", "description", "time")


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ("answer", "correct_answer")
        widgets = {
            'answer': forms.TextInput(
                attrs={
                    'placeholder': 'Ответ'
                }
            )
        }


AnswerFormSet = formset_factory(AnswerForm, extra=1, )


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ("question",)
        widgets = {
            'question': forms.Textarea(
                attrs={
                    'placeholder': 'Введите текст своего вопроса',
                    'cols': "100", 'rows': "10"
                }
            )
        }


QuestionFormSet = formset_factory(QuestionForm, extra=1, )

# QuestionFormSet = modelformset_factory(
#     Question,
#     fields=('question',),
#     extra=1,
#     widgets={
#         'question': forms.Textarea(
#             attrs={
#                 'placeholder': 'Введите текст своего вопроса',
#                 'cols': "100", 'rows': "10"
#             }
#         )
#     }
# )

# AnswerFormSet = modelformset_factory(
#     Answer,
#     fields=("answer", "correct_answer",),
#     extra=1,
#     widgets={
#         'answer': forms.TextInput(
#             attrs={
#                 'placeholder': 'Ответ'
#             }
#         )
#     }
# )
