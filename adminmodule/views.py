import datetime

from django.contrib import auth, messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from accounts.models import Student, Parent
from adminmodule.forms import AddHostelDetailsForm, UpdateHostelDetailsForm, AddFoodDetail, \
    AddIncomeDetailForm, AddStaffForm, UpdateStaffForm, UpdateFoodDetail, \
    NotificationForm, AddAttendanceForm, AddFee
from adminmodule.models import HostelDetails, Food, Income, Complaint, Payment, Notification, Attendance, StaffRegister, \
    Fees, BookRoom, Egrant, Review


@login_required(login_url='accounts:login_view')
def admin_page(request):
    request.session['complaint'] = Complaint.objects.filter(seen=False).count()
    request.session['booking'] = BookRoom.objects.filter(seen=False).count()
    request.session['review'] = Review.objects.filter(seen=False).count()

    request.session['student'] = Student.objects.filter(approval_status=0).count()
    request.session['parent'] = Parent.objects.filter(approval_status=0).count()
    return render(request, 'adminpages/home.html')


@login_required(login_url='accounts:login_view')
def add_hostel_detail(request):
    form = AddHostelDetailsForm()
    if request.method == 'POST':
        form = AddHostelDetailsForm(request.POST, request.FILES)
        if form.is_valid():
            hostel = form.save(commit=False)
            hostel.total_rooms = form.cleaned_data.get('total_rooms')
            hostel.occupied = form.cleaned_data.get('occupied')
            hostel.floor_no = form.cleaned_data.get('floor_no')
            hostel.available_beds = form.cleaned_data.get('available_beds')
            hostel.Vaccant_beds = form.cleaned_data.get('Vaccant_beds')
            hostel.annual_expenses = form.cleaned_data.get('annual_expenses')
            hostel.location = form.cleaned_data.get('location')
            hostel.contact_no = form.cleaned_data.get('contact_no')
            hostel.room_facilities = form.cleaned_data.get('room_facilities')
            hostel.image1 = request.FILES['image1']
            hostel.image2 = request.FILES['image2']
            hostel.image3 = request.FILES['image3']
            fs = FileSystemStorage()
            hostel.save()
            messages.info(request, 'Hostel Details Added')
            return redirect('view_hostel_detail')
    return render(request, 'adminpages/add_hostel_details.html', {'form': form})


@login_required(login_url='accounts:login_view')
def view_hostel_detail(request):
    detail = HostelDetails.objects.all()
    return render(request, 'adminpages/view_hostel_detail.html', {'details': detail})


@login_required(login_url='accounts:login_view')
def update_hostel_detail(request, id):
    detail = HostelDetails.objects.get(id=id)
    form = UpdateHostelDetailsForm(request.POST or None, instance=detail)
    if form.is_valid():
        form.save()
        messages.info(request, 'Hostel Details Updated Successfully')
        return redirect('view_hostel_detail')
    return render(request, 'adminpages/update_hostel_details.html', {'form': form})


@login_required(login_url='accounts:login_view')
def delete_hostel_detail(request, id):
    detail = HostelDetails.objects.get(id=id)
    if request.method == 'POST':
        detail.delete()
        messages.info(request, 'Hostel Details Deleted Successfully')
        return redirect('view_hostel_detail')
    return render(request, 'adminpages/delete_hostel_detail.html')


@login_required(login_url='accounts:login_view')
def add_food_detail(request):
    form = AddFoodDetail()
    if request.method == 'POST':
        form = AddFoodDetail(request.POST)
        if form.is_valid():
            form.save()
            messages.info(request, 'Food Details Added Successfully')
            return redirect('view_food_detail')
    return render(request, 'adminpages/add_food_details.html', {'form': form})


@login_required(login_url='accounts:login_view')
def view_food_detail(request):
    food = Food.objects.all()
    return render(request, 'adminpages/view_food_detail.html', {'foods': food})


@login_required(login_url='accounts:login_view')
def update_food_detail(request, id):
    detail = Food.objects.get(id=id)
    form = UpdateFoodDetail(request.POST or None, instance=detail)
    if form.is_valid():
        form.save()
        messages.info(request, 'Food Details Updated Successfully')
        return redirect('view_food_detail')
    return render(request, 'adminpages/update_food_details.html', {'form': form})


@login_required(login_url='accounts:login_view')
def delete_food_detail(request, id):
    detail = Food.objects.get(id=id)
    if request.method == 'POST':
        detail.delete()
        messages.info(request, 'Food Details Deleted Successfully')
        return redirect('view_food_detail')
    return render(request, 'adminpages/delete_food_detail.html')


@login_required(login_url='accounts:login_view')
def add_income_detail(request):
    form = AddIncomeDetailForm()
    if request.method == 'POST':
        form = AddIncomeDetailForm(request.POST)
        if form.is_valid():
            form.save()
            messages.info(request, 'Income Details Updated Successfully')
            return redirect('view_income_detail')
    return render(request, 'adminpages/add_income_details.html', {'form': form})


