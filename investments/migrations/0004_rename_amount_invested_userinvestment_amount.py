# Generated by Django 5.1.1 on 2025-01-09 15:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('investments', '0003_rename_investment_status_userinvestment_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userinvestment',
            old_name='amount_invested',
            new_name='amount',
        ),
    ]