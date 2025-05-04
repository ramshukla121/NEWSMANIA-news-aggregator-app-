from django.db import models

class Headline(models.Model):
    title = models.CharField(max_length=255)  # Title of the article
    image = models.URLField(null=True, blank=True)  # URL of the article's image
    url = models.URLField()  # URL of the article

    def __str__(self):
        return self.title