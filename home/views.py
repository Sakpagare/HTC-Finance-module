from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from .verification import *
from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse
from .forms import *
from .models import *
import csv
from django.http import JsonResponse
from django.contrib import messages
from django.utils.timezone import now
from collections import defaultdict
import calendar

@login_required(login_url="/login/")
def index(request):
    logo = profile_picture.objects.get(name = request.user.id)
    quotations = quotation_data.objects.all().count()
    invoices = proforma_invoce.objects.all().count()
    employees = EmployeeDetails.objects.all().count()
    materials = MaterialDetails.objects.all().count()
    context = {'segment': 'index', "logo" : logo, 'quotations' : quotations, 'invoices' : invoices, 'employees' : employees, 'materials' : materials}

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def profile(request):
    profile_data = get_object_or_404(company_profile, company=request.user.id)
    profile_db = {'contact_no_1' : profile_data.contact_no_1, 'contact_no_2' : profile_data.contact_no_2, 'reg_address' : profile_data.reg_address, 'city' : profile_data.city, 'pincode' : profile_data.pincode, 'pan_no' : profile_data.pan_no, 'gst_no' : profile_data.gst_no, 'iec_code' : profile_data.iec_code} if profile_data else {}
    user_profile = company_profile_form(request.POST or None, initial=profile_db)
    
    bank_data = get_object_or_404(bank_details, company=request.user.id)
    bank_db = {'bank_name' : bank_data.bank_name, 'branch_name' : bank_data.branch_name, 'bank_acc_no' : bank_data.bank_acc_no, 're_enter_account_no' : bank_data.re_enter_account_no, 'ifsc_code' : bank_data.ifsc_code, 'swift_code' : bank_data.swift_code, 'ad_code' : bank_data.ad_code} if bank_data else {}
    bank_form = bank_details_update(request.POST or None, request.FILES or None, initial=bank_db)
    
    profile_pic = get_object_or_404(profile_picture, name=request.user.id)
    profile_pic_db = {'profile_image' : profile_pic.profile_image}
    profile_picture_form = profile_pic_form(request.POST or None, request.FILES or None, initial=profile_pic_db)

    logo = profile_picture.objects.get(name = request.user.id)
    msg = None

    if 'bank_details' in request.POST:
        if bank_form.is_valid():
            bank_name = bank_form.cleaned_data['bank_name']
            branch_name = bank_form.cleaned_data['branch_name']
            bank_acc_no = bank_form.cleaned_data['bank_acc_no']
            re_enter_account_no = bank_form.cleaned_data['re_enter_account_no']
            ifsc_code = bank_form.cleaned_data['ifsc_code']
            swift_code = bank_form.cleaned_data['swift_code']
            ad_code = bank_form.cleaned_data['ad_code']
            # upload_blank_cheque = bank_form.cleaned_data['upload_blank_cheque']
            # verify_form = bank_form_verification(bank_name, branch_name, bank_acc_no, re_enter_account_no, ifsc_code, swift_code, ad_code)
            # if verify_form == "Success":
            bank_details.objects.filter(company = request.user.id).update(bank_name = bank_name, branch_name = branch_name, bank_acc_no = bank_acc_no, re_enter_account_no = re_enter_account_no, ifsc_code = ifsc_code, swift_code = swift_code, ad_code = ad_code)
            messages.success(request, "Bank Details Updated!!!")
            return redirect("profile")
            # else:
            #     msg = verify_form
        else:
            msg = 'Error validating the form'
    
    elif 'profile_update' in request.POST:
        if user_profile.is_valid():
            contact_no_1 = user_profile.cleaned_data['contact_no_1']
            contact_no_2 = user_profile.cleaned_data['contact_no_2']
            reg_address = user_profile.cleaned_data['reg_address']
            city = user_profile.cleaned_data['city']
            pincode = user_profile.cleaned_data['pincode']
            pan_no = user_profile.cleaned_data['pan_no']
            gst_no = user_profile.cleaned_data['gst_no']
            iec_code = user_profile.cleaned_data['iec_code']
            verify_form = form_verification(contact_no_1, contact_no_2, reg_address, city, pincode, pan_no, gst_no, iec_code)
            if verify_form == "Success":
                company_profile.objects.filter(company = request.user.id).update(contact_no_1 = contact_no_1, contact_no_2 = contact_no_2, reg_address = reg_address, city = city, pincode = pincode, pan_no = pan_no, gst_no = gst_no, iec_code = iec_code)
                messages.success(request, "Profile Updated!!!")
                return redirect("profile")
            else:
                msg = verify_form
        else:
            msg = 'Error validating the form'

    elif 'profile_pic_update' in request.POST or request.FILES:
            if profile_picture_form.is_valid():
                profile_image = profile_picture_form.cleaned_data['profile_image']
                profile_picture.objects.filter(name = request.user.id).update(profile_image = profile_image)
                messages.success(request, "Profile Picture Updated!!!")
                return redirect("profile")

    else:
            msg = 'Error validating the form'
    return render(request, "home/profile.html", {"bank_form": bank_form, "user_profile" : user_profile, "profile_picture_form" : profile_picture_form, "logo" : logo, "msg": msg})


@login_required(login_url="/login/")
def download_details(request):
    profile_data = get_object_or_404(company_profile, company=request.user.id)
    bank_data = get_object_or_404(bank_details, company=request.user.id)
    profile_pic = get_object_or_404(profile_picture, name=request.user.id)
    logo = profile_picture.objects.get(name = request.user.id)
    
    return render(request, "home/download_details.html", {'profile_data' : profile_data, 'bank_data' : bank_data, 'profile_pic' : profile_pic  , "logo" : logo})

@login_required(login_url="/login/")
def quotation_table(request):
    logo = profile_picture.objects.get(name=request.user.id)
    profile_data = get_object_or_404(company_profile, company=request.user.id)
    logo_data = get_object_or_404(profile_picture, name=request.user.id)
    prev_quots = quotation_data.objects.all()
    new_quotation = quotation_data.objects.last()
    qdr_accpt = order_acceptance.objects.all()

    if not new_quotation:
        quotation_number = "Q24250001"
    else:
        # Extract the numeric part of the quotation number
        numeric_part = int(new_quotation.qno[1:])
        # Increment the numeric part
        numeric_part += 1
        # Concatenate the letter part "Q" with the incremented numeric part
        quotation_number = f"Q{numeric_part:08d}"  # Format the numeric part to have leading zeros if necessary

    return render(request, "home/quotation_table.html", {"profile_data": profile_data, 'logo': logo, "prev_quots": prev_quots, "quotation_number" : quotation_number, 'qdr_accpt' : qdr_accpt})

