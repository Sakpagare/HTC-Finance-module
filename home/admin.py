from django.contrib import admin
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
# Register your models here.

class CompanyProfileInline(admin.StackedInline):
    model = company_profile
    can_delete = False
    verbose_name_plural = 'company_profiles'


class BankDetailsInline(admin.StackedInline):
    model = bank_details
    can_delete = False
    verbose_name_plural = 'bank_details'

class ProfilePictureInline(admin.StackedInline):
    model = profile_picture
    can_delete = False
    verbose_name_plural = 'profile_picture'


class CustomizedUserAdmin(UserAdmin):
    inlines = (CompanyProfileInline, BankDetailsInline,ProfilePictureInline)


admin.site.unregister(User)
admin.site.register(User, CustomizedUserAdmin)

admin.site.register(company_profile)
admin.site.register(bank_details)
admin.site.register(profile_picture)
admin.site.register(quotation_data)
admin.site.register(order_acceptance)
admin.site.register(proforma_invoce)
admin.site.register(tax_invoce)
admin.site.register(AttendanceRecord)