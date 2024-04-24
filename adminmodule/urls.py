from django.contrib import admin
from django.urls import path

from adminmodule import views, studentviews, parentviews

urlpatterns = [

    path('admin_page/', views.admin_page, name='admin_page'),

    path('add_hostel_detail/', views.add_hostel_detail, name='add_hostel_detail'),
    path('view_hostel_detail/', views.view_hostel_detail, name='view_hostel_detail'),
    path('update_hostel_detail/<int:id>/', views.update_hostel_detail, name='update_hostel_detail'),
    path('delete_hostel_detail/<int:id>/', views.delete_hostel_detail, name='delete_hostel_detail'),

    path('add_food_detail/', views.add_food_detail, name='add_food_detail'),
    path('view_food_detail/', views.view_food_detail, name='view_food_detail'),
    path('update_food_detail/<int:id>/', views.update_food_detail, name='update_food_detail'),
    path('delete_food_detail/<int:id>/', views.delete_food_detail, name='delete_food_detail'),

    path('add_income_detail/', views.add_income_detail, name='add_income_detail'),
    path('view_income_detail/', views.view_income_detail, name='view_income_detail'),
    path('view_complaint/', views.view_complaint, name='view_complaint'),
    path('add_fee/', views.add_fee, name='add_fee'),
    path('view_fee/', views.view_fee, name='view_fee'),
    path('view_payment/', views.view_payment, name='view_payment'),
    path('add_notification/', views.add_notification, name='add_notification'),
    path('view_notification/', views.view_notification, name='view_notification'),
    path('view_attendance/', views.view_attendance, name='view_attendance'),
    path('day_attendance/<date>/', views.day_attendance, name='day_attendance'),
    path('add_attendance/', views.add_attendance, name='add_attendance'),
    path('mark/<int:id>/', views.mark, name='mark'),
    path('add_staff/', views.add_staff, name='add_staff'),
    path('view_staff/', views.view_staff, name='view_staff'),
    path('update_staff/<int:id>/', views.update_staff, name='update_staff'),
    path('delete_staff/<int:id>/', views.delete_staff, name='delete_staff'),
    path('view_egrant_details/', views.view_egrant_details, name='view_egrant_details'),
    path('approve_egrant/<int:id>/', views.approve_egrant, name='approve_egrant'),
    path('reject_egrant/<int:id>/', views.reject_egrant, name='reject_egrant'),
    path('view_registration_details/', views.view_registration_details, name='view_registration_details'),
    path('approve_student/<int:id>/', views.approve_student, name='approve_student'),
    path('reject_student/<int:id>/', views.reject_student, name='reject_student'),
    path('approve_parent/<int:id>/', views.approve_parent, name='approve_parent'),
    path('reject_parent/<int:id>/', views.reject_parent, name='reject_parent'),
    path('bookings/', views.bookings, name='bookings'),
    path('confirm_booking/<int:id>/', views.confirm_booking, name='confirm_booking'),
    path('reject_booking/<int:id>/', views.reject_booking, name='reject_booking'),
    path('reviews/', views.review, name='review'),
    path('ajax/load-bill/', views.load_bill, name='ajax_load_bill'),  # AJAX


    path('student_page/', studentviews.student_page, name='student_page'),
    path('profile/', studentviews.profile, name='profile'),
    path('update_profile/', studentviews.update_profile, name='update_profile'),
    path('view_fee_student/', studentviews.view_fee, name='view_fee_student'),
    path('pay_fee/', studentviews.pay_fee, name='pay_fee'),
    path('view_attendance_student/', studentviews.view_attendance, name='view_attendance_student'),
    path('view_food_student/', studentviews.view_food_updates, name='view_food_student'),
    path('send_complaint/', studentviews.send_complaint, name='send_complaint'),
    path('view_send_compalints/', studentviews.view_send_compalints, name='view_send_compalints'),

    path('notification_view_student/', studentviews.view_notification, name='notification_view_student'),
    path('hostel_student/', studentviews.view_hostel_details, name='hostel_student'),
    path('book_room/', studentviews.book_room, name='book_room'),
    path('booking_status/', studentviews.booking_status, name='booking_status'),
    path('cancel_booking/<int:id>/', studentviews.cancel_booking, name='cancel_booking'),
    path('apply_egrant/', studentviews.apply_egrant, name='apply_egrant'),
    path('egrant_status/', studentviews.egrant_status, name='egrant_status'),
    path('pay_fee/<int:id>/', studentviews.pay_fee, name='pay_fee'),
    path('do_payment/<int:id>/', studentviews.do_payment, name='do_payment'),
    path('payment_details/', studentviews.payment_details, name='payment_details'),
    path('delete_profile_student/', studentviews.delete_profile_student, name='delete_profile_student'),


    path('parent_page/', parentviews.parent_page, name='parent_page'),
    path('hostel_details_parent/', parentviews.hostel_details, name='hostel_details_parent'),
    path('staff_details_parent/', parentviews.staff_details, name='staff_details_parent'),
    path('book_room_parent/', parentviews.book_room_parent, name='book_room_parent'),
    path('booking_status_parent/', parentviews.booking_status_parent, name='booking_status_parent'),
    path('cancel_booking_parent/<int:id>/', parentviews.cancel_booking_parent, name='cancel_booking_parent'),
    path('student_attendance/', parentviews.student_attendance, name='student_attendance'),
    path('student_egrant/', parentviews.student_egrant, name='student_egrant'),
    path('parent_fee_view/', parentviews.parent_fee_view, name='parent_fee_view'),
    path('parent_pay_fee/<int:id>/', parentviews.parent_pay_fee, name='parent_pay_fee'),
    path('payment_details_parent/', parentviews.payment_details_parent, name='payment_details_parent'),
    path('do_payment_parent<int:id>/', parentviews.do_payment_parent, name='do_payment_parent'),
    path('delete_profile/', parentviews.delete_profile, name='delete_profile'),

]