@login_required(login_url="/login/")
def quotation(request, quotation_number):
    profile_data = get_object_or_404(company_profile, company=request.user.id)
    bank_data = get_object_or_404(bank_details, company=request.user.id)
    logo = profile_picture.objects.get(name=request.user.id)
    material_names = MaterialDetails.objects.values_list('material_name', flat=True)
    try:
        material_details = []
        quotation_instance = quotation_data.objects.get(qno=quotation_number)


        # Evaluate each field using eval or ast.literal_eval
        sr_no = eval(quotation_instance.sr_no)
        item_details = eval(quotation_instance.item_details)
        grade = eval(quotation_instance.grade)
        uom = eval(quotation_instance.uom)
        moq = eval(quotation_instance.moq)
        rate = eval(quotation_instance.rate)
        amount = eval(quotation_instance.amount)
        for index in range(len(sr_no)):
            material_details.append({'sr_no' : int(sr_no[index]), 'item_details' : item_details[index], 'grade' : grade[index], 'uom' : uom[index], 'moq' : int(moq[index]), 'rate' : int(rate[index]), 'amount' : int(amount[index])})

        print(material_details)
        if "save" in request.POST:
            # name = request.user.username
            qno = request.POST.get('qno','')
            q_date = request.POST.get('q_date','')
            customer_name = request.POST.get('customer_name','')
            customer_address = request.POST.get('customer_address','')
            customer_contact = request.POST.get('customer_contact','')
            customer_gst = request.POST.get('customer_gst','')
            customer_reference = request.POST.get('customer_reference','')
            srNo = request.POST.get('srNo[]','')
            itemDetails = request.POST.get('itemDetails[]','')
            grade = request.POST.get('grade[]','')
            uom = request.POST.get('uom[]','')
            moq = request.POST.get('moq[]','')
            rate = request.POST.get('rate[]','')
            amount = request.POST.get('amount[]','')
            remark = request.POST.get('remark','')
            totalAmount = request.POST.get('totalAmount','')
            packingForwarding = request.POST.get('packingForwarding','')
            cgst = request.POST.get('cgst', '0')
            cgst_total = request.POST.get('cgst_total','')
            sgst = request.POST.get('sgst', '0')
            sgst_total = request.POST.get('sgst_total','')
            igst = request.POST.get('igst', '0')
            igst_total = request.POST.get('igst_total','')
            grand_total = request.POST.get('grand_total','')
            amt_in_words = request.POST.get('amt_in_words','')
            payment_tc = request.POST.get('payment_tc','')
            delivery_time_tc = request.POST.get('delivery_time_tc','')
            pf_tc = request.POST.get('pf_tc','')
            for_tc = request.POST.get('for_tc','')
            q_validity_tc = request.POST.get('q_validity_tc','')
            moq_tc = request.POST.get('moq_tc','')
            material_tc = request.POST.get('material_tc','')
            other_tc = request.POST.get('other_tc','')
            # Handle items
            srNo = request.POST.getlist('srNo[]', [])
            itemDetails = request.POST.getlist('itemDetails[]', [])
            grade = request.POST.getlist('grade[]', [])
            uom = request.POST.getlist('uom[]', [])
            moq = request.POST.getlist('moq[]', [])
            rate = request.POST.getlist('rate[]', [])
            amount = request.POST.getlist('amount[]', [])
            

            quotation_instance.qno=qno
            quotation_instance.q_date=q_date
            quotation_instance.customer_name=customer_name
            quotation_instance.customer_address=customer_address
            quotation_instance.customer_contact=customer_contact
            quotation_instance.customer_gst=customer_gst
            quotation_instance.customer_reference=customer_reference
            quotation_instance.sr_no=srNo
            quotation_instance.item_details=itemDetails
            quotation_instance.grade=grade
            quotation_instance.uom=uom
            quotation_instance.moq=moq
            quotation_instance.rate=rate
            quotation_instance.amount=amount
            quotation_instance.remark=remark
            quotation_instance.totalAmount=totalAmount
            quotation_instance.packingForwarding=packingForwarding
            quotation_instance.cgst=cgst
            quotation_instance.cgst_total=cgst_total
            quotation_instance.sgst=sgst
            quotation_instance.sgst_total=sgst_total
            quotation_instance.igst=igst
            quotation_instance.igst_total=igst_total
            quotation_instance.grand_total=grand_total
            quotation_instance.amt_in_words=amt_in_words
            quotation_instance.payment_tc=payment_tc
            quotation_instance.delivery_time_tc=delivery_time_tc
            quotation_instance.pf_tc=pf_tc
            quotation_instance.for_tc=for_tc
            quotation_instance.q_validity_tc=q_validity_tc
            quotation_instance.moq_tc=moq_tc
            quotation_instance.material_tc=material_tc
            quotation_instance.other_tc=other_tc
            quotation_instance.save()
            return redirect(reverse('quotation_print', kwargs={'qno': qno}))
        
        elif 'order_accept' in request.POST:
            qno = request.POST.get('qno','')
            q_date = request.POST.get('q_date','')
            customer_name = request.POST.get('customer_name','')
            customer_address = request.POST.get('customer_address','')
            customer_contact = request.POST.get('customer_contact','')
            customer_gst = request.POST.get('customer_gst','')
            customer_reference = request.POST.get('customer_reference','')
            srNo = request.POST.get('srNo[]','')
            itemDetails = request.POST.get('itemDetails[]','')
            grade = request.POST.get('grade[]','')
            uom = request.POST.get('uom[]','')
            moq = request.POST.get('moq[]','')
            rate = request.POST.get('rate[]','')
            amount = request.POST.get('amount[]','')
            remark = request.POST.get('remark','')
            totalAmount = request.POST.get('totalAmount','')
            packingForwarding = request.POST.get('packingForwarding','')
            cgst = request.POST.get('cgst', '0')
            cgst_total = request.POST.get('cgst_total','')
            sgst = request.POST.get('sgst', '0')
            sgst_total = request.POST.get('sgst_total','')
            igst = request.POST.get('igst', '0')
            igst_total = request.POST.get('igst_total','')
            grand_total = request.POST.get('grand_total','')
            amt_in_words = request.POST.get('amt_in_words','')
            payment_tc = request.POST.get('payment_tc','')
            delivery_time_tc = request.POST.get('delivery_time_tc','')
            pf_tc = request.POST.get('pf_tc','')
            for_tc = request.POST.get('for_tc','')
            q_validity_tc = request.POST.get('q_validity_tc','')
            moq_tc = request.POST.get('moq_tc','')
            material_tc = request.POST.get('material_tc','')
            other_tc = request.POST.get('other_tc','')
            # Handle items
            srNo = request.POST.getlist('srNo[]', [])
            itemDetails = request.POST.getlist('itemDetails[]', [])
            grade = request.POST.getlist('grade[]', [])
            uom = request.POST.getlist('uom[]', [])
            moq = request.POST.getlist('moq[]', [])
            rate = request.POST.getlist('rate[]', [])
            amount = request.POST.getlist('amount[]', [])

            quotation_instance = order_acceptance.objects.create(
                qno=qno,
                q_date=q_date,
                customer_name=customer_name,
                customer_address=customer_address,
                customer_contact=customer_contact,
                customer_gst=customer_gst,
                customer_reference=customer_reference,
                sr_no=srNo,
                item_details=itemDetails,
                grade=grade,
                uom=uom,
                moq=moq,
                rate=rate,
                amount=amount,
                remark=remark,
                totalAmount=totalAmount,
                packingForwarding=packingForwarding,
                cgst=cgst,
                cgst_total=cgst_total,
                sgst=sgst,
                sgst_total=sgst_total,
                igst=igst,
                igst_total=igst_total,
                grand_total=grand_total,
                amt_in_words=amt_in_words,
                payment_tc=payment_tc,
                delivery_time_tc=delivery_time_tc,
                pf_tc=pf_tc,
                for_tc=for_tc,
                q_validity_tc=q_validity_tc,
                moq_tc=moq_tc,
                material_tc=material_tc,
                other_tc=other_tc,
            )
            quotation_instance.save()
            messages.success(request,  'Quotation Accepted Successfully!!')
            return redirect(reverse('quotation_table'))


        return render(request, "home/quotation.html", {"profile_data" : profile_data, 'bank_data' : bank_data, 'logo' : logo, 'quotation_number' : quotation_number, 'quotation_instance' : quotation_instance, 'material_details' : material_details, 'material_names' : material_names})
 
    except:
          # Redirect to a success page
        if "save" in request.POST:
            # name = request.user.username
            qno = request.POST.get('qno','')
            q_date = request.POST.get('q_date','')
            customer_name = request.POST.get('customer_name','')
            customer_address = request.POST.get('customer_address','')
            customer_contact = request.POST.get('customer_contact','')
            customer_gst = request.POST.get('customer_gst','')
            customer_reference = request.POST.get('customer_reference','')
            srNo = request.POST.get('srNo[]','')
            itemDetails = request.POST.get('itemDetails[]','')
            grade = request.POST.get('grade[]','')
            uom = request.POST.get('uom[]','')
            moq = request.POST.get('moq[]','')
            rate = request.POST.get('rate[]','')
            amount = request.POST.get('amount[]','')
            remark = request.POST.get('remark','')
            totalAmount = request.POST.get('totalAmount','')
            packingForwarding = request.POST.get('packingForwarding','')
            cgst = request.POST.get('cgst', '0')
            cgst_total = request.POST.get('cgst_total','')
            sgst = request.POST.get('sgst', '0')
            sgst_total = request.POST.get('sgst_total','')
            igst = request.POST.get('igst', '0')
            igst_total = request.POST.get('igst_total','')
            grand_total = request.POST.get('grand_total','')
            amt_in_words = request.POST.get('amt_in_words','')
            payment_tc = request.POST.get('payment_tc','')
            delivery_time_tc = request.POST.get('delivery_time_tc','')
            pf_tc = request.POST.get('pf_tc','')
            for_tc = request.POST.get('for_tc','')
            q_validity_tc = request.POST.get('q_validity_tc','')
            moq_tc = request.POST.get('moq_tc','')
            material_tc = request.POST.get('material_tc','')
            other_tc = request.POST.get('other_tc','')
            # Handle items
            srNo = request.POST.getlist('srNo[]', [])
            itemDetails = request.POST.getlist('itemDetails[]', [])
            grade = request.POST.getlist('grade[]', [])
            uom = request.POST.getlist('uom[]', [])
            moq = request.POST.getlist('moq[]', [])
            rate = request.POST.getlist('rate[]', [])
            amount = request.POST.getlist('amount[]', [])
            # Create and save the quotation object
            quotation_instance = quotation_data.objects.create(
                qno=qno,
                q_date=q_date,
                customer_name=customer_name,
                customer_address=customer_address,
                customer_contact=customer_contact,
                customer_gst=customer_gst,
                customer_reference=customer_reference,
                sr_no=srNo,
                item_details=itemDetails,
                grade=grade,
                uom=uom,
                moq=moq,
                rate=rate,
                amount=amount,
                remark=remark,
                totalAmount=totalAmount,
                packingForwarding=packingForwarding,
                cgst=cgst,
                cgst_total=cgst_total,
                sgst=sgst,
                sgst_total=sgst_total,
                igst=igst,
                igst_total=igst_total,
                grand_total=grand_total,
                amt_in_words=amt_in_words,
                payment_tc=payment_tc,
                delivery_time_tc=delivery_time_tc,
                pf_tc=pf_tc,
                for_tc=for_tc,
                q_validity_tc=q_validity_tc,
                moq_tc=moq_tc,
                material_tc=material_tc,
                other_tc=other_tc,
            )
            quotation_instance.save()
            return redirect(reverse('quotation_print', kwargs={'qno': qno}))
        
        elif 'order_accept' in request.POST:
            qno = request.POST.get('qno','')
            q_date = request.POST.get('q_date','')
            customer_name = request.POST.get('customer_name','')
            customer_address = request.POST.get('customer_address','')
            customer_contact = request.POST.get('customer_contact','')
            customer_gst = request.POST.get('customer_gst','')
            customer_reference = request.POST.get('customer_reference','')
            srNo = request.POST.get('srNo[]','')
            itemDetails = request.POST.get('itemDetails[]','')
            grade = request.POST.get('grade[]','')
            uom = request.POST.get('uom[]','')
            moq = request.POST.get('moq[]','')
            rate = request.POST.get('rate[]','')
            amount = request.POST.get('amount[]','')
            remark = request.POST.get('remark','')
            totalAmount = request.POST.get('totalAmount','')
            packingForwarding = request.POST.get('packingForwarding','')
            cgst = request.POST.get('cgst', '0')
            cgst_total = request.POST.get('cgst_total','')
            sgst = request.POST.get('sgst', '0')
            sgst_total = request.POST.get('sgst_total','')
            igst = request.POST.get('igst', '0')
            igst_total = request.POST.get('igst_total','')
            grand_total = request.POST.get('grand_total','')
            amt_in_words = request.POST.get('amt_in_words','')
            payment_tc = request.POST.get('payment_tc','')
            delivery_time_tc = request.POST.get('delivery_time_tc','')
            pf_tc = request.POST.get('pf_tc','')
            for_tc = request.POST.get('for_tc','')
            q_validity_tc = request.POST.get('q_validity_tc','')
            moq_tc = request.POST.get('moq_tc','')
            material_tc = request.POST.get('material_tc','')
            other_tc = request.POST.get('other_tc','')
            # Handle items
            srNo = request.POST.getlist('srNo[]', [])
            itemDetails = request.POST.getlist('itemDetails[]', [])
            grade = request.POST.getlist('grade[]', [])
            uom = request.POST.getlist('uom[]', [])
            moq = request.POST.getlist('moq[]', [])
            rate = request.POST.getlist('rate[]', [])
            amount = request.POST.getlist('amount[]', [])
            # Create and save the quotation object
            quotation_instance = order_acceptance.objects.create(
                qno=qno,
                q_date=q_date,
                customer_name=customer_name,
                customer_address=customer_address,
                customer_contact=customer_contact,
                customer_gst=customer_gst,
                customer_reference=customer_reference,
                sr_no=srNo,
                item_details=itemDetails,
                grade=grade,
                uom=uom,
                moq=moq,
                rate=rate,
                amount=amount,
                remark=remark,
                totalAmount=totalAmount,
                packingForwarding=packingForwarding,
                cgst=cgst,
                cgst_total=cgst_total,
                sgst=sgst,
                sgst_total=sgst_total,
                igst=igst,
                igst_total=igst_total,
                grand_total=grand_total,
                amt_in_words=amt_in_words,
                payment_tc=payment_tc,
                delivery_time_tc=delivery_time_tc,
                pf_tc=pf_tc,
                for_tc=for_tc,
                q_validity_tc=q_validity_tc,
                moq_tc=moq_tc,
                material_tc=material_tc,
                other_tc=other_tc,
            )
            quotation_instance.save()
            messages.success(request,  'Quotation Accepted Successfully!!')
            return redirect(reverse('quotation_table'))

        return render(request, "home/quotation.html", {"profile_data" : profile_data, 'bank_data' : bank_data, 'logo' : logo, 'quotation_number' : quotation_number, 'material_names' : material_names})
        

