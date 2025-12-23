from django.db import models

class Dish(models.Model):
    """Единая модель для всех блюд"""

    CATEGORY_CHOICES = [
        ('first', 'Первое блюдо'),
        ('salad', 'Салат'),
        ('appetizer', 'Закуска'),
        ('dessert', 'Десерт'),
    ]

    # Основные поля
    name = models.CharField('Название', max_length=50)
    category = models.CharField('Категория', max_length=20, choices=CATEGORY_CHOICES)

    # НОВОЕ ПОЛЕ: ссылка на ImgBB (вместо image_filename)
    image_url = models.URLField('Ссылка на картинку', max_length=500, blank=True)

    class Meta:
        verbose_name = 'Блюдо'
        verbose_name_plural = 'Блюда'
        ordering = ['category', 'name']

    def __str__(self):
        return f"{self.get_category_display()}: {self.name}"