@login_required(login_url='accounts:login_view')
def view_income_detail(request):
    income = Income.objects.all()
    return render(request, 'adminpages/view_income_detail.html', {'incomes': income})


@login_required(login_url='accounts:login_view')
def view_complaint(request):
    complaint = Complaint.objects.all()
    for i in complaint:
        i.seen = True
        i.save()
    request.session['complaint'] = 0
    return render(request, 'adminpages/view_complaint.html', {'complaints': complaint})


@login_required(login_url='accounts:login_view')
def add_fee(request):
    form = AddFee()
    if request.method == 'POST':
        form = AddFee(request.POST)
        if form.is_valid():
            bill = form.save(commit=False)
            bill_qs = Fees.objects.filter(student=bill.student, from_date=bill.from_date, to_date=bill.to_date)
            if bill_qs.exists():
                messages.info(request, 'Bill Already added for the Student in this duration')
            else:
                bill.save()
                messages.info(request, 'Bill Added')
                return redirect('add_fee')

    return render(request, 'adminpages/add_fee.html', {'form': form})


@login_required(login_url='accounts:login_view')
def load_bill(request):
    student_id = request.GET.get('studentId')
    from_date = request.GET.get('from_date')
    to_date = request.GET.get('to_date')

    student = Student.objects.get(user_id=student_id)
    present_days = Attendance.objects.filter(student=student, date__range=[from_date, to_date]).count()
    amount = present_days * 200
    rent = 2000
    data = {
        'present_days': present_days,
        'mess_bill': amount,
        'room_rent': rent

    }

    return JsonResponse(data)


@login_required(login_url='accounts:login_view')
def view_fee(request):
    fee = Fees.objects.all()
    return render(request, 'adminpages/view_fee.html', {'fees': fee})


@login_required(login_url='accounts:login_view')
def view_payment(request):
    payment = Fees.objects.filter(status=1)
    return render(request, 'adminpages/view_payment.html', {'payments': payment})


@login_required(login_url='accounts:login_view')
def add_notification(request):
    form = NotificationForm()
    if request.method == 'POST':
        form = NotificationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.info(request, 'Notification Added Successfully')
            return redirect('view_notification')
    return render(request, 'adminpages/add_notification.html', {'form': form})


@login_required(login_url='accounts:login_view')
def view_notification(request):
    notification = Notification.objects.all()
    return render(request, 'adminpages/view_notification.html', {'notifications': notification})


#
# def add_attendance(request):
#     form = AddAttendanceForm()
#     if request.method == 'POST':
#         form = AddAttendanceForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.info(request, 'Attendance Added Successfully')
#             return redirect('view_attendance')
#
#
#     return render(request, 'adminpages/mark_attendance.html', {'form': form})

#
# def view_attendance(request):
#     attendance = Attendance.objects.all()
#     return render(request, 'adminpages/view_attendance.html', {'attendances': attendance})

@login_required(login_url='accounts:login_view')
def add_attendance(request):
    student = Student.objects.filter(approval_status=True)
    return render(request, 'adminpages/student_list.html', {'students': student})


now = datetime.datetime.now()


@login_required(login_url='accounts:login_view')
def mark(request, id):
    user = Student.objects.get(user_id=id)
    att = Attendance.objects.filter(student=user, date=datetime.date.today())
    if att.exists():
        messages.info(request, "Today's Attendance Already marked for this Student ")
        return redirect('add_attendance')
    else:
        if request.method == 'POST':
            attndc = request.POST.get('attendance')
            Attendance(student=user, date=datetime.date.today(), attendance=attndc, time=now.time()).save()
            messages.info(request, "Attendance Added successfully ")
            return redirect('add_attendance')
    return render(request, 'adminpages/mark_attendance.html')


@login_required(login_url='accounts:login_view')
def view_attendance(request):
    value_list = Attendance.objects.values_list('date', flat=True).distinct()
    attendance = {}
    for value in value_list:
        attendance[value] = Attendance.objects.filter(date=value)
    return render(request, 'adminpages/view_attendance.html', {'attendances': attendance})


@login_required(login_url='accounts:login_view')
def day_attendance(request, date):
    attendance = Attendance.objects.filter(date=date)
    context = {
        'attendances': attendance,
        'date': date
    }
    return render(request, 'adminpages/day_attendance.html', context)


@login_required(login_url='accounts:login_view')
def add_staff(request):
    form = AddStaffForm()
    if request.method == 'POST':
        form = AddStaffForm(request.POST)
        if form.is_valid():
            form.save()
            messages.info(request, 'Staff Added Successfully')
            return redirect('view_staff')

    return render(request, 'adminpages/add_staff.html', {'form': form})


