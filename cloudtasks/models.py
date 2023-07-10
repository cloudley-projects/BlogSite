from django.db import models
from django.contrib.auth.models import User

class cloudTaskBlog(models.Model):
    Title = models.CharField(max_length=255)
    Description = models.CharField(max_length=255)
    Pub_date = models.DateField()
    Author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.Title
    class Meta:
        db_table = 'cloudTaskBlog'
        verbose_name = 'cloudTaskBlog'
