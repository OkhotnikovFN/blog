# blog-

* Приложение предназначено для ведения личного блога, и просмотра блогов других пользователей, с возможностью оставлять комментарии, и загрузки изображений.
В качестве базы данных используется SQLite
Переменные окружения в данном случае не используются. При необходимости, их нужно установить самостоятельно.

* Шаги по тестовой установке, сборке, запуску:  
  1. Клонировать репозиторий на свою рабочую станцию
  2. Перейти в папку проекта и выполнить команды
  
  Для Linux
  
      ```
      python3 -m venv venv
      source venv/Scripts/activate
      pip3 install -r requirements.txt
      cd blog
      python3 manage.py migrate
      python3 manage.py compilemessages  -i venv/*
      python3 manage.py runserver
      ```
      
   Для Windows
   
      ```
      python -m venv venv
      venv\Scripts\activate.bat
      pip install -r requirements.txt
      cd blog
      python manage.py migrate
      python manage.py compilemessages -i venv/*
      python manage.py runserver
      ```
   После выполнения команд на локальном компьютере развернется приложение, доступное по адресу: http://127.0.0.1:8000/