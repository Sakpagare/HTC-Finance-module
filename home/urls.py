from django.urls import path, re_path
from apps.home import views

urlpatterns = [

    # The home page
    path('', views.index, name='home'),
    path('profile', views.profile, name="profile"),
    path('quotation/<str:quotation_number>', views.quotation, name="quotation"),
    path('proforma/<str:PI_number>/<str:quotation_number>/', views.proforma, name="proforma"),
    path('quotation_table', views.quotation_table, name="quotation_table"),
    path('proforma_table', views.proforma_table, name="proforma_table"),
    path('tax_table', views.tax_table, name="tax_table"),
    path('quotation_print/<str:qno>', views.quotation_print, name="quotation_print"),
    path('proforma_print/<str:PI_number>', views.proforma_print, name="proforma_print"),
    path('employee_reg', views.employee_reg, name="employee_reg"),
    path('attendance', views.attendance, name="attendance"),
    path('mark-attendance/', views.mark_attendance, name='mark_attendance'),
    path('mark-attendance/', views.mark_attendance, name='mark_attendance'),
    path('salary', views.salary, name='salary'),
    path('inventory', views.inventory, name='inventory'),
    path('download_details', views.download_details, name='download_details'),
    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

]