@login_required(login_url="/login/")
def quotation_print(request, qno):
    profile_data = get_object_or_404(company_profile, company=request.user.id)
    bank_data = get_object_or_404(bank_details, company=request.user.id)
    logo_data = get_object_or_404(profile_picture, name=request.user.id)
    
    quotation_data_instances = quotation_data.objects.get(qno = qno)
    material_details = []
    sr_no = eval(quotation_data_instances.sr_no)
    item_details = eval(quotation_data_instances.item_details)
    grade = eval(quotation_data_instances.grade)
    uom = eval(quotation_data_instances.uom)
    moq = eval(quotation_data_instances.moq)
    rate = eval(quotation_data_instances.rate)
    amount = eval(quotation_data_instances.amount)
    for index in range(len(sr_no)):
        material_details.append({'sr_no' : int(sr_no[index]), 'item_details' : item_details[index], 'grade' : grade[index], 'uom' : uom[index], 'moq' : int(moq[index]), 'rate' : int(rate[index]), 'amount' : int(amount[index])})


    return render(request, "home/quotation_print.html", {"profile_data" : profile_data, 'bank_data' : bank_data, 'logo_data' : logo_data, 'quot_data' : quotation_data_instances, 'material_details' : material_details})


@login_required(login_url="/login/")
def proforma_table(request):
    logo = profile_picture.objects.get(name=request.user.id)
    profile_data = get_object_or_404(company_profile, company=request.user.id)
    logo_data = get_object_or_404(profile_picture, name=request.user.id)
    
    prev_qdr_accpt = order_acceptance.objects.all()
    new_order = proforma_invoce.objects.last()
    all_proforma = proforma_invoce.objects.all()

    if not new_order:
        PI_number = "PI24250001"
    else:
        # Extract the numeric part of the quotation number
        numeric_part = int(new_order.PI_number[2:])
        # Increment the numeric part
        numeric_part += 1
        # Concatenate the letter part "Q" with the incremented numeric part
        PI_number = f"PI{numeric_part:08d}"  # Format the numeric part to have leading zeros if necessary

    return render(request, "home/proforma_table.html", {"profile_data": profile_data, 'logo': logo, "PI_number" : PI_number, 'prev_qdr_accpt' : prev_qdr_accpt, 'all_proforma' : all_proforma})


