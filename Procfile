release: python manage.py makemigrations apple_game
release: python manage.py migrate
web: gunicorn apple_game_back.wsgi --log-file -