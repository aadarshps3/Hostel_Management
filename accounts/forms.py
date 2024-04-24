import re

from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import transaction
from django import forms
from accounts.models import User, Student, Parent


class DateInput(forms.DateInput):
    input_type = 'date'


def phone_number_validator(value):
    if not re.compile(r'^[7-9]\d{9}$').match(value):
        raise ValidationError('This is Not a Valid Phone Number')


class UserRegister(UserCreationForm):
    username = forms.CharField()
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput, )
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput, )

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')


class StudentSignUpForm(forms.ModelForm):
    email = forms.CharField(validators=[
        RegexValidator(regex='^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$', message='Please Enter a Valid Email')])
    phone_no = forms.CharField(validators=[phone_number_validator])

    class Meta:
        model = Student
        fields = ('name', 'email', 'phone_no', 'address', 'course', 'photo')
        widget = {
            'photo': forms.FileInput(attrs={'class': 'form-control'}),

        }

    def clean_email(self):
        mail = self.cleaned_data["email"]
        email_qs_t = Parent.objects.filter(email=mail)
        email_qs_s = Student.objects.filter(email=mail)
        if email_qs_t.exists():
            raise forms.ValidationError("This email already registered")
        if email_qs_s.exists():
            raise forms.ValidationError("This email already registered")
        return mail

    def clean_phone_no(self):
        contact_no = self.cleaned_data["phone_no"]
        contact_qs_s = Student.objects.filter(phone_no=contact_no)
        contact_qs_t = Parent.objects.filter(phone_no=contact_no)

        if contact_qs_s.exists():
            raise forms.ValidationError('This Phone Number already registered')
        if contact_qs_t.exists():
            raise forms.ValidationError('This Phone Number already registered')

        return contact_no


class ParentSignUpForm(forms.ModelForm):
    student_name = forms.ModelChoiceField(queryset=Student.objects.all())

    email = forms.CharField(validators=[
        RegexValidator(regex='^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$', message='Please Enter a Valid Email')])

    phone_no = forms.CharField(validators=[phone_number_validator])

    class Meta:
        model = Parent
        fields = ('student_name', 'name', 'email', 'phone_no', 'address')

    def clean_email(self):
        mail = self.cleaned_data["email"]
        email_qs_t = Parent.objects.filter(email=mail)
        email_qs_s = Student.objects.filter(email=mail)
        if email_qs_t.exists():
            raise forms.ValidationError("This email already registered")
        if email_qs_s.exists():
            raise forms.ValidationError("This email already registered")
        return mail

    def clean_phone_no(self):
        contact_no = self.cleaned_data["phone_no"]
        contact_qs_s = Student.objects.filter(phone_no=contact_no)
        contact_qs_t = Parent.objects.filter(phone_no=contact_no)

        if contact_qs_s.exists():
            raise forms.ValidationError('This Phone Number already registered')
        if contact_qs_t.exists():
            raise forms.ValidationError('This Phone Number already registered')
        return contact_no

    def clean_student_name(self):
        student = self.cleaned_data["student_name"]
        student_qs = Parent.objects.filter(student_name=student)

        if student_qs.exists():
            raise forms.ValidationError('Parent Already registered for student {}'.format(student))

        return student
