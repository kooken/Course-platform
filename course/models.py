from django.db import models

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
    link = models.TextField(verbose_name='Lesson link')


    def __str__(self):
        return f'{self.title} {self.description}'

    class Meta:
        verbose_name = 'Lesson'
        verbose_name_plural = 'Lessons'