@login_required(login_url="/login/")
def tax_table(request):
    logo = profile_picture.objects.get(name=request.user.id)
    profile_data = get_object_or_404(company_profile, company=request.user.id)
    logo_data = get_object_or_404(profile_picture, name=request.user.id)
    
    
    new_order = tax_invoce.objects.last()
    all_proforma = proforma_invoce.objects.all()
    prev_qdr_accpt = tax_invoce.objects.all()

    if not new_order:
        TI_number = "TI24250001"
    else:
        # Extract the numeric part of the quotation number
        numeric_part = int(new_order.TI_number[2:])
        # Increment the numeric part
        numeric_part += 1
        # Concatenate the letter part "Q" with the incremented numeric part
        TI_number = f"PI{numeric_part:08d}"  # Format the numeric part to have leading zeros if necessary

    return render(request, "home/tax_table.html", {"profile_data": profile_data, 'logo': logo, "TI_number" : TI_number, 'prev_qdr_accpt' : prev_qdr_accpt, 'all_proforma' : all_proforma})


@login_required(login_url="/login/")
def proforma(request, PI_number,quotation_number):
    profile_data = get_object_or_404(company_profile, company=request.user.id)
    bank_data = get_object_or_404(bank_details, company=request.user.id)
    logo = profile_picture.objects.get(name=request.user.id)
    try:
        material_details = []
        proforma_instance = proforma_invoce.objects.get(PI_number=PI_number)


        # Evaluate each field using eval or ast.literal_eval
        sr_no = eval(proforma_instance.sr_no)
        item_details = eval(proforma_instance.item_details)
        grade = eval(proforma_instance.grade)
        uom = eval(proforma_instance.uom)
        moq = eval(proforma_instance.moq)
        rate = eval(proforma_instance.rate)
        amount = eval(proforma_instance.amount)
        for index in range(len(sr_no)):
            material_details.append({'sr_no' : int(sr_no[index]), 'item_details' : item_details[index], 'grade' : grade[index], 'uom' : uom[index], 'moq' : int(moq[index]), 'rate' : int(rate[index]), 'amount' : int(amount[index])})

        print(material_details)
        if "save" in request.POST:
            # name = request.user.username
            PI_number = request.POST.get('PI_number','')
            invoice_date = request.POST.get('invoice_date','')
            PO_number = request.POST.get('PO_number','')
            po_date = request.POST.get('po_date','')
            customer_name = request.POST.get('customer_name','')
            customer_address = request.POST.get('customer_address','')
            customer_contact = request.POST.get('customer_contact','')
            customer_gst = request.POST.get('customer_gst','')
            customer_reference = request.POST.get('customer_reference','')
            srNo = request.POST.get('srNo[]','')
            itemDetails = request.POST.get('itemDetails[]','')
            grade = request.POST.get('grade[]','')
            uom = request.POST.get('uom[]','')
            moq = request.POST.get('moq[]','')
            rate = request.POST.get('rate[]','')
            amount = request.POST.get('amount[]','')
            remark = request.POST.get('remark','')
            totalAmount = request.POST.get('totalAmount','')
            packingForwarding = request.POST.get('packingForwarding','')
            cgst = request.POST.get('cgst', '0')
            cgst_total = request.POST.get('cgst_total','')
            sgst = request.POST.get('sgst', '0')
            sgst_total = request.POST.get('sgst_total','')
            igst = request.POST.get('igst', '0')
            igst_total = request.POST.get('igst_total','')
            grand_total = request.POST.get('grand_total','')
            amt_in_words = request.POST.get('amt_in_words','')
            srNo = request.POST.getlist('srNo[]', [])
            itemDetails = request.POST.getlist('itemDetails[]', [])
            grade = request.POST.getlist('grade[]', [])
            uom = request.POST.getlist('uom[]', [])
            moq = request.POST.getlist('moq[]', [])
            rate = request.POST.getlist('rate[]', [])
            amount = request.POST.getlist('amount[]', [])
            

            proforma_instance.PI_number=PI_number
            proforma_instance.invoice_date=invoice_date
            proforma_instance.PO_number=PO_number
            proforma_instance.po_date=po_date
            proforma_instance.customer_name=customer_name
            proforma_instance.customer_address=customer_address
            proforma_instance.customer_contact=customer_contact
            proforma_instance.customer_gst=customer_gst
            proforma_instance.customer_reference=customer_reference
            proforma_instance.sr_no=srNo
            proforma_instance.item_details=itemDetails
            proforma_instance.grade=grade
            proforma_instance.uom=uom
            proforma_instance.moq=moq
            proforma_instance.rate=rate
            proforma_instance.amount=amount
            proforma_instance.remark=remark
            proforma_instance.totalAmount=totalAmount
            proforma_instance.packingForwarding=packingForwarding
            proforma_instance.cgst=cgst
            proforma_instance.cgst_total=cgst_total
            proforma_instance.sgst=sgst
            proforma_instance.sgst_total=sgst_total
            proforma_instance.igst=igst
            proforma_instance.igst_total=igst_total
            proforma_instance.grand_total=grand_total
            proforma_instance.amt_in_words=amt_in_words
            proforma_instance.save()
            return redirect(reverse('proforma_print', kwargs={'PI_number': PI_number}))
        
        elif 'generate_tax' in request.POST:
            PI_number = request.POST.get('PI_number','')
            invoice_date = request.POST.get('invoice_date','')
            PO_number = request.POST.get('PO_number','')
            po_date = request.POST.get('po_date','')
            customer_name = request.POST.get('customer_name','')
            customer_address = request.POST.get('customer_address','')
            customer_contact = request.POST.get('customer_contact','')
            customer_gst = request.POST.get('customer_gst','')
            customer_reference = request.POST.get('customer_reference','')
            srNo = request.POST.get('srNo[]','')
            itemDetails = request.POST.get('itemDetails[]','')
            grade = request.POST.get('grade[]','')
            uom = request.POST.get('uom[]','')
            moq = request.POST.get('moq[]','')
            rate = request.POST.get('rate[]','')
            amount = request.POST.get('amount[]','')
            remark = request.POST.get('remark','')
            totalAmount = request.POST.get('totalAmount','')
            packingForwarding = request.POST.get('packingForwarding','')
            cgst = request.POST.get('cgst', '0')
            cgst_total = request.POST.get('cgst_total','')
            sgst = request.POST.get('sgst', '0')
            sgst_total = request.POST.get('sgst_total','')
            igst = request.POST.get('igst', '0')
            igst_total = request.POST.get('igst_total','')
            grand_total = request.POST.get('grand_total','')
            amt_in_words = request.POST.get('amt_in_words','')
            srNo = request.POST.getlist('srNo[]', [])
            itemDetails = request.POST.getlist('itemDetails[]', [])
            grade = request.POST.getlist('grade[]', [])
            uom = request.POST.getlist('uom[]', [])
            moq = request.POST.getlist('moq[]', [])
            rate = request.POST.getlist('rate[]', [])
            amount = request.POST.getlist('amount[]', [])

            proforma_instance = proforma_invoce.objects.create(
                PI_number=PI_number,
                invoice_date=invoice_date,
                PO_number=PO_number,
                po_date=po_date,
                customer_name=customer_name,
                customer_address=customer_address,
                customer_contact=customer_contact,
                customer_gst=customer_gst,
                customer_reference=customer_reference,
                sr_no=srNo,
                item_details=itemDetails,
                grade=grade,
                uom=uom,
                moq=moq,
                rate=rate,
                amount=amount,
                remark=remark,
                totalAmount=totalAmount,
                packingForwarding=packingForwarding,
                cgst=cgst,
                cgst_total=cgst_total,
                sgst=sgst,
                sgst_total=sgst_total,
                igst=igst,
                igst_total=igst_total,
                grand_total=grand_total,
                amt_in_words=amt_in_words,
            )
            proforma_instance.save()
            messages.success(request,  'Proforma Invoice send to Tax Invoice Successfully!!')
            return redirect(reverse('proforma_table'))


        return render(request, "home/proforma.html", {"profile_data" : profile_data, 'bank_data' : bank_data, 'logo' : logo, 'quotation_number' : quotation_number, 'proforma_instance' : proforma_instance, 'material_details' : material_details})
 
    except:
        quotation_instance = order_acceptance.objects.get(qno = quotation_number)


        # Evaluate each field using eval or ast.literal_eval
        sr_no = eval(quotation_instance.sr_no)
        item_details = eval(quotation_instance.item_details)
        grade = eval(quotation_instance.grade)
        uom = eval(quotation_instance.uom)
        moq = eval(quotation_instance.moq)
        rate = eval(quotation_instance.rate)
        amount = eval(quotation_instance.amount)
        for index in range(len(sr_no)):
            material_details.append({'sr_no' : int(sr_no[index]), 'item_details' : item_details[index], 'grade' : grade[index], 'uom' : uom[index], 'moq' : int(moq[index]), 'rate' : int(rate[index]), 'amount' : int(amount[index])})

        print(material_details)
          # Redirect to a success page
        
        if "save" in request.POST:
            # name = request.user.username
            PI_number = request.POST.get('PI_number','')
            invoice_date = request.POST.get('invoice_date','')
            PO_number = request.POST.get('PO_number','')
            po_date = request.POST.get('po_date','')
            customer_name = request.POST.get('customer_name','')
            customer_address = request.POST.get('customer_address','')
            customer_contact = request.POST.get('customer_contact','')
            customer_gst = request.POST.get('customer_gst','')
            customer_reference = request.POST.get('customer_reference','')
            srNo = request.POST.get('srNo[]','')
            itemDetails = request.POST.get('itemDetails[]','')
            grade = request.POST.get('grade[]','')
            uom = request.POST.get('uom[]','')
            moq = request.POST.get('moq[]','')
            rate = request.POST.get('rate[]','')
            amount = request.POST.get('amount[]','')
            remark = request.POST.get('remark','')
            totalAmount = request.POST.get('totalAmount','')
            packingForwarding = request.POST.get('packingForwarding','')
            cgst = request.POST.get('cgst', '0')
            cgst_total = request.POST.get('cgst_total','')
            sgst = request.POST.get('sgst', '0')
            sgst_total = request.POST.get('sgst_total','')
            igst = request.POST.get('igst', '0')
            igst_total = request.POST.get('igst_total','')
            grand_total = request.POST.get('grand_total','')
            amt_in_words = request.POST.get('amt_in_words','')
            srNo = request.POST.getlist('srNo[]', [])
            itemDetails = request.POST.getlist('itemDetails[]', [])
            grade = request.POST.getlist('grade[]', [])
            uom = request.POST.getlist('uom[]', [])
            moq = request.POST.getlist('moq[]', [])
            rate = request.POST.getlist('rate[]', [])
            amount = request.POST.getlist('amount[]', [])
            # Create and save the quotation object
            proforma_instance = proforma_invoce.objects.create(
                PI_number=PI_number,
                invoice_date=invoice_date,
                PO_number=PO_number,
                po_date=po_date,
                customer_name=customer_name,
                customer_address=customer_address,
                customer_contact=customer_contact,
                customer_gst=customer_gst,
                customer_reference=customer_reference,
                sr_no=srNo,
                item_details=itemDetails,
                grade=grade,
                uom=uom,
                moq=moq,
                rate=rate,
                amount=amount,
                remark=remark,
                totalAmount=totalAmount,
                packingForwarding=packingForwarding,
                cgst=cgst,
                cgst_total=cgst_total,
                sgst=sgst,
                sgst_total=sgst_total,
                igst=igst,
                igst_total=igst_total,
                grand_total=grand_total,
                amt_in_words=amt_in_words,
            )
            proforma_instance.save()
            return redirect(reverse('proforma_print', kwargs={'PI_number': PI_number}))
        
        elif 'generate_tax' in request.POST:
            qno = request.POST.get('qno','')
            q_date = request.POST.get('q_date','')
            customer_name = request.POST.get('customer_name','')
            customer_address = request.POST.get('customer_address','')
            customer_contact = request.POST.get('customer_contact','')
            customer_gst = request.POST.get('customer_gst','')
            customer_reference = request.POST.get('customer_reference','')
            srNo = request.POST.get('srNo[]','')
            itemDetails = request.POST.get('itemDetails[]','')
            grade = request.POST.get('grade[]','')
            uom = request.POST.get('uom[]','')
            moq = request.POST.get('moq[]','')
            rate = request.POST.get('rate[]','')
            amount = request.POST.get('amount[]','')
            remark = request.POST.get('remark','')
            totalAmount = request.POST.get('totalAmount','')
            packingForwarding = request.POST.get('packingForwarding','')
            cgst = request.POST.get('cgst', '0')
            cgst_total = request.POST.get('cgst_total','')
            sgst = request.POST.get('sgst', '0')
            sgst_total = request.POST.get('sgst_total','')
            igst = request.POST.get('igst', '0')
            igst_total = request.POST.get('igst_total','')
            grand_total = request.POST.get('grand_total','')
            amt_in_words = request.POST.get('amt_in_words','')
            payment_tc = request.POST.get('payment_tc','')
            delivery_time_tc = request.POST.get('delivery_time_tc','')
            pf_tc = request.POST.get('pf_tc','')
            for_tc = request.POST.get('for_tc','')
            q_validity_tc = request.POST.get('q_validity_tc','')
            moq_tc = request.POST.get('moq_tc','')
            material_tc = request.POST.get('material_tc','')
            other_tc = request.POST.get('other_tc','')
            # Handle items
            srNo = request.POST.getlist('srNo[]', [])
            itemDetails = request.POST.getlist('itemDetails[]', [])
            grade = request.POST.getlist('grade[]', [])
            uom = request.POST.getlist('uom[]', [])
            moq = request.POST.getlist('moq[]', [])
            rate = request.POST.getlist('rate[]', [])
            amount = request.POST.getlist('amount[]', [])
            # Create and save the quotation object
            quotation_instance = order_acceptance.objects.create(
                qno=qno,
                q_date=q_date,
                customer_name=customer_name,
                customer_address=customer_address,
                customer_contact=customer_contact,
                customer_gst=customer_gst,
                customer_reference=customer_reference,
                sr_no=srNo,
                item_details=itemDetails,
                grade=grade,
                uom=uom,
                moq=moq,
                rate=rate,
                amount=amount,
                remark=remark,
                totalAmount=totalAmount,
                packingForwarding=packingForwarding,
                cgst=cgst,
                cgst_total=cgst_total,
                sgst=sgst,
                sgst_total=sgst_total,
                igst=igst,
                igst_total=igst_total,
                grand_total=grand_total,
                amt_in_words=amt_in_words,
                payment_tc=payment_tc,
                delivery_time_tc=delivery_time_tc,
                pf_tc=pf_tc,
                for_tc=for_tc,
                q_validity_tc=q_validity_tc,
                moq_tc=moq_tc,
                material_tc=material_tc,
                other_tc=other_tc,
            )
            quotation_instance.save()
            messages.success(request,  'Proforma Invoice send to Tax Invoice Successfully!!')
            return redirect(reverse('quotation_table'))

    return render(request, "home/proforma.html", {"profile_data" : profile_data, 'bank_data' : bank_data, 'logo' : logo, 'quotation_number' : quotation_number, 'PI_number' : PI_number, 'quotation_instance' : quotation_instance, 'material_details' : material_details})

