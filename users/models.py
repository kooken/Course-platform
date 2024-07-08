from django.contrib.auth.models import AbstractUser
from django.db import models
from course.models import Course, Lesson

# Create your models here.
NULLABLE = {'null': True,
            'blank': True}

class User(AbstractUser):
    phone = models.CharField(max_length=35, verbose_name='phone', **NULLABLE)
    avatar = models.ImageField(upload_to='users/', verbose_name='avatar', **NULLABLE)
    username = None
    email = models.EmailField(unique=True, verbose_name='почта')
    city = models.CharField(max_length=100, verbose_name='city', **NULLABLE)

    token = models.CharField(max_length=100, verbose_name='token', **NULLABLE)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.email


class Payments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="пользователь")
    pay_date = models.DateTimeField(auto_now=True, verbose_name="дата оплаты")
    paid_course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="оплаченный курс", **NULLABLE)
    paid_lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name="оплаченный урок", **NULLABLE)
    pay_sum = models.PositiveIntegerField(verbose_name="сумма оплаты")
    pay_transfer = models.BooleanField(default=True, verbose_name="оплата переводом")

    def __str__(self):
        return f"{self.user}"

    class Meta:
        verbose_name = "Payment"
        verbose_name_plural = "Payments"