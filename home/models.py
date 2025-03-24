from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class company_profile(models.Model):
    company = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    contact_no_1 = models.CharField(max_length= 50)
    contact_no_2 = models.CharField(max_length= 50)
    reg_address = models.CharField(max_length= 500)
    city = models.CharField(max_length= 50)
    pincode = models.CharField(max_length= 50)
    pan_no = models.CharField(max_length= 50)
    gst_no = models.CharField(max_length= 50)
    iec_code = models.CharField(max_length= 50)
    
    def __str__(self):
        return str(self.company)
    
class bank_details(models.Model):
    company = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    bank_name = models.CharField(max_length=150)
    branch_name = models.CharField(max_length= 50)
    bank_acc_no  = models.CharField(max_length= 50)
    re_enter_account_no  = models.CharField(max_length= 50)
    ifsc_code  = models.CharField(max_length= 50)
    swift_code  = models.CharField(max_length= 50)
    ad_code   = models.CharField(max_length= 50)
    
    def __str__(self):
        return str(self.company)
    
class profile_picture(models.Model):
    name = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='logo/')
    
    def __str__(self):
        return str(self.name)

class quotation_data(models.Model):
    # name = models.CharField(max_length=150)
    qno = models.CharField(max_length=150)
    q_date = models.CharField(max_length=150)
    customer_name = models.CharField(max_length=150)
    customer_address = models.CharField(max_length=150)
    customer_contact = models.CharField(max_length=150)
    customer_gst = models.CharField(max_length=150)
    customer_reference = models.CharField(max_length=150)
    sr_no = models.CharField(max_length=150)
    item_details = models.TextField()
    grade = models.CharField(max_length=150)
    uom = models.CharField(max_length=150)
    moq = models.CharField(max_length=150)
    rate = models.CharField(max_length=150)
    amount = models.CharField(max_length=150)
    remark = models.CharField(max_length=150)
    totalAmount = models.CharField(max_length=150)
    packingForwarding = models.CharField(max_length=150)
    cgst = models.CharField(max_length=150)
    cgst_total = models.CharField(max_length=150)
    sgst = models.CharField(max_length=150)
    sgst_total = models.CharField(max_length=150)
    igst = models.CharField(max_length=150)
    igst_total = models.CharField(max_length=150)
    grand_total = models.CharField(max_length=150)
    amt_in_words = models.CharField(max_length=150)
    payment_tc = models.CharField(max_length=150)
    delivery_time_tc = models.CharField(max_length=150)
    pf_tc = models.CharField(max_length=150)
    for_tc = models.CharField(max_length=150)
    q_validity_tc = models.CharField(max_length=150)
    moq_tc = models.CharField(max_length=150)
    material_tc = models.CharField(max_length=150)
    other_tc = models.CharField(max_length=150)

    def __str__(self):
        return self.qno
    
    
class order_acceptance(models.Model):
    # name = models.CharField(max_length=150)
    qno = models.CharField(max_length=150)
    q_date = models.CharField(max_length=150)
    customer_name = models.CharField(max_length=150)
    customer_address = models.CharField(max_length=150)
    customer_contact = models.CharField(max_length=150)
    customer_gst = models.CharField(max_length=150)
    customer_reference = models.CharField(max_length=150)
    sr_no = models.CharField(max_length=150)
    item_details = models.TextField()
    grade = models.CharField(max_length=150)
    uom = models.CharField(max_length=150)
    moq = models.CharField(max_length=150)
    rate = models.CharField(max_length=150)
    amount = models.CharField(max_length=150)
    remark = models.CharField(max_length=150)
    totalAmount = models.CharField(max_length=150)
    packingForwarding = models.CharField(max_length=150)
    cgst = models.CharField(max_length=150)
    cgst_total = models.CharField(max_length=150)
    sgst = models.CharField(max_length=150)
    sgst_total = models.CharField(max_length=150)
    igst = models.CharField(max_length=150)
    igst_total = models.CharField(max_length=150)
    grand_total = models.CharField(max_length=150)
    amt_in_words = models.CharField(max_length=150)
    payment_tc = models.CharField(max_length=150)
    delivery_time_tc = models.CharField(max_length=150)
    pf_tc = models.CharField(max_length=150)
    for_tc = models.CharField(max_length=150)
    q_validity_tc = models.CharField(max_length=150)
    moq_tc = models.CharField(max_length=150)
    material_tc = models.CharField(max_length=150)
    other_tc = models.CharField(max_length=150)

    def __str__(self):
        return self.qno
    

