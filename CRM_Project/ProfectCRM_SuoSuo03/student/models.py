from django.db import models

# Create your models here.
class test(models.Model):
    name = models.CharField(max_length=1024)

    def __str__(self):
        return self.name