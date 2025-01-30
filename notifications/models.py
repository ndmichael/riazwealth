from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class UserNotification(models.Model):
    """Stores notifications for specific users"""
    NOTIFICATION_TYPES = [
        ('withdrawal', 'Withdrawal'),
        ('investment', 'Investment'),
        ('referral', 'Referral'),
        ('system', 'System'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_notifications")
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def mark_as_read(self):
        self.is_read = True
        self.save()

    def __str__(self):
        return f"{self.user.username} - {self.notification_type}: {self.message[:50]}"


class GeneralNotification(models.Model):
    """Stores global announcements/news without duplicating per user"""
    title = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def latest_news():
        return GeneralNotification.objects.order_by('-created_at')[:5]  # Fetch latest 5 news items

    def __str__(self):
        return f"News: {self.title} - {self.created_at.strftime('%Y-%m-%d')}"

