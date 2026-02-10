from django.db import migrations, connection

def fix_sites(apps, schema_editor):
    with connection.cursor() as cursor:
        # 1. Create django_site table ONLY if missing
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS django_site (
            id SERIAL PRIMARY KEY,
            domain VARCHAR(100) NOT NULL,
            name VARCHAR(50) NOT NULL
        );
        """)

        # 2. Ensure a default site exists
        cursor.execute("""
        INSERT INTO django_site (id, domain, name)
        VALUES (1, 'riazvest.com', 'Riazvest')
        ON CONFLICT (id) DO NOTHING;
        """)

        # 3. Mark sites migration as applied
        cursor.execute("""
        INSERT INTO django_migrations (app, name, applied)
        VALUES ('sites', '0001_initial', NOW())
        ON CONFLICT DO NOTHING;
        """)

class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0006_create_default_site"),
    ]

    operations = [
        migrations.RunPython(fix_sites),
    ]