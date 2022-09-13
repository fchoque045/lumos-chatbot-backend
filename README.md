## Setup project

### Create virtual environment

    python3 -m venv env
    source env/bin/activate (On Windows use `env\Scripts\activate`)

### Download requirements
    
    pip install -r requirements.txt

### Make migrations

    python manage.py makemigrations
    python manage.py migrate

### Start application

    python manage.py runserver

### Create superuser (set the password you prefer, you can change this values)
    
    python manage.py createsuperuser --email admin@gmail.com --username admin