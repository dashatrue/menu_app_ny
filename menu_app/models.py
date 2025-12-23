from django.db import models


class Dish(models.Model):
    """Единая модель для всех блюд"""

    # Категории блюд
    CATEGORY_CHOICES = [
        ('first', 'Первое блюдо'),
        ('salad', 'Салат'),
        ('appetizer', 'Закуска'),
        ('dessert', 'Десерт'),
    ]

    # Поля
    name = models.CharField('Название', max_length=50)
    category = models.CharField('Категория', max_length=20, choices=CATEGORY_CHOICES)
    image_filename = models.CharField('Имя файла картинки', max_length=100, blank=True)

    class Meta:
        verbose_name = 'Блюдо'
        verbose_name_plural = 'Блюда'
        ordering = ['category', 'name']  # Сортировка по категории и имени

    def __str__(self):
        return f"{self.get_category_display()}: {self.name}"

    @property
    def image_url(self):
        """Возвращает URL картинки для шаблона"""
        if self.image_filename:
            return f'/static/dishes/{self.image_filename}'
        return ''

    def save(self, *args, **kwargs):
        """Автоматически генерируем имя файла при сохранении"""
        if not self.image_filename and self.name:
            # Создаем имя файла: категория_название.png
            name_slug = self.name.lower().replace(' ', '_')
            # Заменяем русские буквы и спецсимволы
            name_slug = (name_slug.replace('ё', 'e')
                         .replace('й', 'i')
                         .replace('ц', 'ts')
                         .replace(' ', '_'))
            self.image_filename = f'{self.category}_{name_slug}.png'
        super().save(*args, **kwargs)