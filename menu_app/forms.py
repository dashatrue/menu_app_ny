from django import forms
from .models import Dish


class OrderForm(forms.Form):
    first_dish = forms.MultipleChoiceField(
        label='Первое блюдо',
        choices=[],
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'd-none'})
    )
    salad = forms.MultipleChoiceField(
        label='Салат',
        choices=[],
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'd-none'})
    )
    appetizer = forms.MultipleChoiceField(
        label='Закуска',
        choices=[],
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'd-none'})
    )
    dessert = forms.MultipleChoiceField(
        label='Десерт',
        choices=[],
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'd-none'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Заполняем choices из модели Dish с фильтрацией по категориям
        self.fields['first_dish'].choices = [('', '--- Выбери основное блюдо =) ---')] + [
            (dish.id, dish.name) for dish in Dish.objects.filter(category='first')
        ]

        self.fields['salad'].choices = [('', '--- Выбери салатик ---')] + [
            (dish.id, dish.name) for dish in Dish.objects.filter(category='salad')
        ]

        self.fields['appetizer'].choices = [('', '--- Выбери закуски  ---')] + [
            (dish.id, dish.name) for dish in Dish.objects.filter(category='appetizer')
        ]

        self.fields['dessert'].choices = [('', '--- Выбери десерт ---')] + [
            (dish.id, dish.name) for dish in Dish.objects.filter(category='dessert')
        ]