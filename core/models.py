from django.db import models

# Create your models here.
class Event(models.Model):
    created_by = models.ForeignKey('account.User', on_delete=models.CASCADE, related_name='created_events')
    title = models.CharField(verbose_name='Title', max_length=255)
    description = models.TextField(verbose_name='Description')
    date = models.DateField(verbose_name='Date')
    guests = models.ManyToManyField('account.User', related_name='joined_events')

    class Meta:
        unique_together = ('title', 'date')
        
    def __str__(self):
        return self.title