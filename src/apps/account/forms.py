from django import forms

from .models import User, Portfolio, DocumentsUser


class StudentsWorksForm(forms.ModelForm):
    """
      Форма для выставления оценок за портфолио студентам
    """

    class Meta:
        model = Portfolio
        fields = ['file', 'grade']

    grade_value = forms.DecimalField(
        required=False,
        min_value=0,
        max_value=100
    )


class PortfolioStudentForm(forms.ModelForm):
    """
    Форма добавления портфолио
    """

    class Meta:
        model = Portfolio
        fields = ('teacher', 'title', 'subject', 'file')
        widgets = {
            'teacher': forms.Select(attrs={'class': 'select-css'}),
            'subject': forms.Select(attrs={'class': 'select-css'}),
        }


class DocumentsForm(forms.ModelForm):
    """
    Форма добавления портфолио
    """

    class Meta:
        model = DocumentsUser
        fields = ('title', 'file')
        labels = {
            'title': 'Название',
            'file': 'Файл'
        }


class UserRegistrationForm(forms.ModelForm):
    """
    Форма регистрации
    """
    password = forms.CharField(
        label='Password', widget=forms.PasswordInput
    )
    password2 = forms.CharField(
        label='Repeat password', widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпадают')
        return cd['password2']
