from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.

User = get_user_model()


class Note(models.Model):
    title = models.CharField('Заголовок', max_length=69)
    text = models.TextField('Текст', max_length=1000)
    date = models.DateTimeField('Дата', auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True,
                               verbose_name='Автор')