@login_required(login_url="/login/")
def proforma_print(request, PI_number):
    profile_data = get_object_or_404(company_profile, company=request.user.id)
    bank_data = get_object_or_404(bank_details, company=request.user.id)
    logo_data = get_object_or_404(profile_picture, name=request.user.id)
    
    proforma_data_instances = proforma_invoce.objects.get(PI_number = PI_number)
    material_details = []
    sr_no = eval(proforma_data_instances.sr_no)
    item_details = eval(proforma_data_instances.item_details)
    grade = eval(proforma_data_instances.grade)
    uom = eval(proforma_data_instances.uom)
    moq = eval(proforma_data_instances.moq)
    rate = eval(proforma_data_instances.rate)
    amount = eval(proforma_data_instances.amount)
    for index in range(len(sr_no)):
        material_details.append({'sr_no' : int(sr_no[index]), 'item_details' : item_details[index], 'grade' : grade[index], 'uom' : uom[index], 'moq' : int(moq[index]), 'rate' : int(rate[index]), 'amount' : int(amount[index])})


    return render(request, "home/proforma_print.html", {"profile_data" : profile_data, 'bank_data' : bank_data, 'logo_data' : logo_data, 'quot_data' : proforma_data_instances, 'material_details' : material_details})


@login_required(login_url="/login/")
def tax_invoice(request, PI_number,TI_number):
    # profile_data = get_object_or_404(company_profile, company=request.user.id)
    # bank_data = get_object_or_404(bank_details, company=request.user.id)
    # logo = profile_picture.objects.get(name=request.user.id)
    
    # quotation_instance = order_acceptance.objects.get(qno = quotation_number)

    # material_details = []
    # sr_no = eval(proforma_data_instances.sr_no)
    # item_details = eval(proforma_data_instances.item_details)
    # grade = eval(proforma_data_instances.grade)
    # uom = eval(proforma_data_instances.uom)
    # moq = eval(proforma_data_instances.moq)
    # rate = eval(proforma_data_instances.rate)
    # amount = eval(proforma_data_instances.amount)
    # for index in range(len(sr_no)):
    #     material_details.append({'sr_no' : int(sr_no[index]), 'item_details' : item_details[index], 'grade' : grade[index], 'uom' : uom[index], 'moq' : int(moq[index]), 'rate' : int(rate[index]), 'amount' : int(amount[index])})

    # # Evaluate each field using eval or ast.literal_eval
    # sr_no = eval(quotation_instance.sr_no)
    # item_details = eval(quotation_instance.item_details)
    # grade = eval(quotation_instance.grade)
    # uom = eval(quotation_instance.uom)
    # moq = eval(quotation_instance.moq)
    # rate = eval(quotation_instance.rate)
    # amount = eval(quotation_instance.amount)
    # for index in range(len(sr_no)):
    #     material_details.append({'sr_no' : int(sr_no[index]), 'item_details' : item_details[index], 'grade' : grade[index], 'uom' : uom[index], 'moq' : int(moq[index]), 'rate' : int(rate[index]), 'amount' : int(amount[index])})

    # print(material_details)
    #     # Redirect to a success page
    
    # if "save" in request.POST:
    #     # name = request.user.username
    #     PI_number = request.POST.get('PI_number','')
    #     invoice_date = request.POST.get('invoice_date','')
    #     PO_number = request.POST.get('PO_number','')
    #     po_date = request.POST.get('po_date','')
    #     customer_name = request.POST.get('customer_name','')
    #     customer_address = request.POST.get('customer_address','')
    #     customer_contact = request.POST.get('customer_contact','')
    #     customer_gst = request.POST.get('customer_gst','')
    #     customer_reference = request.POST.get('customer_reference','')
    #     srNo = request.POST.get('srNo[]','')
    #     itemDetails = request.POST.get('itemDetails[]','')
    #     grade = request.POST.get('grade[]','')
    #     uom = request.POST.get('uom[]','')
    #     moq = request.POST.get('moq[]','')
    #     rate = request.POST.get('rate[]','')
    #     amount = request.POST.get('amount[]','')
    #     remark = request.POST.get('remark','')
    #     totalAmount = request.POST.get('totalAmount','')
    #     packingForwarding = request.POST.get('packingForwarding','')
    #     cgst = request.POST.get('cgst', '0')
    #     cgst_total = request.POST.get('cgst_total','')
    #     sgst = request.POST.get('sgst', '0')
    #     sgst_total = request.POST.get('sgst_total','')
    #     igst = request.POST.get('igst', '0')
    #     igst_total = request.POST.get('igst_total','')
    #     grand_total = request.POST.get('grand_total','')
    #     amt_in_words = request.POST.get('amt_in_words','')
    #     srNo = request.POST.getlist('srNo[]', [])
    #     itemDetails = request.POST.getlist('itemDetails[]', [])
    #     grade = request.POST.getlist('grade[]', [])
    #     uom = request.POST.getlist('uom[]', [])
    #     moq = request.POST.getlist('moq[]', [])
    #     rate = request.POST.getlist('rate[]', [])
    #     amount = request.POST.getlist('amount[]', [])
    #     # Create and save the quotation object
    #     proforma_instance = proforma_invoce.objects.create(
    #         PI_number=PI_number,
    #         invoice_date=invoice_date,
    #         PO_number=PO_number,
    #         po_date=po_date,
    #         customer_name=customer_name,
    #         customer_address=customer_address,
    #         customer_contact=customer_contact,
    #         customer_gst=customer_gst,
    #         customer_reference=customer_reference,
    #         sr_no=srNo,
    #         item_details=itemDetails,
    #         grade=grade,
    #         uom=uom,
    #         moq=moq,
    #         rate=rate,
    #         amount=amount,
    #         remark=remark,
    #         totalAmount=totalAmount,
    #         packingForwarding=packingForwarding,
    #         cgst=cgst,
    #         cgst_total=cgst_total,
    #         sgst=sgst,
    #         sgst_total=sgst_total,
    #         igst=igst,
    #         igst_total=igst_total,
    #         grand_total=grand_total,
    #         amt_in_words=amt_in_words,
    #     )
    #     proforma_instance.save()
    #     return redirect(reverse('proforma_print', kwargs={'PI_number': PI_number}))
    
    # elif 'generate_tax' in request.POST:
    #     qno = request.POST.get('qno','')
    #     q_date = request.POST.get('q_date','')
    #     customer_name = request.POST.get('customer_name','')
    #     customer_address = request.POST.get('customer_address','')
    #     customer_contact = request.POST.get('customer_contact','')
    #     customer_gst = request.POST.get('customer_gst','')
    #     customer_reference = request.POST.get('customer_reference','')
    #     srNo = request.POST.get('srNo[]','')
    #     itemDetails = request.POST.get('itemDetails[]','')
    #     grade = request.POST.get('grade[]','')
    #     uom = request.POST.get('uom[]','')
    #     moq = request.POST.get('moq[]','')
    #     rate = request.POST.get('rate[]','')
    #     amount = request.POST.get('amount[]','')
    #     remark = request.POST.get('remark','')
    #     totalAmount = request.POST.get('totalAmount','')
    #     packingForwarding = request.POST.get('packingForwarding','')
    #     cgst = request.POST.get('cgst', '0')
    #     cgst_total = request.POST.get('cgst_total','')
    #     sgst = request.POST.get('sgst', '0')
    #     sgst_total = request.POST.get('sgst_total','')
    #     igst = request.POST.get('igst', '0')
    #     igst_total = request.POST.get('igst_total','')
    #     grand_total = request.POST.get('grand_total','')
    #     amt_in_words = request.POST.get('amt_in_words','')
    #     payment_tc = request.POST.get('payment_tc','')
    #     delivery_time_tc = request.POST.get('delivery_time_tc','')
    #     pf_tc = request.POST.get('pf_tc','')
    #     for_tc = request.POST.get('for_tc','')
    #     q_validity_tc = request.POST.get('q_validity_tc','')
    #     moq_tc = request.POST.get('moq_tc','')
    #     material_tc = request.POST.get('material_tc','')
    #     other_tc = request.POST.get('other_tc','')
    #     # Handle items
    #     srNo = request.POST.getlist('srNo[]', [])
    #     itemDetails = request.POST.getlist('itemDetails[]', [])
    #     grade = request.POST.getlist('grade[]', [])
    #     uom = request.POST.getlist('uom[]', [])
    #     moq = request.POST.getlist('moq[]', [])
    #     rate = request.POST.getlist('rate[]', [])
    #     amount = request.POST.getlist('amount[]', [])
    #     # Create and save the quotation object
    #     quotation_instance = order_acceptance.objects.create(
    #         qno=qno,
    #         q_date=q_date,
    #         customer_name=customer_name,
    #         customer_address=customer_address,
    #         customer_contact=customer_contact,
    #         customer_gst=customer_gst,
    #         customer_reference=customer_reference,
    #         sr_no=srNo,
    #         item_details=itemDetails,
    #         grade=grade,
    #         uom=uom,
    #         moq=moq,
    #         rate=rate,
    #         amount=amount,
    #         remark=remark,
    #         totalAmount=totalAmount,
    #         packingForwarding=packingForwarding,
    #         cgst=cgst,
    #         cgst_total=cgst_total,
    #         sgst=sgst,
    #         sgst_total=sgst_total,
    #         igst=igst,
    #         igst_total=igst_total,
    #         grand_total=grand_total,
    #         amt_in_words=amt_in_words,
    #         payment_tc=payment_tc,
    #         delivery_time_tc=delivery_time_tc,
    #         pf_tc=pf_tc,
    #         for_tc=for_tc,
    #         q_validity_tc=q_validity_tc,
    #         moq_tc=moq_tc,
    #         material_tc=material_tc,
    #         other_tc=other_tc,
    #     )
    #     quotation_instance.save()
    #     quot_data = quotation_data.objects.get(qno=qno)
    #     quot_data.delete()
    #     messages.success(request,  'Proforma Invoice send to Tax Invoice Successfully!!')
    #     return redirect(reverse('quotation_table'))

    return render(request, "home/tax_invoice.html")



