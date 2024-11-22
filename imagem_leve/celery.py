import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'imagem_leve.settings')

app = Celery('imagem_leve')

app.config_from_object('django.conf.settings', namespace='CELERY')


app.autodiscover_tasks()

@app.task(bind = True)
def debug_task(self):
    print(f'Reques:{self.request!r}')