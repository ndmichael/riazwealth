from django.conf import settings

EMAIL_BRAND = {
    "app_name": "Riazvest Secured",
    "primary_color": "#003366",   # header / titles
    "accent_color": "#66A3FF",    # buttons / links
    "success_color": "#32CD32",   # success states
    "bg_soft": "#E9F7EA",         # subtle sections
    "text_dark": "#0F172A",
    "text_muted": "#475569",
    "logo_url": f"{settings.SITE_URL}/static/images/logo.PNG",
    "support_email": "support@yourdomain.com",
    "app_url": "https://yourdomain.com",
}