@login_required(login_url="/login/")
def employee_reg(request):
    logo = profile_picture.objects.get(name = request.user.id)
    if request.method == "POST":
        emp_name = request.POST['emp_name']
        email = request.POST['email']
        designation = request.POST['designation']
        joining_date = request.POST['joining_date']
        salary = request.POST['salary']

        emp_data = EmployeeDetails(emp_name = emp_name, email = email, designation = designation, joining_date = joining_date, salary = salary)
        emp_data.save()
        messages.success(request, "Employee Added Successfully")
        return redirect("employee_reg")


    return render(request, "home/employee_reg.html", {'logo' : logo})


@login_required(login_url="/login/")
def attendance(request):
    logo = profile_picture.objects.get(name=request.user.id)
    emp_data = EmployeeDetails.objects.all()

    return render(request, "home/attendance.html", {'logo': logo, 'emp_data': emp_data})

@login_required(login_url="/login/")
def mark_attendance(request):
    logo = profile_picture.objects.get(name=request.user.id)
    emp_data = EmployeeDetails.objects.all()

    if request.method == 'POST':
        attendance_data = request.POST.getlist('attendance[]')
        att_date = request.POST.get('att_date', '')
        for attendance, employee in zip(attendance_data, emp_data):
            # Get or create an AttendanceRecord for the current employee and today's date
            attendance_record, created = AttendanceRecord.objects.get_or_create(
                employee=employee, 
                attendance = attendance,
                date=att_date
            )
            attendance_record.save()
        messages.success(request, 'Attendance marked successfully')
        return redirect('attendance')  # Redirect to the attendance page after marking attendance

    return render(request, "home/attendance.html", {'logo': logo, 'emp_data': emp_data})

