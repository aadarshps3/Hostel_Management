from django.db import models
from django.utils import timezone
from accounts.models import Parent, Student, User


floor = (
    ('ground floor','ground floor'),
    ('1st floor','1st floor'),
    ('2nd floor','2nd floor'),
    ('3rd floor','3rd floor')
)

class HostelDetails(models.Model):
    total_rooms = models.CharField(max_length=100)
    occupied = models.CharField(max_length=100)
    floor_no = models.CharField(max_length=12,choices=floor)
    available_beds = models.IntegerField()
    Vaccant_beds = models.IntegerField()
    annual_expenses = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    contact_no = models.CharField(max_length=10)
    room_facilities = models.TextField(max_length=200)
    image1 = models.ImageField()
    image2 = models.ImageField()
    image3 = models.ImageField()


class BookRoom(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date_joining = models.DateField()
    booking_date = models.DateField(auto_now_add=True)
    status = models.IntegerField(default=0)
    booked_by = models.ForeignKey(User, on_delete=models.CASCADE)
    seen = models.BooleanField(default=False)


class Food(models.Model):
    breakfast = models.CharField(max_length=100)
    lunch = models.CharField(max_length=100)
    dinner = models.CharField(max_length=100)


class Income(models.Model):
    received = models.CharField(max_length=100)
    given = models.CharField(max_length=100)
    total_income = models.CharField(max_length=100)


class Complaint(models.Model):
    name = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    complaint = models.TextField(max_length=100)
    seen = models.BooleanField(default=False)


class Egrant(models.Model):
    name = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.CharField(max_length=50)
    academic_year = models.CharField(max_length=50)
    cast = models.CharField(max_length=50)
    yearly_income = models.CharField(max_length=100)
    approval_status = models.BooleanField(default=0)
    seen = models.BooleanField(default=False)


class Fees(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    from_date = models.DateField()
    to_date = models.DateField()
    room_rent = models.FloatField(default=0)
    mess_bill = models.FloatField(default=0)
    amount = models.FloatField(default=0)
    status = models.BooleanField(default=False)
    paid_by = models.CharField(max_length=100)
    paid_date = models.DateField(null=True)
    payment = models.CharField(max_length=100)

    def get_total(self):
        return self.room_rent + self.mess_bill

#
# class Fees(models.Model):
#     name = models.ForeignKey(Student, on_delete=models.CASCADE)
#     accommodation = models.IntegerField()
#     water = models.IntegerField()
#     electricity = models.IntegerField()
#     caution_deposit = models.IntegerField()
#     security = models.IntegerField()
#     mess = models.IntegerField()
#     others = models.IntegerField()
#     payment_status = models.BooleanField(default=False)
#     paid_by = models.CharField(max_length=100)
#     paid_date = models.DateField(null=True)
#     payment = models.CharField(max_length=100)
#
#     def get_total_fee(self):
#         return self.accommodation + self.water + self.electricity + self.caution_deposit + self.security + self.mess + self.others
#
#     def __unicode__(self):
#         return self.get_total_fee


class Payment(models.Model):
    bill = models.ForeignKey(Fees, on_delete=models.CASCADE, related_name='fee_payment')
    payment = models.CharField(max_length=100)
    card_no = models.CharField(max_length=30)
    card_cvv = models.CharField(max_length=30)
    expiry_month = models.CharField(max_length=20)
    expiry_year = models.CharField(max_length=20)




class Notification(models.Model):
    to = models.CharField(max_length=100)
    notification = models.TextField(max_length=100)
    time = models.TimeField()
    timestamp = models.DateField(auto_now_add=True, null=True)


class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendance')
    date = models.DateField()
    attendance = models.CharField(max_length=100)
    time = models.TimeField()


class StaffRegister(models.Model):
    name = models.CharField(max_length=50)
    mobile = models.CharField(max_length=10)
    email = models.EmailField()
    address = models.CharField(max_length=50)


class Review(models.Model):
    name = models.CharField(max_length=200)
    review = models.TextField(max_length=200)
    seen = models.BooleanField(default=False)
