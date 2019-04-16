from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from account.models import Profile
from action.models import Action

class Comment(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='comments')
    comment = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    target_ct = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    target_id = models.PositiveIntegerField()
    target = GenericForeignKey('target_ct', 'target_id')
    replies = GenericRelation('self', content_type_field='target_ct', object_id_field='target_id', related_query_name='on_comment')
    actions = GenericRelation(Action, content_type_field='target_ct', object_id_field='target_id', related_query_name='comment')
    def __str__(self):
        return self.comment[:40]
