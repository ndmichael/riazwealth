# Generated by Django 5.1.1 on 2025-01-10 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('investments', '0007_rename_ref_code_userinvestment_ref_token_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinvestment',
            name='next_accrual_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
