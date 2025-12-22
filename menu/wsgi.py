import os
import sys
import traceback

print("=== WSGI DEBUG START ===", file=sys.stderr)

try:
    # 1. Проверяем, что переменные окружения установлены
    print(f"1. DJANGO_SETTINGS_MODULE будет: 'menu.settings'", file=sys.stderr)

    # 2. Устанавливаем настройки
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'menu.settings')

    # 3. Проверяем SECRET_KEY ДО импорта Django
    print(f"2. SECRET_KEY в окружении: {bool(os.environ.get('SECRET_KEY'))}", file=sys.stderr)
    print(f"3. ALLOWED_HOSTS: {os.environ.get('ALLOWED_HOSTS')}", file=sys.stderr)

    # 4. Пробуем импортировать Django
    from django.core.wsgi import get_wsgi_application

    print("4. Django успешно импортирован", file=sys.stderr)

    # 5. Пробуем создать application
    application = get_wsgi_application()
    print("5. WSGI application создан успешно", file=sys.stderr)

except ImportError as e:
    print(f"ImportError: {e}", file=sys.stderr)
    traceback.print_exc(file=sys.stderr)


    # Fallback application
    def simple_app(environ, start_response):
        start_response('200 OK', [('Content-Type', 'text/plain')])
        return [b'Error: Import failed in Django']


    application = simple_app

except Exception as e:
    print(f"General error: {e}", file=sys.stderr)
    traceback.print_exc(file=sys.stderr)


    # Fallback application
    def simple_app(environ, start_response):
        start_response('200 OK', [('Content-Type', 'text/plain')])
        return [b'Error: Django setup failed']


    application = simple_app

print("=== WSGI DEBUG END ===", file=sys.stderr)