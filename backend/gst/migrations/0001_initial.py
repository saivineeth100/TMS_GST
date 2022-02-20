# Generated by Django 3.2.9 on 2022-02-20 12:50

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TaxDue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cgst', models.DecimalField(decimal_places=2, max_digits=10)),
                ('sgst', models.DecimalField(decimal_places=2, max_digits=10)),
                ('ugst', models.DecimalField(decimal_places=2, max_digits=10)),
                ('igst', models.DecimalField(decimal_places=2, max_digits=10)),
                ('cess', models.DecimalField(decimal_places=2, max_digits=10)),
                ('total', models.DecimalField(decimal_places=2, max_digits=1000)),
                ('generatedon', models.DateTimeField(auto_now_add=True)),
                ('editedon', models.DateTimeField(auto_now=True)),
                ('ispaid', models.BooleanField(default=False)),
                ('generatedby', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_query_name='clienttaxdues', to='users.taxaccountant', verbose_name='taxaccountants')),
                ('taxpayer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_query_name='taxdues', to='users.taxpayer', verbose_name='taxpayers')),
            ],
        ),
        migrations.CreateModel(
            name='TaxDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('taxrate', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(50)])),
                ('cessrate', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(50)])),
                ('isexempt', models.BooleanField(default=False)),
                ('interstate', models.BooleanField(default=False)),
                ('value', models.DecimalField(decimal_places=2, max_digits=10)),
                ('taxdue', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_query_name='taxdetails', to='gst.taxdue', verbose_name='taxdues')),
                ('taxpayer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_query_name='taxdetails', to='users.taxpayer', verbose_name='taxpayers')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('taxrate', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(50)])),
                ('cessrate', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(50)])),
                ('isexempt', models.BooleanField(default=False)),
                ('taxpayer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_query_name='services', to='users.taxpayer', verbose_name='taxpayers')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('taxrate', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(50)])),
                ('cessrate', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(50)])),
                ('isexempt', models.BooleanField(default=False)),
                ('taxpayer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_query_name='products', to='users.taxpayer', verbose_name='taxpayers')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