def calculate_salary(salary_per_month, total_working_days, present_days, half_days):
    # Calculate salary per day
    salary_per_day = salary_per_month / total_working_days

    # Calculate salary for present days
    present_salary = present_days * salary_per_day

    # Calculate salary for half days
    half_day_salary = (half_days * salary_per_day) / 2

    # Calculate final salary
    final_salary = present_salary + half_day_salary

    return final_salary

@login_required(login_url="/login/")
def salary(request):
    logo = profile_picture.objects.get(name=request.user.id)
    emp_attendance_counts = defaultdict(lambda: {'Present': 0, 'Absent': 0, 'Half_Day': 0, 'Final_Salary': 0})
    emp_list = EmployeeDetails.objects.all()
    selected_month = None  # Initialize selected_month variable

    if request.method == "POST":
        month_select = int(request.POST['month_select'])  # Convert the selected month to integer
        selected_month = calendar.month_name[month_select]  # Get the month name from calendar module
        for emp in emp_list:
            # Get the EmployeeDetails instance for the current employee
            employee_instance = get_object_or_404(EmployeeDetails, emp_name=emp)
            salary_per_month = employee_instance.salary  # Fetch the salary for the current employee
            total_working_days = 24  # Assuming 24 working days in a month
            
            # Filter attendance records for the current employee for the selected month
            records = AttendanceRecord.objects.filter(employee=employee_instance, date__month=month_select)
            for record in records:
                # Increment the count for the current attendance status
                emp_attendance_counts[emp.emp_name][record.attendance] += 1

            # Calculate final salary for the current employee based on attendance records
            counts = emp_attendance_counts[emp.emp_name]
            present_days = counts['Present']
            half_days = counts['Half_Day']  # Use underscore instead of hyphen
            days_absent = counts['Absent']

            final_salary = calculate_salary(int(salary_per_month), total_working_days, present_days, half_days)
            counts['Final_Salary'] = round(final_salary, 2)

    return render(request, "home/salary.html", {'logo': logo, 'emp_attendance_counts': dict(emp_attendance_counts), 'selected_month': selected_month})


@login_required(login_url="/login/")
def inventory(request):
    logo = profile_picture.objects.get(name = request.user.id)
    materials = MaterialDetails.objects.all().order_by('material_name')
    if request.method == "POST":
        material_name = request.POST['material_name']
        amount = request.POST['amount']
        min_value = request.POST['min_value']
        max_value = request.POST['max_value']
        
        emp_data = MaterialDetails(material_name = material_name, amount = amount)
        emp_data.save()
        messages.success(request, "Material Added Successfully")
        return redirect("inventory")


    return render(request, "home/inventory.html", {'logo': logo, 'materials' : materials})

def convert_number_to_words(request, number):
    response = requests.get(f'http://api.mathjs.org/v4/?expr=spellout({number})')
    if response.status_code == 200:
        return JsonResponse({'words': response.text})
    else:
        return JsonResponse({'error': 'Failed to convert number to words'}, status=500)
    
@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))

