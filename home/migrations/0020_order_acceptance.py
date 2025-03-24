# Generated by Django 5.0.1 on 2024-04-02 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0019_delete_item_quotation_data_amount_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='order_acceptance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qno', models.CharField(max_length=150)),
                ('q_date', models.CharField(max_length=150)),
                ('customer_name', models.CharField(max_length=150)),
                ('customer_address', models.CharField(max_length=150)),
                ('customer_contact', models.CharField(max_length=150)),
                ('customer_gst', models.CharField(max_length=150)),
                ('customer_reference', models.CharField(max_length=150)),
                ('sr_no', models.CharField(max_length=150)),
                ('item_details', models.TextField()),
                ('grade', models.CharField(max_length=150)),
                ('uom', models.CharField(max_length=150)),
                ('moq', models.CharField(max_length=150)),
                ('rate', models.CharField(max_length=150)),
                ('amount', models.CharField(max_length=150)),
                ('remark', models.CharField(max_length=150)),
                ('totalAmount', models.CharField(max_length=150)),
                ('packingForwarding', models.CharField(max_length=150)),
                ('cgst', models.CharField(max_length=150)),
                ('cgst_total', models.CharField(max_length=150)),
                ('sgst', models.CharField(max_length=150)),
                ('sgst_total', models.CharField(max_length=150)),
                ('igst', models.CharField(max_length=150)),
                ('igst_total', models.CharField(max_length=150)),
                ('grand_total', models.CharField(max_length=150)),
                ('amt_in_words', models.CharField(max_length=150)),
                ('payment_tc', models.CharField(max_length=150)),
                ('delivery_time_tc', models.CharField(max_length=150)),
                ('pf_tc', models.CharField(max_length=150)),
                ('for_tc', models.CharField(max_length=150)),
                ('q_validity_tc', models.CharField(max_length=150)),
                ('moq_tc', models.CharField(max_length=150)),
                ('material_tc', models.CharField(max_length=150)),
                ('other_tc', models.CharField(max_length=150)),
            ],
        ),
    ]
