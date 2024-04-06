from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
import logging


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'youtube_search.settings')

app = Celery('youtube_search')
app.config_from_object('django.conf:settings', namespace='CELERY')

# Setup logging
log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(format=log_format, level=logging.INFO)

app.autodiscover_tasks()

# Define periodic tasks
# app.conf.beat_schedule = {
#     'fetch-youtube-videos-every-10-seconds': {
#         'task': 'syncthing.tasks.fetch_youtube_videos',
#         'schedule': 10.0,  # Run every 10 seconds
#     },
# }
@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')