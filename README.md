# Приложение 'Сервис терминологии'.
## Описание:
Небольшое приложение в виде RESTful API представляет всего 3 endpoint'а для запросов:
- http://127.0.0.1:8000/refbooks/ - Получение списка справочников (+ актуальных на указанную дату)
- http://127.0.0.1:8000/refbooks/{id}/elements - Получение элементов заданного справочника
- http://127.0.0.1:8000/refbooks/{id}/check_element - Проверка на то, что конкретный элемент присутствует в указанной версии справочника.
### Работа с проектом:
1. **[Опционально]** Установка переменных окружения в файле `.env`
2. Установка зависимостей: `pip install -r requirements.txt`
3. Установка миграций: `python terminology_service/manage.py migrate`
4. Создание админа: `python terminology_service/manage.py createsuperuser`
5. Запуск приложения: `python terminology_service/manage.py runserver`
### Дополнительно:
1. Генерация тестовых данных: `python terminology_service/manage.py filling_the_database`
2. Запуск тестов: `python terminology_service/manage.py test terminology_service`
3. API документация: http://127.0.0.1:8000/api/schema/swagger/
4. Админ панель: http://127.0.0.1:8000/admin/
### Основные технологии: 
- Python 3.10
- Django 5.1.1
- Django REST Framework 3.15.2
- drf-spectacular 0.27.2
- База данных SQLite