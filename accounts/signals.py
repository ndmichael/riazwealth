from django.db.models.signals import post_save
from django.dispatch import receiver
from uuid import uuid4
from .models import CustomUser, Profile


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created and not instance.is_staff and not instance.is_superuser:
        if not hasattr(instance, 'profiles'):
            Profile.objects.create(
                user=instance,
                referral_code=str(uuid4()).replace('-', '').upper()[:8]
            )