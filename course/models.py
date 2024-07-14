from django.db import models

from config.settings import AUTH_USER_MODEL

NULLABLE = {'null': True,
            'blank': True}

# Create your models here.
class Course(models.Model):
    title = models.CharField(max_length=150, verbose_name='Course title')
    description = models.TextField(verbose_name='Course description')
    preview = models.ImageField(upload_to='media/', verbose_name='Course image', **NULLABLE)

    def __str__(self):
        return f'{self.title} {self.description}'

    class Meta:
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Course title')
    description = models.TextField(verbose_name='Course description')
    preview = models.ImageField(upload_to='media/', verbose_name='Course image', **NULLABLE)
    link = models.TextField(verbose_name='Lesson link', **NULLABLE)


    def __str__(self):
        return f'{self.title} {self.description}'

    class Meta:
        verbose_name = 'Lesson'
        verbose_name_plural = 'Lessons'

class Subscription(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='User', **NULLABLE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Course', **NULLABLE)
    is_subscribed = models.BooleanField(default=False, verbose_name='Is subscribed')

    def __str__(self):
        return f'{self.user}: ({self.course})'

    class Meta:
        verbose_name = 'Subscription'
        verbose_name_plural = 'Subscriptions'