@login_required(login_url='accounts:login_view')
def view_staff(request):
    staff = StaffRegister.objects.all()
    return render(request, 'adminpages/view_staff.html', {'staffs': staff})


@login_required(login_url='accounts:login_view')
def update_staff(request, id):
    staff = StaffRegister.objects.get(id=id)

    form = UpdateStaffForm(request.POST or None, instance=staff)
    if form.is_valid():
        form.save()
        messages.info(request, 'Staff Updated Successfully')
        return redirect('view_staff')
    return render(request, 'adminpages/update_staff.html', {'form': form})


@login_required(login_url='accounts:login_view')
def delete_staff(request, id):
    staff = StaffRegister.objects.get(id=id)
    if request.method == 'POST':
        staff.delete()
        messages.info(request, 'Staff Deleted Successfully')
        return redirect('view_staff')
    return render(request, 'adminpages/delete_staff.html')


@login_required(login_url='accounts:login_view')
def view_registration_details(request):
    student = Student.objects.all()
    parent = Parent.objects.all()
    context = {
        'students': student,
        'parents': parent
    }
    return render(request, 'adminpages/view_registration_details.html', context)


@login_required(login_url='accounts:login_view')
def approve_student(request, id):
    student = Student.objects.get(user_id=id)
    student.approval_status = True
    student.save()
    messages.info(request, 'Student Approved  Successfully')
    return HttpResponseRedirect(reverse('view_registration_details'))


@login_required(login_url='accounts:login_view')
def reject_student(request, id):
    student = Student.objects.get(user_id=id)
    if request.method == 'POST':
        student.approval_status = False
        student.save()
        messages.info(request, 'Rejected Student Registration')
        return redirect('view_registration_details')
    return render(request, 'adminpages/reject_student.html')


@login_required(login_url='accounts:login_view')
def approve_parent(request, id):
    parent = Parent.objects.get(user_id=id)
    parent.approval_status = True
    parent.save()
    messages.info(request, 'Parent Approved  Successfully')
    return HttpResponseRedirect(reverse('view_registration_details'))


@login_required(login_url='accounts:login_view')
def reject_parent(request, id):
    parent = Parent.objects.get(user_id=id)
    if request.method == 'POST':
        parent.approval_status = False
        parent.save()
        messages.info(request, 'Rejected Parent Registration')
        return redirect('view_registration_details')
    return render(request, 'adminpages/reject_parent.html')


@login_required(login_url='accounts:login_view')
def bookings(request):
    book = BookRoom.objects.all()
    for i in book:
        i.seen = True
        i.save()
    request.session['booking'] = 0
    return render(request, 'adminpages/bookings.html', {'books': book})


@login_required(login_url='accounts:login_view')
def confirm_booking(request, id):
    details_qs = HostelDetails.objects.all()
    if details_qs.exists():

        book = BookRoom.objects.get(id=id)
        book.status = 1
        book.save()

        hstl = HostelDetails.objects.all().last()
        occupied = hstl.occupied
        Vaccant_beds = hstl.Vaccant_beds
        hstl.occupied = int(occupied) - 1
        hstl.Vaccant_beds = int(Vaccant_beds) - 1
        hstl.save()
        messages.info(request, 'Room Booking Confirmed')
        return redirect('bookings')
    else:
        messages.info(request, 'Please Update Hostel Details')
        return HttpResponseRedirect(reverse('bookings'))


@login_required(login_url='accounts:login_view')
def reject_booking(request, id):
    book = BookRoom.objects.get(id=id)
    if request.method == 'POST':
        book.status = 2
        book.save()
        messages.info(request, 'Room Booking rejected')
        return redirect('bookings')
    return render(request, 'adminpages/reject_booking.html')


@login_required(login_url='accounts:login_view')
def view_egrant_details(request):
    egrant = Egrant.objects.all()

    return render(request, 'adminpages/view_egrant_applications.html', {'egrants': egrant})


@login_required(login_url='accounts:login_view')
def approve_egrant(request, id):
    egrant = Egrant.objects.get(id=id)
    egrant.approval_status = True
    egrant.save()
    messages.info(request, 'E grant Approved')
    return HttpResponseRedirect(reverse('view_egrant_details'))


@login_required(login_url='accounts:login_view')
def reject_egrant(request, id):
    egrant = Egrant.objects.get(id=id)
    if request.method == 'POST':
        egrant.status = False
        egrant.save()
        messages.info(request, 'E grant Rejected')
        return redirect('view_egrant_details')
    return render(request, 'adminpages/reject_booking.html')


@login_required(login_url='accounts:login_view')
def review(request):
    review = Review.objects.all()
    for i in review:
        i.seen = True
        i.save()
    request.session['review'] = 0
    return render(request, 'adminpages/reviews.html', {'reviews': review})
