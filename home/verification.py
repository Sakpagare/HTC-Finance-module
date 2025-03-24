import requests
import pandas as pd
import re

def contact_verify(contact_number):
    # Define the regular expression pattern for the Indian mobile number format
    pattern = r'^[789]\d{9}$'

    # Use re.match() to check if the given contact number matches the pattern
    return bool(re.match(pattern, contact_number))

def address_verify(reg_address):
    if len(reg_address) > 10:
        return True
    else:
        return False
    
def city_verify(city):
    if city.isalpha() and len(city) > 1:
        return True
    else:
        return False 

def pincode_verify(pincode):
    if pincode.isdigit() and len(pincode) == 6:
        return True
    else:
        return False

def city_pin_verify(city, pincode):
    data_frame = pd.read_csv('apps/static/codes/pincode.csv')
    dictionary_data = dict(zip(data_frame['Pincode'], data_frame['District']))
    city_name = dictionary_data.get(eval(pincode))
    if city.lower() == city_name.lower():
        return True
    else:
        return "City Name should be " + city_name
    
def verify_pan(pan_no):
    pan_pattern = r'^[A-Z]{5}\d{4}[A-Z]$'
    
    # Check if the provided PAN number matches the pattern
    if re.match(pan_pattern, pan_no):
        return True
    else:
        return False

def is_valid_gst_number(gst_number):
    # Regular expression pattern for GST number
    gst_pattern = r'^\d{2}[A-Z]{5}\d{4}[A-Z]{1}\d[Z]{1}[A-Z\d]{1}$'
    
    # Check if the provided GST number matches the pattern
    if re.match(gst_pattern, gst_number):
        return True
    else:
        return False

def is_valid_iec_number(iec_number):
    # Define the regular expression pattern for the IEC number format
    pattern = r'^[A-Z]{2}\d{7}[A-Z]$'

    # Use re.match() to check if the given IEC number matches the pattern
    return bool(re.match(pattern, iec_number))

def form_verification(contact_no_1, contact_no_2, reg_address, city, pincode, pan_no, gst_no, iec_code):
    if contact_verify(contact_no_1) == False:
        return "Invalid Contact Number 1"
    elif len(contact_no_2) > 1:
        if contact_verify(contact_no_2) == False:
            return "Invalid Contact Number 2"
    elif address_verify(reg_address) == False:
        return "Address should be Greater than 10 Characters"
    elif city_pin_verify(city, pincode) != True:
        result = city_pin_verify(city, pincode)
        return result
    elif verify_pan(pan_no) == False:
        return "Invalid PAN Number"
    elif is_valid_gst_number(gst_no) == False:
        return "Invalid GST Number"
    elif len(iec_code) > 1:
        if is_valid_iec_number(iec_code) == False:
            return "Invalid IEC Number"
    return "Success"
###############################################################################################
#                                 Bank Details Verification                                   #
###############################################################################################


# def bank_form_verification(bank_name, branch_name, bank_acc_no, re_enter_account_no, ifsc_code, swift_code, ad_code):
