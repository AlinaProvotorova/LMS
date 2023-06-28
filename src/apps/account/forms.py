from django import forms

from .models import User, Portfolio, DocumentsUser


class UserEditForm(forms.ModelForm):
    """
    Форма редактирования профиля
    """

    class Meta:
        model = User
        fields = (
            'first_name', 'reporting', 'last_name', 'email',
            'date_of_birth', 'photo', 'telephone'
        )
        labels = {
            'first_name': 'Имя',
            'reporting': 'Отчество',
            'last_name': 'Фамилия',
            'email': 'Электронная почта',
            'date_of_birth': 'Дата рождения',
            'photo': 'Фото',
            'telephone': 'Телефон',
        }


class PortfolioForm(forms.ModelForm):
    """
    Форма добавления портфолио
    """

    class Meta:
        model = Portfolio
        fields = ('title', 'file')


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