class proforma_invoce(models.Model):
    # name = models.CharField(max_length=150)
    PI_number = models.CharField(max_length=150)
    invoice_date = models.CharField(max_length=150)
    PO_number = models.CharField(max_length=150)
    po_date = models.CharField(max_length=150)
    customer_name = models.CharField(max_length=150)
    customer_address = models.CharField(max_length=150)
    customer_contact = models.CharField(max_length=150)
    customer_gst = models.CharField(max_length=150)
    customer_reference = models.CharField(max_length=150)
    sr_no = models.CharField(max_length=150)
    item_details = models.TextField()
    grade = models.CharField(max_length=150)
    uom = models.CharField(max_length=150)
    moq = models.CharField(max_length=150)
    rate = models.CharField(max_length=150)
    amount = models.CharField(max_length=150)
    remark = models.CharField(max_length=150)
    totalAmount = models.CharField(max_length=150)
    packingForwarding = models.CharField(max_length=150)
    cgst = models.CharField(max_length=150)
    cgst_total = models.CharField(max_length=150)
    sgst = models.CharField(max_length=150)
    sgst_total = models.CharField(max_length=150)
    igst = models.CharField(max_length=150)
    igst_total = models.CharField(max_length=150)
    grand_total = models.CharField(max_length=150)
    amt_in_words = models.CharField(max_length=150)

    def __str__(self):
        return self.PI_number
    
class tax_invoce(models.Model):
    # name = models.CharField(max_length=150)
    PI_number = models.CharField(max_length=150)
    invoice_date = models.CharField(max_length=150)
    PO_number = models.CharField(max_length=150)
    po_date = models.CharField(max_length=150)
    customer_name = models.CharField(max_length=150)
    customer_address = models.CharField(max_length=150)
    customer_contact = models.CharField(max_length=150)
    customer_gst = models.CharField(max_length=150)
    customer_reference = models.CharField(max_length=150)
    sr_no = models.CharField(max_length=150)
    item_details = models.TextField()
    grade = models.CharField(max_length=150)
    uom = models.CharField(max_length=150)
    moq = models.CharField(max_length=150)
    rate = models.CharField(max_length=150)
    amount = models.CharField(max_length=150)
    remark = models.CharField(max_length=150)
    totalAmount = models.CharField(max_length=150)
    packingForwarding = models.CharField(max_length=150)
    cgst = models.CharField(max_length=150)
    cgst_total = models.CharField(max_length=150)
    sgst = models.CharField(max_length=150)
    sgst_total = models.CharField(max_length=150)
    igst = models.CharField(max_length=150)
    igst_total = models.CharField(max_length=150)
    grand_total = models.CharField(max_length=150)
    amt_in_words = models.CharField(max_length=150)

    def __str__(self):
        return self.PI_number
    
class EmployeeDetails(models.Model):
    emp_name = models.CharField(max_length=150)
    email = models.CharField(max_length=150)
    designation = models.CharField(max_length=150)
    joining_date = models.CharField(max_length=150)
    salary = models.CharField(max_length=150)

    def __str__(self):
        return str(self.emp_name)

class MaterialDetails(models.Model):
    material_name = models.CharField(max_length=150)
    amount = models.CharField(max_length=150)
    min_value = models.IntegerField()
    max_value = models.IntegerField()
    
    def __str__(self):
        return str(self.material_name)
    
class AttendanceRecord(models.Model):
    ATTENDANCE_CHOICES = [
        ('Present', 'Present'),
        ('Absent', 'Absent'),
        ('Half_Day', 'Half-Day'),
    ]

    employee = models.ForeignKey(EmployeeDetails, on_delete=models.CASCADE)
    date = models.DateField()
    attendance = models.CharField(max_length=10, choices=ATTENDANCE_CHOICES)

    class Meta:
        unique_together = ('employee', 'date')

    def __str__(self):
        return f"{self.employee} - {self.date}: {self.attendance}"