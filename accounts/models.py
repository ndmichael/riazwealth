from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import ASCIIUsernameValidator
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.core.mail import send_mail




'''
    - USER DATA MODELS
    - ** LIST OF DATA MODELS HERE **
    - * Custom User    
'''

class CustomUser(AbstractUser):
    '''
    - Override the django AbstractUser
    - to create and update the model features
    - Reasons are (to add more fields, make emails and username all lowercase and email unqiue)
    - including other utility methods
    '''
    username_validator = ASCIIUsernameValidator()
    username  = models.CharField(
        _("username"),
        max_length= 150,
        unique= True,
        help_text= _("Required. 150 characters or fewer. letters, digits, and @/./+/-/_ only"),
        validators= [username_validator],
        error_messages= {
            "unique": _("A user with the username already exists.")
        }
    )
    email = models.EmailField(
        _("email address"),
        unique= True,
        error_messages= {
            "unique": _("A user with that email address already exists.")
        }                       
    )
    terms_and_condition = models.BooleanField(verbose_name=_('terms'), default=False)
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        ordering = ['-date_joined']
        abstract = False
    
    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)
        self.username = self.username.lower()
        self.email = self.email.lower()
    
    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="profiles")
    bitcoin_wallet = models.CharField(max_length=150)
    ethereum_wallet = models.CharField(max_length=150)
    usdt_wallet = models.CharField(max_length=150)
    referral_code = models.CharField(max_length=10, unique=True, blank=True)

    def __str__(self) -> str:
        return f"user.username"