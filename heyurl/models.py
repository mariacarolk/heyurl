from django.utils import timezone
from django.db import models
# CACAU Import the function used to create random codes
from .utils import create_short_url

class Url(models.Model):
    short_url = models.CharField(max_length=255, unique=True) #INCLUSO UNIQUE TRUE
    original_url = models.URLField(unique=True) #cacau alterado tipo / INCLUSO UNIQUE TRUE
    clicks = models.IntegerField(default=0)
    created_at = models.DateTimeField('date created')
    updated_at = models.DateTimeField('date updated')

    #CACAU only because we have rules here
    def save(self, *args, **kwargs):
        # If the short url wasn't specified
        if not self.short_url:
            # We pass the model instance that is being saved
            self.short_url = create_short_url(self)
            self.created_at = timezone.now()
            self.updated_at = timezone.now()
        else:
            self.updated_at = timezone.now()

        super().save(*args, **kwargs)

class Click(models.Model):
    url = models.ForeignKey(Url, on_delete=models.CASCADE)
    browser = models.CharField(max_length=255)
    platform = models.CharField(max_length=255)
    created_at = models.DateTimeField('date created')
    updated_at = models.DateTimeField('date updated')





