from django.db import models

# Create your models here.


class Film(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField(null=True)
    duration = models.IntegerField()
    rating_kinopoisk = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
