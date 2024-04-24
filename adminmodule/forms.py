import re

from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import transaction
from django import forms
from django.forms import Textarea
import datetime

from accounts.models import Student, Parent, User
from adminmodule.models import HostelDetails, Food, Income, Notification, StaffRegister, Fees, Attendance, Payment, \
    Complaint, Review, BookRoom, Egrant


def phone_number_validator(value):
    if not re.compile(r'^[7-9]\d{9}$').match(value):
        raise ValidationError('This is Not a Valid Phone Number')


class DateInput(forms.DateInput):
    input_type = 'date'


class TimeInput(forms.TimeInput):
    input_type = 'time'


class AddHostelDetailsForm(forms.ModelForm):
    class Meta:
        model = HostelDetails
        fields = (
            'total_rooms', 'occupied','floor_no','available_beds','Vaccant_beds','annual_expenses', 'location', 'contact_no', 'room_facilities', 'image1',
            'image2',
            'image3')
        widgets = {
            'image1': forms.FileInput(attrs={'class': 'form-control'}),
            'image2': forms.FileInput(attrs={'class': 'form-control'}),
            'image3': forms.FileInput(attrs={'class': 'form-control'}),
        }


class UpdateHostelDetailsForm(forms.ModelForm):
    class Meta:
        model = HostelDetails
        fields = (
            'total_rooms', 'occupied','floor_no','available_beds','Vaccant_beds', 'annual_expenses', 'location', 'contact_no', 'room_facilities', 'image1',
            'image2',
            'image3')


class AddFoodDetail(forms.ModelForm):
    class Meta:
        model = Food
        fields = ('breakfast', 'lunch', 'dinner')


class UpdateFoodDetail(forms.ModelForm):
    class Meta:
        model = Food
        fields = ('breakfast', 'lunch', 'dinner')


class AddIncomeDetailForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ('received', 'given', 'total_income')


class AddStaffForm(forms.ModelForm):
    email = forms.CharField(validators=[
        RegexValidator(regex='^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$', message='Please Enter a Valid Email')])
    mobile = forms.CharField(validators=[phone_number_validator])

    class Meta:
        model = StaffRegister
        fields = ('name', 'mobile', 'email', 'address',)


class UpdateStaffForm(forms.ModelForm):
    class Meta:
        model = StaffRegister
        fields = ('name', 'mobile', 'email', 'address',)


class AddFee(forms.ModelForm):
    student = forms.ModelChoiceField(queryset=Student.objects.filter(approval_status=True))
    from_date = forms.DateField(widget=DateInput)
    to_date = forms.DateField(widget=DateInput)
    room_rent = forms.CharField(
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    mess_bill = forms.CharField(
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    class Meta:
        model = Fees
        fields = ('student', 'from_date', 'to_date', 'room_rent', 'mess_bill')

    def clean(self):
        cleaned_data = super().clean()
        from_date = cleaned_data.get("from_date")
        to_date = cleaned_data.get("to_date")

        if (from_date > datetime.date.today()):
            raise forms.ValidationError("Invalid From Date")
        # if to_date <= from_date or to_date > datetime.date.today():
        #     raise forms.ValidationError("Invalid To Date")

        from_day = from_date.strftime("%d")
        from_m = from_date.strftime("%m")
        to_day = to_date.strftime("%d")
        print(from_m, to_day)

        if int(from_day) != 1:
            raise forms.ValidationError('Invalid From Date')
        if int(from_m) == 2:
            if int(to_day) not in [29, 28]:
                raise forms.ValidationError('Invalid To Date')

        else:

            if int(from_m) in [1, 3, 5, 7, 8, 10, 12]:
                if int(to_day) != 31:
                    raise forms.ValidationError('Invalid To Date')

            elif int(from_m) == [4, 6, 9, 11]:

                if int(to_day) != 30:
                    raise forms.ValidationError('Invalid To Date')

        return cleaned_data


attendnace_choice = (
    ('P', 'P'),
    ('A', 'A'),
)


class AddAttendanceForm(forms.ModelForm):
    student = forms.ModelChoiceField(queryset=Student.objects.filter(approval_status=True))
    attendance = forms.ChoiceField(choices=attendnace_choice, widget=forms.RadioSelect)

    class Meta:
        model = Attendance
        fields = ('student', 'attendance')

    # def clean(self):
    #     cleaned_data = super().clean()
    #     from_date = cleaned_data.get("initial_day")
    #     to_date = cleaned_data.get("final_day")
    #
    #     if (from_date > datetime.date.today()):
    #         raise forms.ValidationError("Invalid From Date")
    #     if to_date <= from_date or to_date > datetime.date.today():
    #         raise forms.ValidationError("Invalid To Date")
    #
    #     return cleaned_data


class StudentPaymentForm(forms.ModelForm):
    payment = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    date = forms.DateField(required=True, widget=DateInput())

    class Meta:
        model = Payment
        fields = ('payment', 'date')


class RegisterComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ('subject', 'complaint')


class AddReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('name', 'review',)


class StudentBookRoomForm(forms.ModelForm):
    date_joining = forms.DateField(widget=DateInput)

    class Meta:
        model = BookRoom
        fields = ('date_joining',)

    def clean_date_joining(self):
        date = self.cleaned_data['date_joining']

        if date < datetime.date.today():
            raise forms.ValidationError("Invalid Date")
        return date


class ApplyEgrantForm(forms.ModelForm):
    class Meta:
        model = Egrant
        fields = ('course', 'academic_year', 'cast', 'yearly_income')


class NotificationForm(forms.ModelForm):
    time = forms.TimeField(widget=TimeInput)

    class Meta:
        model = Notification
        fields = '__all__'


MONTH_CHOICES = (
    ('January', 'January'),
    ('February ', 'February '),
    ('March ', 'March '),
    ('April ', 'April '),
    ('May ', 'May '),
    ('June ', 'June '),
    ('July ', 'July '),
    ('August ', 'August '),
    ('September ', 'September '),
    ('October ', 'October '),
    ('November ', 'November '),
    ('December ', 'December '),
)


def current_year():
    return datetime.date.today().year


def year_choices():
    return [(r, r) for r in range(2021, datetime.date.today().year + 10)]


class PayBillForm(forms.ModelForm):
    card_no = forms.CharField(validators=[RegexValidator(regex='^.{16}$', message='Please Enter a Valid Card No')])
    card_cvv = forms.CharField(validators=[RegexValidator(regex='^.{3}$', message='Please Enter a Valid CVV')])
    expiry_month = forms.ChoiceField(choices=MONTH_CHOICES)
    expiry_year = forms.TypedChoiceField(coerce=int, choices=year_choices, initial=current_year)

    class Meta:
        model = Payment
        fields = ('card_no', 'card_cvv', 'expiry_month', 'expiry_year')


class UserUpdate(UserCreationForm):
    username = forms.CharField()
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput, )
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput, )

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')


class StudentUpdate(forms.ModelForm):
    email = forms.CharField(validators=[
        RegexValidator(regex='^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$', message='Please Enter a Valid Email')])
    phone_no = forms.CharField(validators=[phone_number_validator])

    class Meta:
        model = Student
        fields = ('name', 'email', 'phone_no', 'address')
