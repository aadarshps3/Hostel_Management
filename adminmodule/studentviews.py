import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.utils import timezone

from accounts.forms import UserRegister, StudentSignUpForm
from accounts.models import Student
from adminmodule.forms import StudentPaymentForm, RegisterComplaintForm, AddReviewForm, StudentBookRoomForm, \
    ApplyEgrantForm, PayBillForm, UserUpdate, StudentUpdate
from adminmodule.models import Fees, Attendance, Food, Complaint, Notification, HostelDetails, BookRoom, Egrant, Payment

@login_required(login_url='accounts:login_view')
def student_page(request):
    user = Student.objects.get(user=request.user)
    request.session['notification'] = Notification.objects.filter(timestamp=datetime.date.today()).count()
    return render(request, 'student/home.html', {'user': user})

@login_required(login_url='accounts:login_view')
def profile(request):
    student = Student.objects.get(user=request.user)
    return render(request, 'student/profile.html', {'students': student})

@login_required(login_url='accounts:login_view')
def update_profile(request):
    student = Student.objects.get(user=request.user)

    form = StudentUpdate(instance=student)
    if request.method == 'POST':
        form = StudentUpdate(request.POST or None, instance=student or None)

        if form.is_valid():
            form.save()
            messages.info(request, 'Profile Updated  Successfully')
            return redirect('profile')
    return render(request, 'student/update_profile.html', {'form': form, })

@login_required(login_url='accounts:login_view')
def view_hostel_details(request):
    detail = HostelDetails.objects.all()
    return render(request, 'student/view_hostel_details.html', {'details': detail})

@login_required(login_url='accounts:login_view')
def book_room(request):
    form = StudentBookRoomForm()
    if request.method == 'POST':
        form = StudentBookRoomForm(request.POST)
        if form.is_valid():
            book = form.save(commit=False)

            book.student = Student.objects.get(user=request.user)
            book.date_joining = form.cleaned_data.get('date_joining')
            book.booking_date = form.cleaned_data.get('booking_date')
            book.booked_by = request.user
            student_qs = BookRoom.objects.filter(student=Student.objects.get(user=request.user))
            if student_qs.exists():
                messages.info(request, 'You have Already Booked room  ')
            else:
                book.save()
                messages.info(request, 'Successfully Booked Room ')
                return redirect('booking_status')
    return render(request, 'student/book_room.html', {'form': form})

@login_required(login_url='accounts:login_view')
def booking_status(request):
    student = Student.objects.get(user=request.user)
    status = BookRoom.objects.filter(student=student)
    return render(request, 'student/booking_status.html', {'statuss': status})

@login_required(login_url='accounts:login_view')
def cancel_booking(request, id):
    book = BookRoom.objects.filter(pk=id)
    if request.method == 'POST':
        book.delete()
        messages.info(request, 'Your Booking Has Been Cancelled')
        return redirect('booking_status')
    return render(request, 'student/cancel_booking.html')

@login_required(login_url='accounts:login_view')
def view_attendance(request):
    u = Student.objects.get(user=request.user)
    attendance = Attendance.objects.filter(student=u)
    return render(request, 'student/view_attendance.html', {'attendances': attendance})

@login_required(login_url='accounts:login_view')
def apply_egrant(request):
    form = ApplyEgrantForm()
    if request.method == 'POST':
        form = ApplyEgrantForm(request.POST)
        if form.is_valid():
            egrant = form.save(commit=False)
            egrant.name = Student.objects.get(user=request.user)
            egrant.course = form.cleaned_data.get('course')
            egrant.academic_year = form.cleaned_data.get('academic_year')
            egrant.cast = form.cleaned_data.get('cast')
            egrant.yearly_income = form.cleaned_data.get('yearly_income')
            egrant.save()
            messages.info(request, 'Successfully Applied for egrant ')
            return redirect('egrant_status')
    return render(request, 'student/apply_egrant.html', {'form': form})

