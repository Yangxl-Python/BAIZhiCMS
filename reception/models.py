from django.db import models

# Create your models here.


class UsersTable(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=64)
    email = models.CharField(max_length=20)
    salt = models.CharField(max_length=36)
    activation = models.BooleanField(default=False)

    class Meta:
        managed = False
        db_table = 'cms_users_table'
        unique_together = ('username',)
