from django import forms

class OrderForm(forms.Form):
    first_dish = forms.ChoiceField(
        label = 'Первое блюдо',
        choices = [],
        required=False,
        widget = forms.Select(attrs={'class': 'form-control'})
    )
    salad = forms.ChoiceField(
        label = 'Салат',
        choices=[],
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    appetizer = forms.ChoiceField(
        label='Закуска',
        choices=[],
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    dessert = forms.ChoiceField(
        label='Десерт',
        choices=[],
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    customer_name = forms.CharField(
        label='Ваше имя',
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Напиши свое имя :)'})
    )

    comments = forms.CharField(
        label="Комментарии к заказу",
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Особые пожелания...'})
    )
    def __init__(self, *args, **kwargs):
        from .models import First, Salad, Appetizer, Dessert
        super().__init__(*args, **kwargs)

        self.fields['first_dish'].choices = [('', '--- Выбери основное блюдо =) ---')] + [
            (f.id, f.name) for f in First.objects.all()
        ]
        self.fields['salad'].choices = [('', '--- Выбери салатик ---')] + [
            (s.id, s.name) for s in Salad.objects.all()
        ]
        self.fields['appetizer'].choices = [('', '--- Выбери закуски  ---')] + [
            (a.id, a.name) for a in Appetizer.objects.all()
        ]
        self.fields['dessert'].choices = [('', '--- Выбери десерт ---')] + [
            (d.id, d.name) for d in Dessert.objects.all()
        ]