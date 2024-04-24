import datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.shortcuts import render, redirect
from accounts.models import Parent, Student
from adminmodule.forms import StudentBookRoomForm, StudentPaymentForm, PayBillForm
from adminmodule.models import Fees, Attendance, Food, Complaint, Notification, HostelDetails, StaffRegister, BookRoom, \
    Egrant, Payment

@login_required(login_url='accounts:login_view')
def parent_page(request):
    return render(request, 'parent/home.html')

@login_required(login_url='accounts:login_view')
def hostel_details(request):
    detail = HostelDetails.objects.all()
    return render(request, 'parent/view_hostel_details.html', {'details': detail})

@login_required(login_url='accounts:login_view')
def staff_details(request):
    staff = StaffRegister.objects.all()
    return render(request, 'parent/staff_detail.html', {'staffs': staff})

@login_required(login_url='accounts:login_view')
def book_room_parent(request):
    parent = Parent.objects.get(user=request.user)
    form = StudentBookRoomForm()
    if request.method == 'POST':
        form = StudentBookRoomForm(request.POST)
        if form.is_valid():
            if form.is_valid():
                book = form.save(commit=False)

                book.student = parent.student_name
                book.date_joining = form.cleaned_data.get('date_joining')
                book.booking_date = form.cleaned_data.get('booking_date')
                book.booked_by = request.user
                student_qs = BookRoom.objects.filter(student=parent.student_name)
                if student_qs.exists():
                    messages.info(request, 'You have Already Booked room  ')
                else:
                    book.save()
                    messages.info(request, 'Successfully Booked Room ')
                    return redirect('booking_status_parent')
    return render(request, 'parent/book_room.html', {'form': form})

@login_required(login_url='accounts:login_view')
def booking_status_parent(request):
    parent = Parent.objects.get(user=request.user)
    status = BookRoom.objects.filter(student=parent.student_name)
    return render(request, 'parent/booking_status.html', {'statuss': status})

@login_required(login_url='accounts:login_view')
def cancel_booking_parent(request, id):
    book = BookRoom.objects.filter(pk=id)
    if request.method == 'POST':
        book.delete()
        messages.info(request, 'Your Booking Has Been Cancelled')
        return redirect('booking_status_parent')
    return render(request, 'parent/cancel_booking.html')

@login_required(login_url='accounts:login_view')
def student_attendance(request):
    u = Parent.objects.get(user=request.user)
    attendance = Attendance.objects.filter(student=u.student_name)
    return render(request, 'parent/student_attendance.html', {'attendances': attendance})

@login_required(login_url='accounts:login_view')
def student_egrant(request):
    u = Parent.objects.get(user=request.user)
    egrant = Egrant.objects.filter(name=u.student_name)
    return render(request, 'parent/egrant_status.html', {'egrants': egrant})

@login_required(login_url='accounts:login_view')
def parent_fee_view(request):
    u = Parent.objects.get(user=request.user)
    fee = Fees.objects.filter(student=u.student_name, status=False)
    return render(request, 'parent/fees_view_parent.html', {'fees': fee})

@login_required(login_url='accounts:login_view')
def parent_pay_fee(request, id):
    parent = Parent.objects.get(user=request.user)
    fee = Fees.objects.get(id=id)
    egrnt_qs = Egrant.objects.filter(name=parent.student_name)
    total = 0

    if egrnt_qs.exists():
        if egrnt_qs.last().approval_status == True:
            total = fee.water + fee.electricity + fee.caution_deposit + fee.security + fee.mess + fee.others
            return render(request, 'parent/pay_fee.html', {'total': total, 'fee': fee})
        else:
            total = fee.accommodation + fee.water + fee.electricity + fee.caution_deposit + fee.security + fee.mess + fee.others
            return render(request, 'parent/pay_fee.html', {'total': total, 'fee': fee})
    else:
        total = fee.accommodation + fee.water + fee.electricity + fee.caution_deposit + fee.security + fee.mess + fee.others
        return render(request, 'parent/pay_fee.html', {'total': total, 'fee': fee})

@login_required(login_url='accounts:login_view')
def do_payment_parent(request, id):
    parent = Parent.objects.get(user=request.user)
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
            fee.paid_by = parent.name
            fee.payment = amount
            fee.paid_date = datetime.date.today()
            fee.save()
            messages.info(request, 'Fee Paid Successfully')
            return redirect('payment_details_parent')

    return render(request, 'parent/do_payment.html', {'form': form})

@login_required(login_url='accounts:login_view')
def payment_details_parent(request):
    u = Parent.objects.get(user=request.user)
    payment = Fees.objects.filter(student=u.student_name)
    return render(request, 'parent/payment_details.html', {'payments': payment})

@login_required(login_url='accounts:login_view')
def delete_profile(request):
    user = request.user
    if request.method == 'POST':
        user.delete()
        messages.info(request,'Your Account Deleted Successfully')
        return redirect('accounts:login_view')
    return render(request, 'parent/delete_profile.html')