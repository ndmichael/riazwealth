# Generated by Django 5.1.1 on 2024-11-06 18:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('withdrawals', '0002_withdrawalrequest_payment'),
    ]

    operations = [
        migrations.RenameField(
            model_name='withdrawalrequest',
            old_name='payment',
            new_name='payment_option',
        ),
    ]
