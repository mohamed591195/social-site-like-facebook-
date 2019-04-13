from django.db import models
from django.conf import settings

class Profile(models.Model):
    GENDER_CHOICES = (('male', 'M'), ('female', 'F'))
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='profile', on_delete=models.CASCADE)
    gender = models.CharField(max_length=30, choices=GENDER_CHOICES, blank=True)
    birth = models.DateField('Date Of Birth', blank=True, null=True)
    image = models.ImageField('Personal Image', upload_to='profile/images', blank=True, default='defaultPImage.png')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.get_full_name()
    
