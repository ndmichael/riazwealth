from django.db.models.signals import post_save
from django.dispatch import receiver
from uuid import uuid4
from .models import CustomUser, Profile

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    print("sender ", sender)
    print("created: ", created)
    if created:
        profile = Profile.objects.create(user=instance)
        profile.referral_code = str(uuid4()).replace('-','').upper()[:8]
        profile.save()

@receiver(post_save, sender=CustomUser)
def save_profile(sender, instance, **kwargs):
    instance.profiles.save()