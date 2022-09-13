import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SQLITE = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

POSTGRESQL = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'd6g5lt4i4m84q',
        'USER': 'xjlduajilpnbrj',
        'PASSWORD': 'b0bf61bdf47d1042981dc12b5cabd837895a42a21f7d3b893999cc6e3917c186',
        'HOST': 'ec2-34-227-135-211.compute-1.amazonaws.com',
        'PORT': '5432',
    }
}