# menu_app/views.py
from django.shortcuts import render, redirect
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from django.contrib import messages
from django.views.generic import TemplateView
from django.views import View
from .models import Dish  # ← импортируем новую модель
from .forms import OrderForm


class MenuView(TemplateView):
    template_name = 'menu_app/menu.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Получаем блюда по категориям из одной модели Dish
        context['first_dishes'] = Dish.objects.filter(category='first')
        context['salads'] = Dish.objects.filter(category='salad')
        context['appetizers'] = Dish.objects.filter(category='appetizer')
        context['desserts'] = Dish.objects.filter(category='dessert')
        context['form'] = OrderForm()
        return context


class OrderSubmitView(View):
    def get(self, request):
        return redirect('menu')

    def post(self, request):
        form = OrderForm(request.POST)

        if form.is_valid():
            customer_name = form.cleaned_data['customer_name']
            comments = form.cleaned_data.get('comments', '')

            selected_dishes = self.get_selected_dishes(form.cleaned_data)

            email_content = self.create_email_content(
                customer_name, selected_dishes, comments
            )

            try:
                self.send_order_email(email_content, customer_name)
                messages.success(
                    request,
                    'Спасибо! Твой заказик отправлен =)'
                )

            except Exception as e:
                messages.error(
                    request,
                    f'Произошла ошибка. {str(e)}'
                )

                return redirect('menu')

            else:
                # Возвращаем контекст с Dish
                context = {
                    'first_dishes': Dish.objects.filter(category='first'),
                    'salads': Dish.objects.filter(category='salad'),
                    'appetizers': Dish.objects.filter(category='appetizer'),
                    'desserts': Dish.objects.filter(category='dessert'),
                    'form': form,
                }
                return render(request, 'menu_app/menu.html', context)

    def get_selected_dishes(self, cleaned_data):
        selected_dishes = {}

        # Для MultipleChoiceField получаем список, берём первый элемент
        first_ids = cleaned_data.get('first_dish', [])
        if first_ids:
            try:
                # Берём первый выбранный элемент из списка
                first_id = first_ids[0] if first_ids else None
                if first_id:
                    selected_dishes['first'] = Dish.objects.get(id=int(first_id), category='first')
            except (ValueError, Dish.DoesNotExist):
                selected_dishes['first'] = None

        salad_ids = cleaned_data.get('salad', [])
        if salad_ids:
            try:
                salad_id = salad_ids[0] if salad_ids else None
                if salad_id:
                    selected_dishes['salad'] = Dish.objects.get(id=int(salad_id), category='salad')
            except (ValueError, Dish.DoesNotExist):
                selected_dishes['salad'] = None

        appetizer_ids = cleaned_data.get('appetizer', [])
        if appetizer_ids:
            try:
                appetizer_id = appetizer_ids[0] if appetizer_ids else None
                if appetizer_id:
                    selected_dishes['appetizer'] = Dish.objects.get(id=int(appetizer_id), category='appetizer')
            except (ValueError, Dish.DoesNotExist):
                selected_dishes['appetizer'] = None

        dessert_ids = cleaned_data.get('dessert', [])
        if dessert_ids:
            try:
                dessert_id = dessert_ids[0] if dessert_ids else None
                if dessert_id:
                    selected_dishes['dessert'] = Dish.objects.get(id=int(dessert_id), category='dessert')
            except (ValueError, Dish.DoesNotExist):
                selected_dishes['dessert'] = None

        return selected_dishes

    def create_email_content(self, name, dishes, comments):
        content = f"""
        НОВЫЙ ЗАКАЗ С САЙТА МЕНЮ

        Информация о клиенте:
        Имя: {name}

        Выбранные блюда:
        """

        if dishes.get('first'):
            content += f"• Первое блюдо: {dishes['first'].name}\n"
        if dishes.get('salad'):
            content += f"• Салат: {dishes['salad'].name}\n"
        if dishes.get('appetizer'):
            content += f"• Закуска: {dishes['appetizer'].name}\n"
        if dishes.get('dessert'):
            content += f"• Десерт: {dishes['dessert'].name}\n"

        if comments:
            content += f"\nКомментарии к заказу:\n{comments}\n"

        return content

    def send_order_email(self, content, customer_name):
        subject = f'Новогодний заказ от {customer_name}'

        send_mail(
            subject=subject,
            message=content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.EMAIL_HOST_USER],
            fail_silently=False,
        )