from django.db import models
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.dispatch import receiver
from django.db.models.signals import post_save
# Create your models here.


# Profile model attached to the custom django user
class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
	first_name = models.CharField(max_length=100, null=True, blank=True)
	last_name = models.CharField(max_length=100, null=True, blank=True)
	email = models.EmailField(max_length=255, null=True, blank=True)

@receiver(post_save, sender=User)
def generate_user_token(sender, instance=None, created=False, **kwargs):
	if created:
		Token.objects.create(user=instance)
		Profile.objects.create(user=instance)

		