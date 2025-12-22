from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse  # Добавьте этот импорт

# Простейший view для теста
def test_view(request):
    return HttpResponse("Django работает!")

urlpatterns = [
    path('test/', test_view),
    path('admin/', admin.site.urls),
    path('', include('menu_app.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)