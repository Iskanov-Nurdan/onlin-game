import uuid
from django.db import models
from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.auth.models import User

User = get_user_model()

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Цена в сомах")
    image = models.ImageField(upload_to='products/')
    stock = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class Order(models.Model):
    order_number = models.CharField(max_length=100, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Генерируем случайный номер заказа, если он еще не установлен
        if not self.order_number:
            self.order_number = str(uuid.uuid4())[:8]
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Заказ {self.order_number} пользователя {self.user.username}"

from django.db import models
from django.contrib.auth.models import User

LANGUAGE_CHOICES = [
    ('en', 'Английский'),
    ('ru', 'Русский'),
    ('de', 'Немецкий'),
    ('fr', 'Французский'),
    # добавляй по мере необходимости
]

class TranslationTask(models.Model):
    title = models.CharField(max_length=255)
    source_lang = models.CharField(max_length=5, choices=LANGUAGE_CHOICES)
    target_lang = models.CharField(max_length=5, choices=LANGUAGE_CHOICES)
    translation_type = models.CharField(max_length=100, blank=True)
    document = models.FileField(upload_to='translations/')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Ожидает'),
        ('in_progress', 'В работе'),
        ('completed', 'Завершен')
    ], default='pending')
    assigned_to = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.title

