from django.db import models


class TextFile(models.Model):
    name = models.CharField(max_length=255)
    amount = models.IntegerField(null=True, blank=True)
    file = models.CharField(max_length=255, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    completed = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ('created',)

    def __unicode__(self):
        return self.name
