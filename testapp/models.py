from django.db import models


class Calcu(models.Model):
    n = models.CharField(max_length=10)
