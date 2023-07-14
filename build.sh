pip install -r requirements.txt
poetry install
python manage.py makemigrations
python3 manage.py migrate
python3 manage.py createsuperuser --noinput