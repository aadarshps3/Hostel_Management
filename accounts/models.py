from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    is_student = models.BooleanField(default=False)
    is_parent = models.BooleanField(default=False)


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,primary_key=True,related_name='student')
    role = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    address = models.TextField(max_length=100)
    email = models.EmailField()
    phone_no = models.CharField(max_length=10, null=True)
    course = models.CharField(max_length=200)
    approval_status = models.BooleanField(default=0)
    photo = models.ImageField(upload_to='profile',null=True)
    seen = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Parent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,primary_key=True,related_name='parent')
    name = models.CharField(max_length=50)
    role = models.CharField(max_length=50)
    student_name = models.ForeignKey(Student, on_delete=models.CASCADE)
    address = models.TextField(max_length=100)
    email = models.EmailField()
    phone_no = models.CharField(max_length=10, null=True)
    approval_status = models.BooleanField(default=0)
    seen = models.BooleanField(default=False)

    def __str__(self):
        return self.name
