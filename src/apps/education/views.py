from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView

from .forms import AnswerFormSet, QuestionFormSet, TestForm
from .models import Answer, Education, Question, Test


class EducationsListView(ListView):
    """
    Отображение списка курсов или программ обучения пользователя
    """

    model = Education
    is_online = None

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(is_online=self.is_online)
        return queryset


class AllCoursesView(EducationsListView):
    template_name = "course/base_page_all_courses.html"
    is_online = True


class AllEducationView(EducationsListView):
    template_name = "education/base_page_all_educations.html"
    is_online = False


class PageCourse(DetailView):
    model = Education
    template_name = "course/base_one_course.html"


class PageEducation(DetailView):
    model = Education
    template_name = "education/base_one_education.html"


def add_test(request):
    if request.method == 'POST':
        test_form = TestForm(request.POST)
        # question_form = QuestionForm(request.POST)
        question_formset = QuestionFormSet(request.POST)
        answer_formset = AnswerFormSet(request.POST)

        if (
                test_form.is_valid()
                and question_formset.is_valid()
                and answer_formset.is_valid()
        ):
            tests_obj = test_form.save()

            for question_form in question_formset:
                # if question_form.cleaned_data.get('question'):
                instanse_q = question_form.save(commit=False)
                instanse_q.test = tests_obj
                q_obj = question_form.save()

                for answer_form in answer_formset:
                    # if answer_form.cleaned_data.get('answer'):
                    instanse_a = answer_form.save(commit=False)
                    instanse_a.question = q_obj
                    answer_form.save()
            return render(
                request, 'course/add_test_done.html',
                {'test_id': tests_obj.id}
            )
    else:
        test_form = TestForm()
        question_formset = QuestionFormSet()
        answer_formset = AnswerFormSet()

    return render(
        request, 'course/add_test.html',
        {'test_form': test_form, "question_formset": question_formset,
         "answer_formset": answer_formset, 'heading': "Formset Demo", }
    )


def test(request, id_test):
    test = get_object_or_404(Test, pk=id_test)
    data = {"test": test}
    questions = Question.objects.filter(test_id=id_test).all()
    if request.method == 'POST':
        score = 0
        wrong = 0
        correct = 0
        for q in questions:
            if (
                    Answer.objects.filter(
                        question_id=q.id, correct_answer=True
                    ).first().answer == request.POST.get("answ1")
            ):
                score += 10
                correct += 1
            else:
                wrong += 1
        score = round(score / (len(questions) * 10) * 100)
        data = {
            'correct': correct,
            'wrong': wrong,
            'score': score,
        }
        return render(request, 'course/result.html', data)

    questions_dict = {}
    for i, q in enumerate(questions):
        questions_dict[
            f'{str(i + 1)}. {q.question}'
        ] = [
            a.answer for a in Answer.objects.filter(question_id=q.id).all()
        ]
    data["questions"] = questions_dict

    return render(request, 'course/passing-tests.html', {"data": data})
