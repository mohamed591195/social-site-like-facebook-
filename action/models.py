from django.db import models
from account.models import Profile
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

class Action(models.Model):
    profile   = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='actions')
    verb      = models.CharField(max_length=255)
    created   = models.DateTimeField(auto_now_add=True)
    target_ct = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True, related_name='target_object')
    target_id = models.PositiveIntegerField(null=True, blank=True, db_index=True)
    target    = GenericForeignKey('target_ct', 'target_id')

    def __str__(self):
        return '{} {} {}'.format(self.profile, self.verb, self.target)

    class Meta:
        ordering = ['-created']