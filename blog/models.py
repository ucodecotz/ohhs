from django.db import models


# Create your models here.
class BlogPost(models.Model):
    title = models.CharField(max_length=100, null=True)
    content = models.TextField(null=True)

    class Meta:
        verbose_name_plural = 'Blog post'

    def __str__(self):
        return self.title
