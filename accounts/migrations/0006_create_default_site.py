from django.db import migrations

def create_site(apps, schema_editor):
    Site = apps.get_model("sites", "Site")
    Site.objects.update_or_create(
        id=1,
        defaults={
            "domain": "riazvest.com",
            "name": "Riazvest",
        },
    )

class Migration(migrations.Migration):

    dependencies = [
        ("sites", "0002_alter_domain_unique"),
        ("accounts", "0005_alter_profile_referral_code"), 
    ]

    operations = [
        migrations.RunPython(create_site),
    ]