@login_required(login_url='accounts:login_view')
def egrant_status(request):
    u = Student.objects.get(user=request.user)
    egrant = Egrant.objects.filter(name=u)
    return render(request, 'student/egrant_status.html', {'egrants': egrant})

@login_required(login_url='accounts:login_view')
def view_fee(request):
    u = Student.objects.get(user=request.user)
    fee = Fees.objects.filter(student=u,status=False)
    return render(request, 'student/fees_view_student.html', {'fees': fee})

@login_required(login_url='accounts:login_view')
def pay_fee(request, id):
    u = Student.objects.get(user=request.user)
    fee = Fees.objects.get(id=id)
    total = 0
    egrnt_qs = Egrant.objects.filter(name=u)
    if egrnt_qs.exists():
        if egrnt_qs.last().approval_status == True:
            total = fee.water + fee.electricity + fee.caution_deposit + fee.security + fee.mess + fee.others
            return render(request, 'student/pay_fee.html', {'total': total, 'fee': fee})
        else:
            total = fee.accommodation + fee.water + fee.electricity + fee.caution_deposit + fee.security + fee.mess + fee.others
            return render(request, 'student/pay_fee.html', {'total': total, 'fee': fee})
    else:
        total = fee.accommodation + fee.water + fee.electricity + fee.caution_deposit + fee.security + fee.mess + fee.others
        return render(request, 'student/pay_fee.html', {'total': total, 'fee': fee})

@login_required(login_url='accounts:login_view')
def do_payment(request, id):
    u = Student.objects.get(user=request.user)
    fee = Fees.objects.get(id=id)

    amount = fee.get_total()

    form = PayBillForm()
    if request.method == 'POST':
        form = PayBillForm(request.POST)
        if form.is_valid():
            p = form.save(commit=False)
            p.payment = amount
            p.bill = fee
            p.save()
            fee.status = True
            fee.paid_by = u.name
            fee.payment = amount
            fee.paid_date = datetime.date.today()
            fee.save()
            messages.info(request, 'Fee Paid Successfully')
            return redirect('payment_details')

    return render(request, 'student/do_payment.html', {'form': form})

@login_required(login_url='accounts:login_view')
def payment_details(request):
    u = Student.objects.get(user=request.user)
    payment = Fees.objects.filter(student=u,status=True)
    return render(request, 'student/payment_details.html', {'payments': payment})

@login_required(login_url='accounts:login_view')
def view_food_updates(request):
    food = Food.objects.all()
    return render(request, 'student/view_food_detail.html', {'foods': food})

@login_required(login_url='accounts:login_view')
def send_complaint(request):
    form = RegisterComplaintForm()
    if request.method == 'POST':
        form = RegisterComplaintForm(request.POST)
        if form.is_valid():
            comp = form.save(commit=False)
            comp.name = request.user
            comp.subject = form.cleaned_data.get('subject')
            comp.complaint = form.cleaned_data.get('complaint')
            comp.save()
            messages.info(request, 'Successfully Send Complaint')
            return redirect('view_send_compalints')

    else:
        form = RegisterComplaintForm()
    return render(request, 'student/send_complaint.html', {'form': form})

@login_required(login_url='accounts:login_view')
def view_send_compalints(request):
    user = request.user
    complaint = Complaint.objects.filter(name=user)
    return render(request, 'student/view_send_complaint.html', {'complaints': complaint})

@login_required(login_url='accounts:login_view')
def view_notification(request):
    notification = Notification.objects.all()
    request.session['seen'] = True

    return render(request, "student/view_notification.html", {'notifications': notification, })
@login_required(login_url='accounts:login_view')
def delete_profile_student(request):
    user = request.user
    if request.method == 'POST':
        user.delete()
        messages.info(request,'Your Account Deleted Successfully')
        return redirect('accounts:login_view')
    return render(request, 'student/delete_profile.html')