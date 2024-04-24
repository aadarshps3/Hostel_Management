from django.contrib import admin

# Register your models here.
from adminmodule import models


admin.site.register(models.Food)
admin.site.register(models.Income)
admin.site.register(models.Complaint)
admin.site.register(models.Notification)
admin.site.register(models.StaffRegister)
admin.site.register(models.HostelDetails)
admin.site.register(models.Payment)
admin.site.register(models.Attendance)
admin.site.register(models.Fees)
admin.site.register(models.Review)
admin.site.register(models.BookRoom)
admin.site.register(models.Egrant)