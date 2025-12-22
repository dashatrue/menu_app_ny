from django.shortcuts import render, redirect
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from django.contrib import messages
from django.views.generic import ListView, TemplateView
from django.views import View
from .models import First, Salad, Appetizer, Dessert
from .forms import OrderForm


class MenuView(TemplateView):
    template_name = 'menu_app/menu.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['first_dishes'] = First.objects.all()
        context['salads'] = Salad.objects.all()
        context['appetizers'] = Appetizer.objects.all()
        context['desserts'] = Dessert.objects.all()
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
                context = {
                    'first_dishes': First.objects.all(),
                    'salads': Salad.objects.all(),
                    'appetizers': Appetizer.objects.all(),
                    'desserts': Dessert.objects.all(),
                    'form': form,
                }
                return render(request, 'menu_app/menu.html', context)

    def get_selected_dishes(self, cleaned_data):
        selected_dishes = {}

        first_id = cleaned_data.get('first_dish')
        if first_id:
            try:
                selected_dishes['first'] = First.objects.get(id=first_id)
            except First.DoesNotExist:
                selected_dishes['first'] = None

        salad_id = cleaned_data.get('salad')
        if salad_id:
            try:
                selected_dishes['salad'] = Salad.objects.get(id=salad_id)
            except Salad.DoesNotExist:
                selected_dishes['salad'] = None

        appetizer_id = cleaned_data.get('appetizer')
        if appetizer_id:
            try:
                selected_dishes['appetizer'] = Appetizer.objects.get(id=appetizer_id)
            except Appetizer.DoesNotExist:
                selected_dishes['appetizer'] = None

        dessert_id = cleaned_data.get('dessert')
        if dessert_id:
            try:
                selected_dishes['dessert'] = Dessert.objects.get(id=dessert_id)
            except Dessert.DoesNotExist:
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