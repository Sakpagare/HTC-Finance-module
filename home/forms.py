from django import forms
from .models import *
class bank_details_update(forms.ModelForm):
    class Meta:
        model = bank_details
        fields = [
            'bank_name', 
            'branch_name',
            'bank_acc_no',
            're_enter_account_no',
            'ifsc_code', 
            'swift_code', 
            'ad_code',
        ]
        widgets = {
            'bank_name' : forms.TextInput(attrs={'class': "form-control", 'type' : 'text', 'placeholder' : 'Bank Name'}),
            'branch_name' : forms.TextInput(attrs={'class': "form-control", 'type' : 'text', 'placeholder' : 'Branch Name'}),
            'bank_acc_no' : forms.TextInput(attrs={'class': "form-control", 'type' : 'password', 'placeholder' : 'Bank Account Number'}),
            're_enter_account_no' : forms.TextInput(attrs={'class': "form-control", 'type' : 'text', 'placeholder' : 'Bank Account Number'}),
            'ifsc_code' : forms.TextInput(attrs={'class': "form-control", 'type' : 'text', 'placeholder' : 'IFSC Code'}),
            'swift_code' : forms.TextInput(attrs={'class': "form-control", 'type' : 'text', 'placeholder' : 'SWIFT Code'}),
            'ad_code' : forms.TextInput(attrs={'class': "form-control", 'type' : 'text', 'placeholder' : 'AD Code'}),
            
        }
    swift_code = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control", 'type' : 'text', 'placeholder' : 'SWIFT Code'}),
        required=False
    )

    ad_code = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control", 'type' : 'text', 'placeholder' : 'AD Code'}),
        required=False
    )
    
        
class company_profile_form(forms.ModelForm):
    class Meta:
        model = company_profile  # Set the model for the form
        fields = [
            'contact_no_1',
            'contact_no_2',
            'reg_address',
            'city',
            'pincode',
            'pan_no',
            'gst_no',
            'iec_code',
        ]
        widgets = {
            'contact_no_1': forms.TextInput(attrs={'class': "form-control", 'type': 'text', 'placeholder': 'Contact Number'}),
            'contact_no_2': forms.TextInput(attrs={'class': "form-control", 'type': 'text', 'placeholder': 'Contact Number'}),
            'reg_address': forms.Textarea(attrs={'class': "form-control", 'type': 'text', 'placeholder': 'Registered Address'}),
            'city': forms.TextInput(attrs={'class': "form-control", 'type': 'text', 'placeholder': 'City'}),
            'pincode': forms.TextInput(attrs={'class': "form-control", 'type': 'text', 'placeholder': 'PIN Code', 'id': 'pincode'}),
            'pan_no': forms.TextInput(attrs={'class': "form-control", 'type': 'text', 'placeholder': 'PAN Number'}),
            'gst_no': forms.TextInput(attrs={'class': "form-control", 'type': 'text', 'placeholder': 'GST Number'}),
            'iec_code': forms.TextInput(attrs={'class': "form-control", 'type': 'text', 'placeholder': 'ISE Number'}),
        }
        # Set required attribute for specific fields
    contact_no_2 = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control", 'type': 'text', 'placeholder': 'Contact Number'}),
        required=False
    )

    iec_code = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control", 'type': 'text', 'placeholder': 'ISE Number'}),
        required=False
    )

class profile_pic_form(forms.ModelForm):
    class Meta:
        model = profile_picture  # Set the model for the form
        fields = [
            'profile_image',
        ]
        widgets = {
            'profile_image': forms.FileInput(attrs={'class': "form-control", 'type' : 'file', 'placeholder' : 'Upload Profile Picture', 'accept' : 'image/png, image/jpg, image/jpeg'}),
        }
    profile_image = forms.ImageField(
        widget=forms.FileInput(attrs={'class': "form-control", 'type' : 'file', 'placeholder' : 'Upload Profile Picture', 'accept' : 'image/png, image/jpg, image/jpeg'}),
        required=True
    )

# class quotation_form(forms.ModelForm):
#     class Meta:
#         model = quotation

#         fields = [
#             'qno',
#             'q_date',
#             'customer_name',
#             'customer_address',
#             'customer_contact',
#             'customer_gst',
#             'customer_reference',
#             'srNo[]',
#             'itemDetails[]',
#             'grade[]',
#             'uom[]',
#             'moq[]',
#             'rate[]',
#             'amount[]',
#             'remark',
#             'totalAmount',
#             'packingForwarding',
#             'cgst',
#             'cgst_total',
#             'sgst',
#             'sgst_total',
#             'igst',
#             'igst_total',
#             'grand_total',
#             'amt_in_words',
#             'payment_tc',
#             'delivery_time_tc',
#             'pf_tc',
#             'for_tc',
#             'q_validity_tc',
#             'moq_tc',
#             'material_tc',
#             'other_tc',

#         ]
#         widgets = {
#             'qno' : 
#             'q_date' : 
#             'customer_name' : 
#             'customer_address' : 
#             'customer_contact' : 
#             'customer_gst' : 
#             'customer_reference' : 
#             'srNo[]' : 
#             'itemDetails[]' : 
#             'grade[]' : 
#             'uom[]' : 
#             'moq[]' : 
#             'rate[]' : 
#             'amount[]' : 
#             'remark' : 
#             'totalAmount' : 
#             'packingForwarding' : 
#             'cgst' : 
#             'cgst_total' : 
#             'sgst' : 
#             'sgst_total' : 
#             'igst' : 
#             'igst_total' : 
#             'grand_total' : 
#             'amt_in_words' : 
#             'payment_tc' : 
#             'delivery_time_tc' : 
#             'pf_tc' : 
#             'for_tc' : 
#             'q_validity_tc' : 
#             'moq_tc' : 
#             'material_tc' : 
#             'other_tc' : 
#         }